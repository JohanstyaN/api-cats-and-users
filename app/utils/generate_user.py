import re


def generate_username(name: str, last_name: str) -> str:
    clean = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
    return f"{clean(name)}.{clean(last_name)}"
