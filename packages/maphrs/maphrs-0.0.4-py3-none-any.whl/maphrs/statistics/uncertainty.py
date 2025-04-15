from typing import Union
from maphrs.statistics.descriptive import sqrt, standard_deviation

Number = Union[int, float]

def uncertainty_a(values: list[Number]):
    std = standard_deviation(values)
    return std / sqrt(len(values))


def uncertainty_c(values: list[Number], instrument_uncertainty: float):
    return sqrt(uncertainty_a(values) ** 2 + instrument_uncertainty ** 2)
