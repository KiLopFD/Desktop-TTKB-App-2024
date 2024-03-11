from typing import TypeVar

T = TypeVar('T') # Generic type

'''
    Interface cho các đối tượng DAO

    Định nghĩa các phương thức cơ bản cho các đối tượng DAO

    - get_by_id: lấy đối tượng theo id
    - get_all: lấy tất cả các đối tượng
    - create: tạo đối tượng
    - update: cập nhật đối tượng
    - delete: xóa đối tượng
'''
class InterfaceDao:
    def get_by_id(self, id: int) -> T:
        pass

    def get_all(self) -> list[T]:
        pass

    def create(self, obj: T) -> T:
        pass

    def update(self, obj: T) -> T:
        pass

    def delete(self, id: int) -> bool:
        pass


