import random


def build_donors(num_donors: int, min_donation: int, max_donation: int, result_path: str) -> None:
    """

    :param num_donors: How many donors
    :param min_donation: The minimum donation amount
    :param max_donation: The maximum donation amount
    :param result_path:  The place to put the resulting file
    :return:
    """
    donors = list(range(num_donors))
    random.shuffle(donors)
    with open(result_path, 'w') as result_file:
        for donor in donors:
            donation = random.randint(min_donation, max_donation)
            line = f'{donor} : {donation}\n'
            result_file.write(line)


def main() -> None:
    """
    You can use this program to build a sample donor files for you
    to test against. Just change the path of the file to where you
    want the file to end up at
    :return:
    """
    build_donors(10, 10, 10000, './donor_files/donor10.txt')


if __name__ == '__main__':
    main()
