from typing import List


class Item(object):
    def __init__(self, name: str, weight: int, value: int) -> None:
        self.name = name
        self.weight = weight
        self.value = value

    def __lt__(self, other: "Item"):
        if self.value == other.value:
            if self.weight == other.weight:
                return self.name < other.name
            else:
                return self.weight < other.weight
        else:
            return self.value < other.value

    def __eq__(self, other: "Item") -> bool:
        if isinstance(other, Item):
            return (self.name == other.name and
                    self.value == other.value and
                    self.weight == other.weight)
        else:
            return False

    def __ne__(self, other: "Item") -> bool:
        return not (self == other)

    def __str__(self) -> str:
        return f'A {self.name} worth {self.value} that weighs {self.weight}'


def get_best_backpack(items: List[Item], max_capacity: int) -> List[Item]:
    sorted_items = sorted(items, key=lambda x: x.value)
    sorted_items2 = sorted(items, key=lambda x: x.value, reverse=True)
    my_bag = []
    my_bag2 = []
    a = _get_best_backpack(sorted_items, max_capacity, my_bag)
    b = _get_best_backpack(sorted_items2, max_capacity, my_bag2)
    a_value = sum([x.value for x in a])
    b_value = sum([x.value for x in b])
    if a_value > b_value:
        return a
    else:
        return b


def _get_best_backpack(items: List[Item], max_capacity: int, bag: List) -> List[Item]:
    if len(items) != 0:
        a = items[-1]
        if max_capacity >= a.weight:
            bag.append(a)
            max_capacity -= a.weight
            items.pop()
            return _get_best_backpack(items, max_capacity, bag)
        else:
            items.pop()
            return _get_best_backpack(items, max_capacity, bag)
    else:
        return bag


items = [Item('0', 43, 43),
         Item('1', 3, 38),
         Item('2', 5, 17),
         Item('3', 18, 25)]

print(str(list(get_best_backpack(items, 100))))
