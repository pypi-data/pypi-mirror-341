from math import sqrt


def pythagorean_theorem(a: float, b: float) -> float:
    """This function calculates the hypotenuse of a right triangle using the
    Pythagorean theorem: c^2 = a^2 + b^2.

    Args:
        a (float): Length of one leg of the triangle. Must be non-negative.
        b (float): Length of the other leg of the triangle. Must be
            non-negative.

    Returns:
        float: The length of the hypotenuse.

    Raises:
        ValueError: If either 'a' or 'b' is negative.
    """
    if a < 0 or b < 0:
        raise ValueError(
            "Lengths of the triangle's legs must be non-negative.",
        )

    return sqrt(a**2 + b**2)
