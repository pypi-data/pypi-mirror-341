import pytest

from pyquations.physics.newtons_second_law import newtons_second_law


@pytest.mark.parametrize(
    "mass, acceleration, expected",
    [
        (10, 9.8, 98),
        (0, 9.8, 0),
        (5, 0, 0),
        (1.5, 3.2, pytest.approx(4.8)),
        (100, 1.5, 150),
    ],
)
def test_newtons_second_law(mass, acceleration, expected):
    assert newtons_second_law(mass, acceleration) == expected


@pytest.mark.parametrize(
    "mass, acceleration",
    [
        (-1, 9.8),
        (-5, 0),
    ],
)
def test_newtons_second_law_invalid(mass, acceleration):
    with pytest.raises(ValueError):
        newtons_second_law(mass, acceleration)
