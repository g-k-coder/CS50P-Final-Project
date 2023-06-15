import csv
import sys
from datetime import datetime, timedelta, timezone
import random
import argparse
import re
from colorama import Fore


class Secure:
    def __init__(self, uppercase: str, lowercase: str, numbers: int, **kwargs):
        self.uppercase = uppercase.strip().upper()
        self.lowercase = lowercase.strip().lower()
        self.numbers = numbers

    @property
    def lowercase(self) -> str:
        return self._lowercase

    @lowercase.setter
    def lowercase(self, s: str):
        if not len(s) or type(s) != str or not s.isalpha():
            raise ValueError(
                "\n\n*** LOWERCASE must be a string of at least one(1) letter and containing only letters ***\n"
            )
        self._lowercase = s.strip().lower()

    @property
    def uppercase(self) -> str:
        return self._uppercase

    @uppercase.setter
    def uppercase(self, s: str):
        if not len(s) or type(s) != str or not s.isalpha():
            raise ValueError(
                "\n\n*** UPPERCASE must be a string of at least one(1) letter and containing only letters ***\n"
            )

        self._uppercase = s.strip().upper()

    @property
    def numbers(self) -> int:
        return self._numbers

    @numbers.setter
    def numbers(self, s: int):
        if type(s) != int or s < 0:
            raise ValueError(
                "\n\n*** NUMBERS must be an integer containing at least one(1) digit and containing only positive integer ***\n"
            )

        self._numbers = s


class Username(Secure):
    def __init__(
        self,
        uppercase: str,
        lowercase: str,
        numbers: int,
        underscore: str = "_",
        check=False,
        **kwargs,
    ):
        # Remove the spaces within a string
        uppercase = re.subn(" ", "", uppercase)[0]
        lowercase = re.subn(" ", "", lowercase)[0]

        super().__init__(uppercase, lowercase, numbers)
        default = self.uppercase + self.lowercase + str(self.numbers)
        self.username = default + underscore if check == True else default

    # Getter
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, s: str):
        # Remove the spaces within a string
        s = re.subn(" ", "", s)[0]

        has_number = any(m.isdigit() for m in s)
        has_upper = any(m.isupper() for m in s)
        has_lower = any(m.islower() for m in s)

        if type(s) != str or not has_number or not has_upper or not has_lower:
            raise ValueError(
                "Username must be a string including at least one(1) lowercase letter, one(1) upppercase letter, and one(1) integer"
            )
        elif len(s) < 6:
            s = s * len(s)
            s = s[:6]
        self._username = "".join(random.sample(s, len(s)))

    def __str__(self):
        time_format = datetime.now(tz=timezone(timedelta(hours=0))).strftime(
            "%H:%M:%S UTC - %d/%m/%Y"
        )

        with open("generator-log.txt", "a") as file:
            writer = csv.writer(file)
            writer.writerow([f"USERNAME {self.username} generated at {time_format}"])

        return f"USERNAME {Fore.GREEN + self.username}{Fore.RESET} generated at {time_format}"


class Password(Secure):
    def __init__(
        self,
        uppercase: str,
        lowercase: str,
        numbers: int,
        length: int = 12,
        symbols="*-/$%@_",
        punctuation="?!.:",
        check=False,
        check_special=False,
        **kwargs,
    ):
        # Remove the spaces within a string
        uppercase = re.subn(" ", "", uppercase)[0]
        lowercase = re.subn(" ", "", lowercase)[0]

        super().__init__(uppercase, lowercase, numbers)
        self.length: int = length
        default = self.uppercase + self.lowercase + str(self.numbers)
        self.password = (
            default + symbols + punctuation
            if check and check_special
            else default + symbols
            if check_special
            else default + punctuation
            if check
            else default
        )

    # Getter
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, s: str):
        # Remove the spaces within a string
        s = re.subn(" ", "", s)[0]

        has_number = any(m.isdigit() for m in s)
        has_upper = any(m.isupper() for m in s)
        has_lower = any(m.islower() for m in s)

        if type(s) != str or not has_number or not has_upper or not has_lower:
            raise ValueError(
                "Password must be a string including at least one(1) lowercase letter, one(1) upppercase letter, and one(1) integer"
            )
        elif len(s) < 12:
            s = s * len(s)
            s = s[:12]
        self._password = "".join(random.sample(s, len(s)))

    def __str__(self):
        time_format = datetime.now(tz=timezone(timedelta(hours=0))).strftime(
            "%H:%M:%S UTC - %d/%m/%Y"
        )

        with open("generator-log.txt", "a") as file:
            writer = csv.writer(file)
            writer.writerow([f"PASSWORD {self.password} generated at {time_format}"])

        return f"PASSWORD {Fore.GREEN + self.password}{Fore.RESET} generated at {time_format}"


def main():
    parser = argparse.ArgumentParser(
        prog="project.py",
        description="Generate random username and password\n",
    )

    parser.add_argument(
        "-m",
        "--mode",
        help="choose between the modes of username and password",
        type=str,
        required=True,
        choices=["username", "password", "shuffle"],
    )
    parser.add_argument(
        "-a",
        "--amount",
        help="amount of output samples to generate",
        type=int,
        default=1,
    )

    # Only applicable in shuffle mode
    parser.add_argument(
        "-t",
        "--text",
        help="string to shuffle",
        type=str,
    )

    args = parser.parse_args()

    try:
        mode = args.m
    except AttributeError:
        mode = args.mode

    try:
        amount = args.a
    except AttributeError:
        amount = args.amount

    try:
        pattern = args.t
    except AttributeError:
        pattern = args.text

    while True:
        try:
            if mode == "shuffle":
                try:
                    if pattern is None or not len(pattern):
                        raise ValueError()

                    for _ in range(amount):
                        generate_shuffle(pattern)
                except ValueError:
                    print(
                        "When setting the mode to shuffle,  -t/--text [TEXT] is required."
                    )
                    return
            else:
                numbers = int(input("NUMBERS -> int: ").strip())
                uppercase = input("UPPERCASE -> str: ").strip().upper()
                lowercase = input("LOWERCASE -> str: ").strip().lower()

                # Remove the spaces within a string
                uppercase = re.subn(" ", "", uppercase)[0]
                lowercase = re.subn(" ", "", lowercase)[0]

                if mode == "username":
                    generate_username(uppercase, lowercase, numbers, amount)
                elif mode == "password":
                    generate_password(uppercase, lowercase, numbers, amount)

            break
        except (EOFError, KeyboardInterrupt):
            sys.exit()
        except ValueError:
            print(
                "\n\tNUMBERS must be an integer containing at least one(1) digit and containing only positive integer\n",
                "\tUPPERCASE must be a string of at least one(1) letter and containing only letters\n",
                "\tLOWERCASE must be a string of at least one(1) letter and containing only letters\n",
            )


def generate_username(
    uppercase: str, lowercase: str, numbers: int, amount: int, **kwargs
) -> bool:
    """Generate usernames and print them

    :param uppercase: letters to be converted to uppercase
    :type: str

    :param lowercase: letters to be converted to lowercase
    :type: str

    :param numbers: numbers to implement in username
    :type: int

    :param amount: amount of samples to create and print
    :type: int

    :return: Indicate success
    :rtype: bool
    """
    # Remove the spaces within a string
    uppercase = re.subn(" ", "", uppercase)[0]
    lowercase = re.subn(" ", "", lowercase)[0]

    if "check" not in kwargs.keys():
        check = (
            True
            if input("Include underscore? [y/N]: ").strip().lower() in ("y", "yes")
            else False
        )
    else:
        check = True if kwargs["check"] else False

    print("---------------------------------")

    for _ in range(amount):
        s = Username(
            uppercase,
            lowercase,
            numbers,
            check=check,
            check_special=False,
        )
        print(s)

    return True


def generate_password(
    uppercase: str, lowercase: str, numbers: int, amount: int, **kwargs
) -> bool:
    """Generate passwords and print them

    :param uppercase: letters to be converted to uppercase
    :type: str

    :param lowercase: letters to be converted to lowercase
    :type: str

    :param numbers: numbers to implement in username
    :type: int

    :param amount: amount of samples to create and print
    :type: int

    :return: Indicate success
    :rtype: bool
    """
    # Remove the spaces within a string
    uppercase = re.subn(" ", "", uppercase)[0]
    lowercase = re.subn(" ", "", lowercase)[0]

    if "check" not in kwargs.keys():
        check = (
            True
            if input("Include punctuation? [y/N]: ").strip().lower() in ("y", "yes")
            else False
        )
    else:
        check = True if kwargs["check"] == True else False

    if "check_special" not in kwargs.keys():
        check_special = (
            True
            if input("Include special characters? [y/N]: ").strip().lower()
            in ("y", "yes")
            else False
        )
    else:
        check_special = True if kwargs["check_special"] else False

    print("---------------------------------")

    for _ in range(amount):
        s = Password(
            uppercase,
            lowercase,
            numbers,
            check=check,
            check_special=check_special,
        )
        print(s)

    return True


def generate_shuffle(pattern: str) -> bool:
    """Shuffle text and print it

    :param pattern: text to shuffle
    :type: str

    :return: Indicate success
    :rtype: bool
    """
    if type(pattern) != str:
        raise ValueError("Pattern must be a string")

    # Remove the spaces within the pattern
    re.sub(" ", "", pattern)

    time_format = datetime.now(tz=timezone(timedelta(hours=0))).strftime(
        "%H:%M:%S UTC - %d/%m/%Y"
    )
    shuffle = "".join(random.sample(pattern, len(pattern)))

    with open("generator-log.txt", "a") as file:
        writer = csv.writer(file)
        writer.writerow([f"TEXT {shuffle} shuffled at {time_format}"])

    print(f"TEXT {Fore.GREEN + shuffle}{Fore.RESET} shuffled at {time_format}")

    return True


if __name__ == "__main__":
    main()
