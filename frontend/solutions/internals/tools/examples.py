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
def get_datetime_today() -> str:
    """Get today's date in the format 'YYYY/MM/DD'."""
    import datetime

    return datetime.datetime.now().strftime("%Y/%m/%d")


@tool
def get_date_from_offset(offset: int) -> str:
    """Get the date 'offset' days from today in the format 'YYYY/MM/DD'."""
    import datetime

    return (datetime.datetime.now() + datetime.timedelta(days=offset)).strftime("%Y/%m/%d")


@tool
def get_date_diffs(yyyymmdd1: str, yyyymmdd2: str) -> str:
    """Get the difference between two dates in days."""
    import datetime

    date1 = datetime.datetime.strptime(yyyymmdd1, "%Y/%m/%d")
    date2 = datetime.datetime.strptime(yyyymmdd2, "%Y/%m/%d")
    return abs((date1 - date2).days)
