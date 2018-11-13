__all__ = (
    'AsyncInit',
)


class AsyncInit(object):
    async def __async_init__(self):
        raise NotImplementedError()

    async def close(self):
        pass

    def __enter__(self):
        raise TypeError("Use async with instead")

    def __exit__(self, exc_type, exc_val, exc_tb):
        # __exit__ should exist in pair with __enter__ but never executed
        pass  # pragma: no cover

    def __await__(self):
        return self.__async_init__().__await__()

    async def __aenter__(self):
        await self.__async_init__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
