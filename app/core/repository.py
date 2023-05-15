from abc import abstractmethod, ABCMeta

from starlette.requests import Request


class Repository(metaclass=ABCMeta):
    request: Request

    @abstractmethod
    async def objs_list(self, **kwargs):
        ...

    @abstractmethod
    async def get(self, _id: int):
        ...

    @abstractmethod
    async def create(self, data):
        ...

    @abstractmethod
    async def update(self, _id, data):
        ...

    @abstractmethod
    async def delete(self, _id: int):
        ...
