# Dict 2 Dataclass

This is a simple python script that converts a dictionary to a class. It is useful when you want to access the dictionary values as class attributes.

It performs type checking and will raise a `ValueError` if the dictionary does not match the class attributes.

## Usage

```python
from dict2dataclass import FromDict
from dataclasses import dataclass

@dataclass
class Address(FromDict):
    street: str
    city: str
    state: str

@dataclass
class Person(FromDict):
    name: str
    age: int
    address: Address

data = {
    "name": "John Doe",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL"
    }
}

person = Person.from_dict(data)
print(person.name) # John Doe
```
