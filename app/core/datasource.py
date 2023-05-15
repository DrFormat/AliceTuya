from abc import abstractmethod, ABC


class Datasource(ABC):
    def __init__(self, system_id: int):
        self.system_id = system_id

    @abstractmethod
    async def objs_list(self, **kwargs):
        ...
