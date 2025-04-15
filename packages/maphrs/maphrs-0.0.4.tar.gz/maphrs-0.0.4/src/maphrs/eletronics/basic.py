from typing import Literal, Union

from maphrs.objects.eletronics import COMMERCIAL_RESISTORS, Resistor
from maphrs.statistics.descriptive import relative_error


Number = Union[int, float]

def find_resistor_association(
    value: Number,
    association_type: Literal["series", "parallel"] = "series",
    tolerance: int = 10,
):
    """
    Finds combinations of two commercial resistors from the E24 series that,
    when combined in series or parallel, result in a value close to the target resistance.

    :param value: Target total resistance value (in ohms) to approximate with the combination.
    :param association_type: Type of resistor association.
                             Can be "series" (direct sum) or "parallel" (parallel combination).
    :param tolerance: Maximum acceptable tolerance between the resulting value and the target value, in percent.
    :return: List of dictionaries containing the resistor pair (r1 and r2),
             the resulting combined value, and the relative error compared to the target value.

    Examples:
        >>> assoc_p = find_resistor_association(13260, "parallel", 30)

        >>> assoc_p[0]
        {'r1': Resistor(value=20000.0),
         'r2': Resistor(value=39000.0),
         'value': Resistor(value=13220.338983050848),
         'relative error': 0.29910269192422567}

        >>> assoc_s = find_resistor_association(13260)

        >>> assoc_s[0]
        {'r1': Resistor(value=270.0),
         'r2': Resistor(value=13000.0),
         'value': Resistor(value=13270.0),
         'relative error': 0.07541478129713425}
    """

    resistor = Resistor(value)
    resistor_list = COMMERCIAL_RESISTORS.E24

    resistor_values = []
    assoc = 0
    for i, r1 in enumerate(resistor_list):
        for r2 in resistor_list[i:]:
            if association_type == "series":
                assoc = r1 + r2
            elif association_type == "parallel":
                assoc = r1 | r2

            relative = relative_error(assoc.value, resistor.value)
            if relative < tolerance / 100:
                resistor_values.append(
                    {"r1": r1, "r2": r2, "value": assoc, "relative error": relative}
                )
    return resistor_values
