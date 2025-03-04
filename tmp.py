from pydantic import BaseModel, PrivateAttr

class MyModel(BaseModel):
    public_field: int
    _private_field: int = PrivateAttr()

    def __init__(self, public_field: int, private_field: int, **data):
        super().__init__(public_field=public_field, **data)
        self._private_field = private_field

# Создаем два объекта
obj1 = MyModel(public_field=1, private_field=10)
obj2 = MyModel(public_field=1, private_field=20)

# Сравниваем объекты
print(obj1 == obj2) 