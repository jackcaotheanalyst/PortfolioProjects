from typing import List


class Donor(object):
    """
    Maybe it would be a good idea to a make a simple donor class
    """
    instances: List["Donor"] = []

    def __init__(self, name: str, amount: int) -> None:
        self.name = name
        self.amount = amount
        Donor.instances.append(self)

    @staticmethod
    def create_from_file(path_to_file: str) -> None:
        with open(path_to_file) as config_file:
            config = {}
            for line in config_file:
                line = line.strip()
                if line:
                    name, amount = line.split(':')
                    name = name.strip()
                    amount = amount.strip()
                    try:
                        amount_int = int(amount)
                    except ValueError:
                        pass
                    config[name] = amount_int
            for key in config:
                Donor(key, config[key])

    def __str__(self) -> str:
        return f"{self.name}  with a donation of {self.amount}"
