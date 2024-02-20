from typing import TypeVar

T = TypeVar('T')

class InterfaceDao:
    def get(self, id: int) -> T:
        pass

    def get_all(self) -> list[T]:
        pass

    def create(self, obj: T) -> T:
        pass

    def update(self, obj: T) -> T:
        pass

    def delete(self, id: int) -> bool:
        pass