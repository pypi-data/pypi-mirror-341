import typing


def unique(iterable: typing.Iterable[typing.Any]) -> typing.List[typing.Any]:
    seen = set()
    return [item for item in iterable if not (item in seen or seen.add(item))]


def flatten(iterable: typing.Iterable[typing.Any]) -> typing.List[typing.Any]:
    array = []
    for item in iterable:
        if isinstance(item, (list, tuple)):
            array.extend(flatten(item))
        else:
            array.append(item)
    return array


def filter(iterable: typing.Iterable[typing.Any], expression: typing.Callable) -> typing.List[typing.Any]:
    return [item for item in iterable if expression(item)]


def sort(
    iterable: typing.Iterable[typing.Any], key: typing.Any = None, reverse: bool = False
) -> typing.List[typing.Any]:
    return sorted(iterable, key=key, reverse=reverse)


def first(iterable: typing.Iterable[typing.Any]) -> typing.Any:
    return next(iter(iterable))


def last(iterable: typing.Iterable[typing.Any]) -> typing.Any:
    return iterable[-1]


def reverse(iterable: typing.Iterable[typing.Any]) -> typing.List[typing.Any]:
    return list(iterable)[::-1]
