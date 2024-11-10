# WroqCompany Assesment Project

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13%2B-blue)

This is a sample project that requested by the WorqCompany for assesment purpose.

## Table of Contents
- [Purpose](#purpose)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Purpose
- Creating a Main Service in 3-Tier Architecture that supports SAGA Choreography 
- Creating a Virtual Service for SAGA execution
- Both services are written with FAS

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/calculator-project.git
    cd calculator-project
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

```python
from calculator import Calculator
from my_logger import Logger  # Replace with your logger

logger = Logger()
calc = Calculator(logger=logger)

# Perform some operations
result_add = calc.add(2, 3)
result_divide = calc.divide(10, 2)

print(f"Addition Result: {result_add}")
print(f"Division Result: {result_divide}")

