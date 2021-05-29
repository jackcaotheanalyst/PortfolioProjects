from typing import List


def print_hello() -> None:
    """
    Print Hello
    :return: None
    """
    print('Hello')


def print_list(values: List) -> None:
    """
    Print all of the elements in values, each on their own line
    :param values: the values to print
    :return: None
    """
    for value in values:
        print(value)
