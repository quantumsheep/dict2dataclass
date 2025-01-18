# Dict 2 Dataclass

This is a simple python script that converts a dictionary to a dataclass and a dataclass to a dictionary. It is useful when you want to access the dictionary values as class attributes.

## Usage

### Dict -> Dataclass

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

### Dataclass -> Dict

```python
from dict2dataclass import ToDict
from dataclasses import dataclass

@dataclass
class Address(ToDict):
    street: str
    city: str
    state: str

@dataclass
class Person(ToDict):
    name: str
    age: int
    address: Address

person = Person(
    name="John Doe",
    age=30,
    address=Address(
        street="123 Main St",
        city="Springfield",
        state="IL"
    )
)

data = person.to_dict()
print(data) # {'name': 'John Doe', 'age': 30, 'address': {'street': '123 Main St', 'city': 'Springfield', 'state': 'IL'}}
```
