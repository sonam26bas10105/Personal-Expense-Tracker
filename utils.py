"""Small console helpers."""
def line(width: int = 40, char: str = "-") -> None:
    """Print a horizontal separator line."""
    print(char * width)


def pause_for_user(message: str = "Press Enter to continue...") -> None:
    """Wait for Enter; silently continue when there is no interactive input."""
    try:
        input(message)
    except EOFError:
        pass
