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

**Exercise:** If you use the `-s` flag to set the `sep` variable to either `''` or `' '` and the `-n` flag to set the `end` variable to either `''` or `'\n'`, then this call to `print()` should give you the desired behaviour.

```python
print(sep.join(args), end=end)
```

The `echo` command can take both flags in one with `-ns`, but our code cannot. That require a bit more spohistication in parsing, and I won't bother with it here. In any case, there are great modules for handing this and in practise you are better off using those. We will see my favorite in a few weeks.

## ed

For our next excercise we will implement our own editor! That sounds scary, but don't fret, we are going to implement `ed`.

```sh
$ python3 src/ed.py

?
help
?
?
?
quit
?
exit
?
bye
?
hello?
?
```

If you have the actual `ed` on your machine, you can check that this is not made-up behavoiur; this is how it works.

```sh
$ ed

?
help
?
?
?
quit
?
exit
?
bye
?
hello?
?
```

(it will be easier to get out of our Python implementation than the real thing, though).

[The `ed` editor](https://www.gnu.org/fun/jokes/ed-msg.en.html) is one of the oldest interactive source code editors, and has personality, to put it mildly. A rather unpleasant personality. And most people's only experience with `ed` is trying to get it to do *anything* besides printing `?` for every line you give it. If we write a program that does that, we should be able to fool 99% of users into thinking they are running the real `ed`.

To achieve this, we need two things: we need to be able to read a line from the standard input, and we need to print `?` to the standard output. And we need to do this forever. That's it. That is why `ed` has such a small memory footprint.

We already know how to make an infinite loop with `while True:` and we already know how to write to standard output with `print()` so all we need to figure out is how to read a line from standard input. The good people who wrote Python chose the name for that function well, it is `input()`.

When you call `input()` it will wait until it can get a line from standard input--if that is a file it can get it right away, but otherwise it needs to wait for the user to type it--and then it will return the input sans the newline.

**Exercise:** Try to implement `src/ed.py` using a `while True:` loop that waits for input with `input()`, ignores the actual input, and prints `?`.

**Exercise:** Although it hardly seems possible, maybe we can improve on `ed`. Change your code such that if the user types `eat flaming death`, the loop terminates (you can use `break` to make the suffering end).

## cat

The `cat` command concatenates a number of files and prints them to standard output. We are going to implement that now. First, let's make a very simple version:

```python
import sys

for line in sys.stdin:
    print(line)
```

In the `for` loop here, we run through `sys.stdin`. What is that doing? Well, for any file, if you try to loop through it, you get each line in turn. The standard input pipe/file is found in `sys.stdin` and the `for` loop runs through each line in it, and we print it.

If you run this code, catting itself, it doesn't look quite right:

```sh
$ cat src/cat.py | python3 src/cat.py
import sys



for line in sys.stdin:

    print(line)

```

There is an extra newline in the output for each line in the input. That is because the `line` you get in the loop contains the newline character for that line, `'\n'`. When we used `input()` we didn't get it, but the `input()` function is more intended for interactive use and this is the general way you run through files, and here the newline character remains.

**Exercise:** If the line already has a newline, `print()` shouldn't add it. Remove it the way you did in the `echo` exercise.

If you are wondering, the standard output file is also found in `sys` and is called `sys.stdout`. We don't need it here, because `print()` uses it by default, but we could make it explicit with `print(line, file=sys.stdout)`.

The real `cat` only reads from `stdin` if we don't provide any arguments. If it gets arguments, it considers them a list of files to open and print in turn. Here's a simple program that does that:

```python
import sys

args = sys.argv[1:]  # get all command line arguments
if args:  # if args is not empty
    for fname in args:
        with open(fname) as f:
            print(f.read(), end='')
else:
    print(sys.stdin.read(), end='')
```

Here, we use the `.read()` method on files or `stdin`; it reads the entire content of a file, and we print that. This is not space efficient, though, because we read the entire content of the file in before we print it.

**Exercise:** Change this code so we read and print a line at a time.

The special case of some files or none can be made a little nicer on a UNIX system, where we can just add the file name for `stdin` to the arguments if the argument list is empty

```python
args = sys.argv[1:]
if not args:
    args.append('/dev/stdin')

for arg in args:
    with open(arg) as f:
        print(f.read(), sep='')
```

This works because UNIX knows that the `/dev/stdin` file isn't a real file but one that refers to the standard input. That being said, though, modules that can handle options for you will typically take care of special cases such as this when you need them to.

The real `cat` command has an option, `-n`, that you can use to add line numbers to the output.

```sh
$ cat -n src/echo.py
     1	import sys
     2
     3	print(' '.join(sys.argv))
$ cat -n src/cat.py
     1	import sys
     2
     3	for line in sys.stdin:
     4	    print(line)
$ cat -n src/echo.py src/cat.py
     1	import sys
     2
     3	print(' '.join(sys.argv))
     1	import sys
     2
     3	for line in sys.stdin:
     4	    print(line)
```

**Exercise:** Can you add this option? Don't worry about making it look nice or anything, just print the line number in front of each line.

**Exercise:** As you can see in the examples above, the line numbers go back to 1 each time you start a new file. Can you add another option that makes the line numbers go from 1 and upwards, *not* resetting at each new file?

**Exercise:** Assuming we can't do that (but we can!), could you use `cat` itself to get consequtive numbers? Maybe pipe the result of one cat through another...?
