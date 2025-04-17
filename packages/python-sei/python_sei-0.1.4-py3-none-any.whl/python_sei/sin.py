from typing import Literal


def decode_sin(value: str) -> bool:
    """Transforma uma string com valores S/N em bool"""
    match value.lower():
        case "n":
            return False
        case "s":
            return True
        case _:
            raise ValueError("Invalid value for SIN")


def encode_sin(value: bool) -> Literal["S", "N"]:
    """Transforma um valor bool em S/N"""
    return "S" if value else "N"
