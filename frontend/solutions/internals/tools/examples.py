from langchain_core.tools import tool


@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' times 'y'."""
    return x * y


@tool
def exponentiate(x: float, y: float) -> float:
    """Raise 'x' to the 'y'."""
    return x**y


@tool
def add(x: float, y: float) -> float:
    """Add 'x' and 'y'."""
    return x + y


@tool
def get_current_weather(city: str) -> str:
    """Get the current weather in 'city'."""
    return f"The weather in {city} is sunny."
