from pynanoid import generate


def generate_code(length: int = 6) -> str:
    return generate(size=length)
