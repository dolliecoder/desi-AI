---
topic: Python Basics
framework: Python
difficulty: Beginner
---

# Python Basics

## Variables and Data Types

Python is dynamically typed, meaning you don't need to declare variable types explicitly. The interpreter infers the type based on the value assigned.

```python
# Integer
age = 25

# Float
price = 19.99

# String
name = "Rahul"

# Boolean
is_student = True

# List
fruits = ["apple", "banana", "mango"]

# Dictionary
person = {"name": "Priya", "age": 22, "city": "Mumbai"}
```

## Control Flow

### If-Else Statements

```python
score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")
```

### Loops

**For Loop:**
```python
# Iterate over a list
fruits = ["apple", "banana", "mango"]
for fruit in fruits:
    print(fruit)

# Range-based loop
for i in range(5):
    print(i)  # Prints 0 to 4
```

**While Loop:**
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

## Functions

Functions in Python are defined using the `def` keyword.

```python
def greet(name):
    return f"Hello, {name}!"

# Function with default parameter
def add(a, b=0):
    return a + b

# Function with multiple return values
def get_user_info():
    return "Amit", 25, "Delhi"

name, age, city = get_user_info()
```

## List Comprehensions

List comprehensions provide a concise way to create lists.

```python
# Create a list of squares
squares = [x**2 for x in range(10)]

# Filter even numbers
evens = [x for x in range(20) if x % 2 == 0]

# Transform strings
names = ["rahul", "priya", "amit"]
capitalized = [name.capitalize() for name in names]
```

## Exception Handling

Handle errors gracefully using try-except blocks.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("This always executes")
```

## File Operations

```python
# Reading a file
with open("data.txt", "r") as file:
    content = file.read()
    print(content)

# Writing to a file
with open("output.txt", "w") as file:
    file.write("Hello, World!")

# Appending to a file
with open("log.txt", "a") as file:
    file.write("New log entry\n")
```

## Common Built-in Functions

- `len()`: Get length of a sequence
- `type()`: Get type of an object
- `str()`, `int()`, `float()`: Type conversion
- `input()`: Get user input
- `print()`: Display output
- `range()`: Generate sequence of numbers
- `enumerate()`: Get index and value in loops
- `zip()`: Combine multiple iterables

## Tips for Beginners

1. **Indentation matters**: Python uses indentation to define code blocks
2. **Use meaningful variable names**: `user_age` is better than `x`
3. **Follow PEP 8**: Python's style guide for clean code
4. **Use f-strings**: Modern way to format strings (Python 3.6+)
5. **Practice regularly**: Build small projects to reinforce concepts
