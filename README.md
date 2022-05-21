# Working with the command line from Python

It might be too ambitious a title, but this exercise concerns the basics of writing Python programs that play well with other command line tools.

As we saw first week, there are basically three components to communicating with a command line program: the arguments we give a command, the standard input pipe and the standard output pipe. There is, of course, more options--for example, a command can read data from a file where it receives the file name as an argument, it has a standard error pipe to write error messages to, and there are so-called "environment variables" that it might also use, and even more than this--but these are the basic ones that most tools use. We will write a few programs that use these, and in later projects you will explore it in more details.

## echo

If you call, the `echo` command simply prints its arguments.

```sh
$ echo foo bar baz
foo bar baz
```

We will now write our own `echo`, and there is already a start in the file `src/echo.py`. If you run that program, you get something similar but not quite correct:

```sh
$ python3 src/echo.py foo bar baz
src/echo.py foo bar baz
```

The first thing we will do is fix it so it doesn't print the script name, `src/echo.py`.

If you look at the file you will see that we first import the "system" (`sys`) module

```python
import sys
```

This is where we can get the command's arguments and pipes, and the arguments are in `sys.argv`, which we print with:

```python
print(' '.join(sys.argv))
```

There are a few things to unpack here, and if it gets complicated I promise you that it will be second nature for you to unpack this in a few weeks.  First, the `sys.argv` is a list that contains all the arguments. If you print it with `print(sys.argv)` this should be clear.

```python
import sys

print(sys.argv)
```

will print the list the way we are used to.

```sh
$ python3 src/echo.py foo bar baz
['src/echo.py', 'foo', 'bar', 'baz']
```

What is `print()` doing, then? Well, it prints! (Ask a silly question and you get a silly answer...)

No, there is of course more to it. When you `print()` something you obviously also print it some*where*; you print to a file or the terminal or something. By default, `print()` prints to standard output, and that is why the command prints the result so you can see it. You can use `print()` to print to other files or pipes, the standard output is just the default, and this is the typical way we print to standard output.

So, `sys.argv` has the list of arguments and `print()` will print to standard output, but if we print the list we get output that looks like a list. We want the output as a space-separated string of arguments and that is what the `' '.join(...)` does. If you have a list of strings, you can join them into a single string with a separator between them using `sep.join(x)`; the result is all the strings in `x` concatenated with `sep` between them.

So that is what `print(' '.join(sys.argv))` is doing--it takes all the strings in `sys.argv`, concatenates them with a space between them, and then prints the result (to the standard output).

The problem is the first element in the list, `src/echo.py`. That is not an argument we give the command but the name of the Python script itself. In general, what commands get as arguments is a list of arguments but the first one, the argument at index zero, `sys.argv[0]`, is the name of the program itself. I don't know why the UNIX people decided to make it that way (but it has its usage in very rare cases), but it is what it is.

**Exercise:** To make a proper `echo` command, remove the first element of the `sys.argv` and print the rest.

If you read `man echo` you will see that the command takes a few options. We are not going to implement all of them, don't worry, but let's try implementing these two. The `-s` option tells `echo` not to put spaces between the arguments when it prints them.

```sh
$ echo -s foo bar baz
foobarbaz
```

The option `-n` tells `echo` not to put a newline after it prints, so we can add something more after that:

```sh
$ echo -n foo ; echo bar ; echo -n baz ; echo qux
foobar
bazqux
```

(the `;` enables me to put multiple commands on the same line, so they are executed in order, and I just used it here so you could actually see that we didn't get a newline after `foo` and `baz`, where we used `-n`).

There are sophisticated modules for parsing command line arguments for you, and we will see one in later projects, but it isn't hard to do ourselves. Here is a simple function that will split arguments that start with a `-` from those that do not:

```python
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
```

Using this, you can get the flags and the arguments with

```python
flags, args = split_args(sys.argv[1:])
```

and you can check if the user provided `-n` with `'-n' in flags` and similarly for `-s`.

If you use the `-s` flag to set the `sep` variable to either `''` or `' '` and the `-n` flag to set the `end` variable to either `''` or `'\n'`, then this call to `print()` should give you the desired behaviour.

```python
print(sep.join(args), end=end)
```

The `echo` command can take both flags in one with `-ns`, but our code cannot. That require a bit more spohistication in parsing, and I won't bother with it here. In any case, there are great modules for handing this and in practise you are better off using those. We will see my favorite in a few weeks.

