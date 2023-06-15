from pytest import raises
from project import (
    Secure,
    Username,
    Password,
    generate_username,
    generate_password,
    generate_shuffle,
)


def test_Secure():
    """Test the superclass of both Username and Password"""
    """ 
        def __init__(self, uppercase: str, lowercase: str, numbers: int, **kwargs):
            self.uppercase = uppercase.strip().upper()
            self.lowercase = lowercase.strip().lower()
            self.numbers = numbers
    """

    # Test unpacking
    Secure(*["a", "b", 1])
    Secure(*["asdasds", "asdasd", 1312])

    with raises(TypeError):
        Secure()
        Secure("a", "b")
        Secure("b", True)
        Secure("a" * 3)
        Secure("a", 1)
        Secure("1" * 3)
        Secure("2", "b")
        Secure("a", "b", 1, 123, 123, 123)

    with raises(AttributeError):
        Secure(1, "b", 1)
        Secure(None, [], {})
        Secure("", 1, {})
        Secure(set(), [], -1)
        Secure(True, dict(), -2 - 2)
        Secure("a", False, 1)
        Secure("a", "b", True)
        Secure(*[1, 1, 1])
        Secure(*["a", "b", -1])
        Secure(*[True, True, True])
        Secure("2", "2", 1)


def test_Secure_uppercase():
    """Test uppercase getter and setter"""
    s = Secure("a", "b", 1)
    assert s.uppercase == "A"
    s.uppercase = "abcd"
    assert s.uppercase == "ABCD"
    s = Secure("AbC", "BNM", 123)
    assert s.uppercase == "ABC"

    with raises(ValueError):
        Secure("", "b", 123)
        Secure(None, "a", 123)
        Secure("      ", "b", 123)
        Secure("   ", "b", 123)
        Secure("     ", "b", 123)
        Secure("        ", "b", 123)


def test_Secure_lowercase():
    """Test lowercase getter and setter"""
    s = Secure("a", "b", 1)
    assert s.lowercase == "b"
    s.lowercase = "VBN"
    assert s.lowercase == "vbn"
    s = Secure("AbC", "BNM", 123)
    assert s.lowercase == "bnm"

    with raises(ValueError):
        Secure("a", "", 123)
        Secure("a", "     ", 123)
        Secure("a", "   ", 123)
        Secure("a", None, 123)
        Secure("a", "       ", 123)
        Secure("a", set(), 123)
        Secure("a", 0, 123)
        Secure("a", "1", 123)


def test_Secure_numbers():
    """Test numbers getter and setter"""
    s = Secure("a", "b", 1)
    assert s.numbers == 1
    s.numbers = 123123
    assert s.numbers == 123123
    s = Secure("AbC", "BNM", 123)
    assert s.numbers == 123

    with raises(ValueError):
        Secure("a", "b", -1)
        Secure("a", "b", "-1")
        Secure("a", "b", "1")
        Secure("a", "b", 0)
        Secure("a", "b", -123 - 123)
        Secure("a", "b", "asdasd")
        Secure("a", "b", None)


def test_Username():
    """Test the class generating usernames"""

    s = Username("a", "b", 1, check=True)
    username = s.username
    assert len(username) == 6
    assert "_" in username
    assert username.count("_") == 1

    s = Username("aaa", "bbbb", 1)
    username = s.username
    assert len(username) == 8
    assert "_" not in username
    assert username.count("A") == 3
    assert username.count("b") == 4
    assert username.count("1") == 1

    s = Username("a", "aasd", 123, check=True)
    username = s.username
    assert len(username) == 9
    assert "_" in username
    assert username.count("A") == 1
    assert username.count("a") == 2
    assert username.count("s") == 1
    assert username.count("d") == 1
    assert username.count("123") == 0
    assert username.count("1") == 1
    assert username.count("2") == 1
    assert username.count("3") == 1

    with raises(TypeError):
        s.username = 0
        s.username = None

    with raises(ValueError):
        s.username = ""
        s.username = set()
        s.username = {}
        s.username = []


def test_Password():
    """Test the class generating passwords"""
    # check = True
    punctuation = "?!.:"

    # check_special = True
    special = "*-/$%@_"

    s = Password("a", "b", 1, check=True)
    password = s.password
    assert len(password) == 12
    for c in punctuation:
        assert c in password

    s = Password("a", "b", 2, check_special=True)
    password = s.password
    assert len(password) == 12
    for c in special:
        assert c in password

    s = Password("aaa", "bbbb", 1, check=True, check_special=True)
    password = s.password
    assert len(password) == 8 + len(punctuation) + len(special)
    assert password.count("A") == 3
    assert password.count("b") == 4
    assert password.count("1") == 1

    for c in special:
        assert c in password

    for c in punctuation:
        assert c in password

    s = Password("gggggggg", "aasd", 123, check=True)
    password = s.password
    assert len(password) == 15 + len(punctuation)
    assert password.count("G") == 8
    assert password.count("a") == 2
    assert password.count("s") == 1
    assert password.count("d") == 1
    assert password.count("1") == 1
    assert password.count("2") == 1
    assert password.count("3") == 1

    for c in punctuation:
        assert c in password

    with raises(TypeError):
        s.password = 0
        s.password = None

    with raises(ValueError):
        s.password = ""
        s.password = set()
        s.password = {}
        s.password = []


""" 
    Functions generate_username, generate_password, and generate_shuffle, 
    require user's attention and interaction
"""


def test_generate_username():
    """Test the function that prompts the user to
    specify wether they want underscore in username or not,
    which then tries to instantiate the Username class,
    and returns True on success
    """
    """ 
        def generate_username(
            uppercase: str, 
            lowercase: str, 
            numbers: int, 
            amount: int, 
            **kwargs
        ) -> bool:
    """
    # Test valid
    assert generate_username("a", "b", 1, 1, check=True) == True
    assert generate_username("aasdasd", "basdsad", 123, 2, check=True) == True
    assert generate_username("ASDASDASDasdsaDAS", "bSADAS", 2, 5, check=False) == True
    assert generate_username("a", "b", 1, 1, check=False) == True
    assert generate_username("   aasads   ", "asdads     ", 1, 1, check=False) == True
    assert generate_username("a", "b", 1, 1, check=True) == True

    with raises(ValueError):
        generate_username(
            "   aasads123123.,/.,/.  ", "2341234sadffdalll    ", 1, 1, check=False
        )
        generate_username("   aasad  ", "asdasd    ", 1, -1, check=True)
        generate_username("654654654", "46546464654", 1, -1, check=True)
        generate_username("", "", "", "", check="")


def test_generate_password():
    """Test the function that prompts the user to
    specify wether they want special characters and/or punctuation in password or not,
    which then tries to instantiate the Password class,
    and returns True on success
    """
    assert generate_password("a", "b", 1, 1, check=True, check_special=True) == True
    assert (
        generate_password("aasdasd", "basdsad", 123, 2, check=True, check_special=True)
        == True
    )
    assert (
        generate_password(
            "ASDASDASDasdsaDAS", "bSADAS", 2, 5, check=False, check_special=True
        )
        == True
    )
    assert generate_password("a", "b", 1, 1, check=False, check_special=False) == True
    assert (
        generate_password(
            "   aasads   ", "asdads     ", 1, 1, check=False, check_special=True
        )
        == True
    )
    assert generate_password("a", "b", 1, 1, check=True, check_special=0) == True
    assert generate_password("a", "b", 1, 1, check=True, check_special=None) == True

    with raises(ValueError):
        generate_password(
            "   aasads123123.,/.,/.  ",
            "2341234sadffdalll    ",
            1,
            1,
            check=False,
            check_special=0,
        )
        generate_password(
            "   aasad  ", "asdasd    ", 1, -1, check=True, check_special=0
        )
        generate_password(
            "654654654", "46546464654", 1, -1, check=True, check_special=0
        )
        generate_password("", "", "", "", check="", check_special=-112121212)


def test_generate_shuffle():
    """Test the function shuffling the string provided by the user"""
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True
    assert generate_shuffle("asdasd-09as-0d9as0-ddasdas") == True

    with raises(ValueError):
        generate_shuffle(12312312)
        generate_shuffle(None)
        generate_shuffle(set())
        generate_shuffle(list())
        generate_shuffle(dict())
