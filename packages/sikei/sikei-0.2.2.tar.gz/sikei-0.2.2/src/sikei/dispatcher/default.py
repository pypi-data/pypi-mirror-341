from sikei.container.protocol import Container
from sikei.dispatcher.result import DispatchResult
from sikei.middlewares.base import MiddlewareChain
from sikei.requests.map import RequestMap
from sikei.requests.request import Request


class DefaultDispatcher:
    def __init__(
        self,
        request_map: RequestMap,
        container: Container,
        middleware_chain: MiddlewareChain | None = None,
    ) -> None:
        self._request_map = request_map
        self._container = container
        self._middleware_chain = middleware_chain or MiddlewareChain()

    async def dispatch(self, request: Request) -> DispatchResult:
        handler_type = self._request_map.get(type(request))

        handler = await self._container.resolve(handler_type)

        wrapped_handle = self._middleware_chain.wrap(handler.handle)

        response = await wrapped_handle(request)

        return DispatchResult(response=response, events=handler.events)
