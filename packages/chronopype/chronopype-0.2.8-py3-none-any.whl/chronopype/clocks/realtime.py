import asyncio
import time
from collections.abc import Callable

from chronopype.clocks.base import BaseClock, ClockTickEvent
from chronopype.clocks.config import ClockConfig
from chronopype.clocks.modes import ClockMode
from chronopype.exceptions import ClockError
from chronopype.processors.base import TickProcessor


class RealtimeClock(BaseClock):
    """Clock implementation for realtime mode."""

    start_publication = BaseClock.start_publication
    tick_publication = BaseClock.tick_publication
    stop_publication = BaseClock.stop_publication

    def __init__(
        self,
        config: ClockConfig,
        error_callback: Callable[[TickProcessor, Exception], None] | None = None,
    ) -> None:
        """Initialize a new RealtimeClock instance."""
        if config.clock_mode != ClockMode.REALTIME:
            raise ClockError("RealtimeClock requires REALTIME mode")
        super().__init__(config, error_callback)

    async def run(self) -> None:
        """Run the clock indefinitely."""
        try:
            await self.run_til(float("inf"))
        except asyncio.CancelledError:
            # Ensure we're properly cleaned up
            self._shutdown_event.set()
            if self._running:
                self._running = False
                self._task = None
            raise  # Re-raise to ensure proper cancellation

    async def run_til(self, target_time: float) -> None:
        """Run the clock until the target time."""
        if self._task is not None:
            raise ClockError("Clock is already running")

        self._running = True
        self._started = True

        # Calculate the actual target time based on current time
        current_time = time.time()
        duration = target_time - self._current_tick
        actual_target = current_time + duration

        self._task = asyncio.create_task(
            self._run_til_impl(actual_target, self._processors)
        )

        # Activate all processors
        for processor in self._processors:
            state = self._processor_states[processor]
            self._processor_states[processor] = state.model_copy(
                update={"is_active": True}
            )

        try:
            await self._task
        finally:
            self._task = None

    async def _run_til_impl(
        self, target_time: float, processors: list[TickProcessor]
    ) -> None:
        """Run the clock until a specific timestamp."""
        if not self._running:
            raise ClockError("Clock must be started.")

        while time.time() < target_time:
            processors = [p for p in processors if self._processor_states[p].is_active]
            await self._execute_tick(processors)
            await self._wait_next_tick()

    async def _wait_next_tick(self) -> float:
        """Wait until the next tick."""
        current_time = time.time()
        next_tick = (
            current_time // self._config.tick_size + 1
        ) * self._config.tick_size
        wait_time = next_tick - current_time

        if wait_time > 0:
            try:
                await asyncio.sleep(wait_time)
            except asyncio.CancelledError:
                raise

        # Account for any drift that occurred during sleep
        actual_time = time.time()
        if actual_time > next_tick:
            # We've drifted, adjust next_tick to the nearest future tick
            ticks_passed = int((actual_time - next_tick) / self._config.tick_size)
            next_tick += (ticks_passed + 1) * self._config.tick_size

        # Update current tick to the *current* tick boundary, not the next one
        self._current_tick = (
            actual_time // self._config.tick_size
        ) * self._config.tick_size
        return next_tick

    async def _execute_tick(self, processors: list[TickProcessor]) -> None:
        """Execute a tick for all processors."""
        self._tick_counter += 1

        if self._config.concurrent_processors:
            # Execute processors concurrently
            tasks = []
            for processor in processors:
                task = asyncio.create_task(
                    self._execute_processor(processor, self._current_tick)
                )
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)
            errors = []

            # Update states for all processors first
            for processor, result in zip(processors, results, strict=False):
                if isinstance(result, Exception):
                    if self._error_callback:
                        self._error_callback(processor, result)
                    errors.append(result)
                else:
                    # Update processor state after successful execution
                    state = self._processor_states[processor]
                    self._processor_states[processor] = state.model_copy(
                        update={"last_timestamp": self._current_tick}
                    )

            # Emit tick event after all processors have been executed
            self.publish(
                self.tick_publication,
                ClockTickEvent(
                    timestamp=self._current_tick,
                    emission_timestamp=time.time(),
                    tick_counter=self._tick_counter,
                    processors=self.get_active_processors(),
                ),
            )

            # Raise the first error if any occurred
            if errors:
                raise errors[0]
        else:
            # Execute processors sequentially
            for processor in processors:
                try:
                    await self._execute_processor(processor, self._current_tick)
                    # Update processor state after successful execution
                    state = self._processor_states[processor]
                    self._processor_states[processor] = state.model_copy(
                        update={"last_timestamp": self._current_tick}
                    )
                except Exception as e:
                    if self._error_callback:
                        self._error_callback(processor, e)
                    raise e

            # Emit tick event after all processors have been executed
            self.publish(
                self.tick_publication,
                ClockTickEvent(
                    timestamp=self._current_tick,
                    emission_timestamp=time.time(),
                    tick_counter=self._tick_counter,
                    processors=self.get_active_processors(),
                ),
            )
