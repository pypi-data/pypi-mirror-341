def newtons_second_law(mass: float, acceleration: float) -> float:
    """This function calculates the force exerted on an object using Newton's
    second law of motion: F = m * a.

    Args:
        mass (float): The mass of the object in kilograms. Must be
            non-negative.
        acceleration (float): The acceleration of the object in meters per
            second squared.

    Returns:
        float: The force exerted on the object in newtons (N).

    Raises:
        ValueError: If 'mass' is negative.
    """
    if mass < 0:
        raise ValueError("Mass must be non-negative.")

    return mass * acceleration
