from typing import Protocol, TypeVar

from sikei.events.event import Event

E = TypeVar("E", bound=Event, contravariant=True)


class EventHandler(Protocol[E]):
    """
    The event handler interface.

    Usage::

      class UserJoinedEventHandler(EventHandler[UserJoinedEventHandler])
          def __init__(self, meetings_api: MeetingAPIProtocol) -> None:
              self._meetings_api = meetings_api

          async def handle(self, event: UserJoinedEventHandler) -> None:
              await self._meetings_api.notify_room(event.meeting_id, "New user joined!")

    """

    async def handle(self, event: E) -> None:
        raise NotImplementedError
