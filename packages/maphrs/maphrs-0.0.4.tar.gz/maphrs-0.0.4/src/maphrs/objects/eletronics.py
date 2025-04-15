from typing import Union

Number = Union[int, float]

class Resistor:
    """
    Represents an electrical resistor with a given resistance value in ohms.

    Supports arithmetic operations to simulate resistor combinations in series and parallel.

    :param value: Resistance value in ohms.
    """
    def __init__(self, value: Number):
        """
        Initializes a Resistor with a given resistance value.

        :param value: Resistance value in ohms.
        """
        self.value = value

    def __add__(self, other: "Resistor"):
        """
        Returns a new Resistor representing the series combination of two resistors.

        :param other: Another Resistor to combine in series.
        :return: A new Resistor with resistance equal to the sum of both resistors.
        """
        return Resistor(self.value + other.value)

    def __or__(self, other: "Resistor"):
        """
        Returns a new Resistor representing the parallel combination of two resistors.

        :param other: Another Resistor to combine in parallel.
        :return: A new Resistor with resistance equal to the parallel formula.
        """
        return Resistor((self.value * other.value) / (self.value + other.value))

    def __repr__(self):
        """
        Returns a string representation of the Resistor instance.

        :return: A string in the format 'Resistor(value=...)'.
        """
        return f"Resistor(value={self.value})"

class ResistorUnit:
    """
    Defines common resistor units as tuples containing the unit name and its multiplier.

    Units:
        - ohm:      base unit (1)
        - kilohm:   10^3 ohms
        - megaohm:  10^6 ohms
    """
    ohm = ("ohm", 1)
    kilohm = ("kilohm", 10**3)
    megaohm = ("megaohm", 10**6)

class CommercialResistors:
    """
    Provides access to commercial resistor values based on the E24 series.

    The E24 series includes 24 logarithmically spaced values per decade,
    and this class scales them across multiple decades (1Ω to 10MΩ).
    """
    E24Base = [Resistor(r) for r in
           [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8,
            2.0, 2.2, 2.4, 2.7,
            3.0, 3.3, 3.6, 3.9,
            4.3, 4.7,
            5.1, 5.6,
            6.2, 6.8,
            7.5,
            8.2,
            9.1]]

    @property
    def E24(self):
        """
        Returns a list of Resistor instances from the E24 series,
        scaled across multiple decades (from 1Ω up to 10MΩ).

        :return: List of Resistor objects representing the full E24 commercial series.
        """
        return [Resistor(resistor.value * 10 ** exp) for exp in range(0, 7) for resistor in self.E24Base]

COMMERCIAL_RESISTORS = CommercialResistors()