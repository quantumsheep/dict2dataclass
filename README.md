# Dict 2 Dataclass

A lightweight Python utility to seamlessly convert between dictionaries and dataclasses. This is useful when you want to access dictionary values as class attributes or serialize dataclasses back to dictionaries.

## Features

- 🚀 **Easy Conversion:** Convert dictionaries to dataclasses and vice versa.
- 🔗 **Nested Support:** Handles nested dataclasses effortlessly.
- 🧩 **Intuitive API:** Simple and clean syntax for integration.

## Installation

```bash
pip install dict2dataclass
```

## Usage

> **Note**
> The `FromDict` and `ToDict` classes are **compatible**. You can use both in the same dataclass for full bidirectional conversion.

### Convert Dictionary to Dataclass

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

# Example dictionary
data = {
    "name": "John Doe",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL"
    }
}

# Convert to dataclass
person = Person.from_dict(data)
print(person.name)      # Output: John Doe
print(person.address.city)  # Output: Springfield
```

### Convert Dataclass to Dictionary

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

# Create a dataclass instance
person = Person(
    name="John Doe",
    age=30,
    address=Address(
        street="123 Main St",
        city="Springfield",
        state="IL"
    )
)

# Convert to dictionary
data = person.to_dict()
print(data)
# Output: {'name': 'John Doe', 'age': 30, 'address': {'street': '123 Main St', 'city': 'Springfield', 'state': 'IL'}}
```

## Combining `FromDict` and `ToDict`

For full bidirectional support, you can inherit from both `FromDict` and `ToDict`:

```python
from dict2dataclass import FromDict, ToDict
from dataclasses import dataclass

@dataclass
class Address(FromDict, ToDict):
    street: str
    city: str
    state: str

@dataclass
class Person(FromDict, ToDict):
    name: str
    age: int
    address: Address
```
