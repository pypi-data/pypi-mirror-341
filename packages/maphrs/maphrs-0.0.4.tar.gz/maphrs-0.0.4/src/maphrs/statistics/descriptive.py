"""
Descriptive statistics refers to the study of the aggregate quantities of a dataset.
These measures are some of the commonly used notations in everyday life.
Some examples of descriptive statistics include average annual income, median home
price in a neighborhood, range of credit scores of a population, etc.
"""

from typing import Literal, Union

Number = Union[int, float]


def root(number: Number, n: int) -> int | float:
    """
    Calculate de nth root of a number.
    :param number: Any integer or float number
    :param n: value of the root
    :returns: the calculated nth root of the number

    Examples:
        >>> square_root = root(10, 2)
        >>> print(square_root)
        3.1622776602

        >>> cubic_root = root(10, 3)
        >>> print(cubic_root)
        2.1544346900

    """
    return number ** (1 / n)


def sqrt(number: Number) -> Number:
    """
    Calculate the square root of a number.
    :param number: Integer or Float number
    :return: calculated square root of the number

    Examples:
        >>> square = sqrt(2)
        >>> print(square)
        1,4142135624
    """
    return root(number, 2)


def mean(values: list[Number]) -> Number:
    """
    Calculate the mean of a list of numbers.
    :param values: list of numbers
    :return: mean of the list of numbers

    Examples:
        >>> values_list = [10,20,30,40]
        >>> values_mean = mean(values_list)
        >>> print(values_mean)
        25
    """
    return sum(values) / len(values)


def standard_deviation(
    values: list[Number], type: Literal["sample", "population"] = "sample"
):
    """
    Calculate the standard deviation of a list of numbers. It's possible to choose wich type
    of standard deviation to calculate, be it 'sample' or 'population'.
    :param values: list of numbers, the list length must be greater or equal to 2
    :param type: choose either "sample" or "population" standard deviation types
    :return: calculated standard deviation of the list of numbers

    Examples:
        >>> values_list = [10,34,23,54,9]
        >>> stdev = standard_deviation(values_list)
        >>> print(stdev)
        18.721645226849056
    """
    if len(values) < 2:
        raise Exception("Minimum length of values need to be 2")

    if type.lower() == "sample":
        std_value = sqrt(
            sum([(xi - mean(values)) ** 2 for xi in values]) / (len(values) - 1)
        )
    elif type.lower() == "population":
        std_value = sqrt(
            sum([(xi - mean(values)) ** 2 for xi in values]) / (len(values))
        )
    else:
        raise ValueError(
            f"'type' must be either 'sample' or 'population', {type} is invalid"
        )

    return std_value


def relative_error(approximate_value: float, real_value: float):
    """
    Calculates the relative error between an approximated value, and it's intended value.

    Let's take an example, where we must calculate the gravity in a physics experiment. We all know
    the real value stands around 9.8 m/s, but the calculated value obtained through experiments
    is 9.62 m/s. To see the relative error between the calculated value and real value:

    >>> calculated = 9.62
    >>> real = 9.80
    >>> error = relative_error(calculated, real)
    >>> print(f"Error in percentage: {error:.2f}%")
    1,83%

    :param approximate_value: calculated number
    :param real_value: expected value
    :return: the relative error between the calculated data and the real value, in percentage

    Examples:
        >>> calculated = 9.62
        >>> real = 9.80
        >>> error = relative_error(calculated, real)
        >>> print(f"Error in percentage: {error:.2f}%")
        1,83%
    """
    return abs(((approximate_value - real_value) / real_value) * 100)
