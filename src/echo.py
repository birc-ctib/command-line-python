import sys

print(' '.join(sys.argv))


def split_args(args: list[str]) -> tuple[list[str], list[str]]:
    """
    Split argv and return the flags separated from the rest.

    >>> split_args(['-n', 'foo', 'bar'])
    (['-n'], ['foo', 'bar'])
    >>> split_args(['-n', 'foo', '-s', 'bar'])
    (['-n', '-s'], ['foo', 'bar'])
    """
    flags, rest = [], []
    for arg in args:
        if arg.startswith('-'):
            flags.append(arg)
        else:
            rest.append(arg)
    return flags, rest


flags, args = split_args(sys.argv[1:])
sep = '' if '-s' in flags else ' '
end = '' if '-n' in flags else '\n'
print(sep.join(args), end=end)
