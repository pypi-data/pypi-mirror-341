# arpakit

from typing import Optional, Any

import markdown
from bs4 import BeautifulSoup

from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def str_in(string: str, main_string: str, *, max_diff: Optional[int] = None) -> bool:
    if string not in main_string:
        return False

    if max_diff is None:
        return True

    diff = len(main_string) - len(string)
    if diff <= max_diff:
        return True

    return False


def bidirectional_str_in(string1: str, string2: str, *, max_diff: Optional[int] = None) -> bool:
    if (
            str_in(string=string1, main_string=string2, max_diff=max_diff)
            or str_in(string=string2, main_string=string1, max_diff=max_diff)
    ):
        return True
    return False


def str_startswith(string: str, main_string: str, max_diff: Optional[int] = None) -> bool:
    if not main_string.startswith(string):
        return False

    if max_diff is None:
        return True

    diff = len(main_string) - len(string)
    if diff <= max_diff:
        return True

    return False


def bidirectional_str_startswith(string1: str, string2: str, max_diff: Optional[int] = None) -> bool:
    if str_startswith(string1, string2, max_diff=max_diff) or str_startswith(string2, string1, max_diff=max_diff):
        return True
    return False


def make_blank_if_none(string: Optional[str] = None) -> str:
    if string is None:
        return ""
    return string


def make_none_if_blank(string: Optional[str] = None) -> str | None:
    if not string:
        return None
    return string


def strip_or_make_none_if_blank(string: Optional[str] = None) -> str | None:
    if string is None:
        return None
    string = string.strip()
    if not string:
        return None
    return string


def none_if_blank(string: Optional[str] = None) -> str | None:
    return make_none_if_blank(string=string)


def lower_and_strip_if_not_none(string: str | None) -> str | None:
    if string is None:
        return None
    return string.lower().strip()


def remove_html(string: str) -> str:
    raise_for_type(string, str)
    return BeautifulSoup(string, "html.parser").text


def remove_markdown(text: str) -> str:
    html_text = markdown.markdown(text)
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def remove_tags(string: str) -> str:
    raise_for_type(string, str)
    return string.replace("<", "").replace(">", "")


def remove_tags_and_html(string: str) -> str:
    raise_for_type(string, str)
    return remove_tags(remove_html(string))


def raise_if_string_blank(string: str) -> str:
    if not string:
        raise ValueError("not string")
    return string


def return_str_if_none(value: str | None, value_str: str) -> str:
    if value is None:
        return value_str
    return value


def strip_if_not_none(v: str | None) -> str | None:
    if v is None:
        return v
    return v.strip()


def strip_or_none(value: Any):
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        return value
    return None


def lower_and_strip_or_none(value: Any) -> str | None:
    value = strip_or_none(value)
    if isinstance(value, str):
        return value.lower().strip()
    return None


def int_or_float_or_none(value: Any) -> float | int | None:
    if isinstance(value, float) or isinstance(value, int):
        return value
    value = strip_or_none(value)
    if value is not None and value.isdigit():
        return int(value)
    if value is not None and value.isdecimal():
        return float(value)
    return None


def int_or_none(value: Any) -> int | None:
    if isinstance(value, int):
        return value
    value = strip_or_none(value)
    if value is not None and value.isdigit():
        return int(value)
    return None


def float_or_none(value: Any) -> float | None:
    if isinstance(value, float):
        return value
    value = strip_or_none(value)
    if value is not None and value.isdecimal():
        return float(value)
    return None


def __example():
    print(int_or_none("124.124"))

    print("str_in:")
    print(str_in(string="hello", main_string="hello world"))
    print(str_in(string="bye", main_string="hello world"))
    print(str_in(string="hello", main_string="hello world", max_diff=6))
    print(str_in(string="hello", main_string="hello world", max_diff=1))

    print("\nbidirectional_str_in:")
    print(bidirectional_str_in(string1="hello", string2="hello world"))
    print(bidirectional_str_in(string1="world", string2="hello world"))

    print("\nstr_startswith:")
    print(str_startswith(string="hello", main_string="hello world"))
    print(str_startswith(string="world", main_string="hello world"))

    print("\nbidirectional_str_startswith:")
    print(bidirectional_str_startswith(string1="hello", string2="hello world"))
    print(bidirectional_str_startswith(string1="world", string2="hello world"))

    print("\nmake blank_if_none:")
    print(make_blank_if_none())
    print(make_blank_if_none(string="test"))

    print("\nremove_html:")
    print(remove_html(string="<div>Hello <b>World</b></div>"))

    print("\nremove_tags:")
    print(remove_tags(string="<div>Hello <b>World</b></div>"))

    print("\nremove_tags_and_html:")
    print(remove_tags_and_html("<div>Hello <b>World</b></div>"))

    print(remove_markdown("# Тут обычный текст с **жирным** и *курсивным* выделением."))


if __name__ == '__main__':
    __example()
