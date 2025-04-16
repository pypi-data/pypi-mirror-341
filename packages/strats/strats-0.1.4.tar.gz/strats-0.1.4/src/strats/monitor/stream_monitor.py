import asyncio
import logging
from typing import Callable, Optional, TypeVar

from strats.core import Monitor, State
from strats.exchange import StreamClient

logger = logging.getLogger(__name__)


S = TypeVar("S")


class StreamMonitor(Monitor):
    def __init__(
        self,
        client: StreamClient,
        data_name: Optional[str] = None,
        on_init: Optional[Callable] = None,
        on_delete: Optional[Callable] = None,
        on_pre_event: Optional[Callable] = None,
        on_post_event: Optional[Callable] = None,
    ):
        self.client = client
        self.data_name = data_name

        # Lifecycle Hook
        self.on_init = on_init
        self.on_delete = on_delete
        self.on_pre_event = on_pre_event
        self.on_post_event = on_post_event

    @property
    def name(self) -> str:
        return f"StreamMonitor/{self.data_name}"

    async def run(self, state: Optional[State]):
        try:
            logger.info(f"{self.name} start")

            data_descriptor = None
            if state is not None and self.data_name:
                if self.data_name in type(state).__dict__:
                    data_descriptor = type(state).__dict__[self.data_name]
                else:
                    raise ValueError(f"data_name: `{self.data_name}` is not found in State")

            if self.on_init is not None:
                self.on_init()

            async for data in self.client.stream():
                if self.on_pre_event is not None:
                    self.on_pre_event()

                if data_descriptor is not None:
                    try:
                        data_descriptor.__set__(state, data)
                    except Exception as e:
                        logger.error(f"failed to update state.{self.data_name}: {e}")

                if self.on_post_event is not None:
                    self.on_post_event(data)

        except asyncio.CancelledError:
            # To avoid "ERROR:asyncio:Task exception was never retrieved",
            # Re-raise the CancelledError
            raise
        except Exception as e:
            logger.error(f"Unhandled exception in {self.name}: {e}")
        finally:
            if self.on_delete is not None:
                self.on_delete()
            logger.info(f"{self.name} stopped")
