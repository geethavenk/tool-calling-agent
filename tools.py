from langchain_core.tools import tool
from datetime import datetime
from zoneinfo import ZoneInfo


# -------------------------
# TOOL 1: CALCULATOR
# -------------------------

@tool
def calculator(a: float, b: float, operation: str) -> float:
    """
    Perform a basic mathematical calculation like addition, subtraction, multiplication or division.

    Args:
        a: First number.
        b: Second number.
        operation: One of add, subtract, multiply, or divide.

    Returns:
        The result of the calculation.
    """

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    else:
        raise ValueError(
            "Unsupported operation. "
            "Use add, subtract, multiply, or divide."
        )


# -------------------------
# TOOL 2: UNIT CONVERTER
# -------------------------

@tool
def unit_converter(
    value: float,
    from_unit: str, 
    to_unit: str
) -> str:
    """
    Convert between the supported units.

    Convert a value between units of length, mass, or temperature.

    Args:
        value: The numeric quantity to convert.
        from_unit: One of kilometers, miles, kilograms, pounds, celsius,
            fahrenheit. Abbreviations (km, mi, kg, lb, c, f) also work.
        to_unit: Same list, must measure the same quantity as from_unit.

    Returns:
        A string like "5 kilometers = 3.11 miles".
    """
    aliases = {
        "km": "kilometers", "mi": "miles", "mile": "miles",
        "kg": "kilograms", "lb": "pounds", "lbs": "pounds",
        "c": "celsius", "f": "fahrenheit",
    }
    conversions = {
        ("kilometers", "miles"): lambda v: v * 0.621371,
        ("miles", "kilometers"): lambda v: v / 0.621371,
        ("kilograms", "pounds"): lambda v: v * 2.20462,
        ("pounds", "kilograms"): lambda v: v / 2.20462,
        ("celsius", "fahrenheit"): lambda v: v * 9 / 5 + 32,
        ("fahrenheit", "celsius"): lambda v: (v - 32) * 5 / 9,
    }

    def clean(u):
        u = u.strip().lower()
        return aliases.get(u, u)

    src, tgt = clean(from_unit), clean(to_unit)

    if src == tgt:
        return f"{value} {src} = {value} {tgt}"

    if (src, tgt) not in conversions:
        units = sorted({u for pair in conversions for u in pair})
        return f"Cannot convert {src} to {tgt}. Supported units: {", ".join(units)}"

    result = conversions[(src, tgt)](float(value))
    return f"{value} {src} = {result:.2f} {tgt}"

# -------------------------
# TOOL 3: DATE AND TIME
# -------------------------


@tool
def get_current_datetime(timezone: str = "UTC") -> str:
    """
    Get the current date and time.

    Use when the user asks for today's date, the current time, the day of
    the week, or needs to reason about what "today", "tomorrow", or "next
    week" refers to.

    Args:
        timezone: IANA timezone name, e.g. "Europe/Berlin", "US/Eastern",
            "Asia/Tokyo". Defaults to "UTC". Pass the user's timezone when
            it is known; otherwise leave as UTC.

    Returns:
        A string like "Wednesday, 9 September 2026, 14:32 CEST".
    """
    try:
        tz = ZoneInfo(timezone)
    except Exception:
        return (
            f"Unknown timezone {timezone!r}. Use an IANA name such as "
            f"'Europe/Berlin', 'US/Eastern', or 'UTC'."
        )

    now = datetime.now(tz)
    return now.strftime(f"%A, {now.day} %B %Y, %H:%M %Z")

# -------------------------
# TOOL 4: TEXT COUNTER
# -------------------------

@tool
def text_counter(text: str) -> dict:
    """
    Count words and characters in a piece of text.

    Use when the user asks about word count, character count, or text length.

    Args:
        text: The text to measure.

    Returns:
        A dict with word_count, character_count (including spaces), and
        character_count_no_spaces.
    """
    words = text.split()
    return {
        "word_count": len(words),
        "character_count": len(text),
        "character_count_no_spaces": len(text) - sum(c.isspace() for c in text),
    }

# -------------------------
# TOOL 5: INFORMATION LOOKUP
# -------------------------

LANGUAGE_DATA = {
    "python": {
        "creator": "Guido van Rossum",
        "year": 1991,
        "use_cases": [
            "Data Science",
            "Machine Learning",
            "Web Development",
            "Automation"
        ]
    },

    "java": {
        "creator": "James Gosling",
        "year": 1995,
        "use_cases": [
            "Enterprise Applications",
            "Android Development"
        ]
    },

    "javascript": {
        "creator": "Brendan Eich",
        "year": 1995,
        "use_cases": [
            "Frontend Development",
            "Backend Development"
        ]
    }
}

@tool
def lookup_language(language: str) -> dict:
    """
    Look up structured information about a programming language.

    Args:
        language: Language name. One of: python, java, javascript.

    Returns:
        A dict with creator, year, and use_cases — or an error key if the
        language is not in the dataset.
    """
    language = language.strip().lower()

    if language not in LANGUAGE_DATA:
        available = ", ".join(sorted(LANGUAGE_DATA))
        return {"error": f"No information found for '{language}'. Available: {available}."}

    return {"language": language, **LANGUAGE_DATA[language]}

tools = [
    calculator,
    unit_converter,
    get_current_datetime,
    text_counter,
    lookup_language
]