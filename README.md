# Codeforces Template Tool

I created this tool to help me quickly set up codeforces contests/singular problems with templates.

Tested for windows, should work on linux or any other operating system.

## Installation

Clone the repository with git.

```sh
git clone git@github:com/AnotherTwinkle/cftool.git
```

Now, navigate to the `cftool` directory with and install it with `pip`-

```sh
cd cftool
pip install .
```

Note that Python 3.8 was used to test this script. This should run on 3.4+.

## Usage

After installation, the tool should be available anywhere on your CLI. The script has 4 commands you can use.

### Creating Singular Files

To create a singular file, use this command-

```
cftool problem [filename] [?template]
```

where `template` is optional. Note that the file name must end with an appropriate language file extension.

For example-

```
cftool problem 843A.py fastio
```

The script infers the language from the filename and searches for the template file in the directory `templates/{lang}/` directory. Then, it creates a file called `[filename]`in the current working directory and pastes the template code for you to use.

If the template language directory or the template file doesn't exist, `[filename]` will be empty on creation.

If you don't provide the `template` argument, the script will use the `default` template in the language directory.

### Creating a directory for a singular problem

If you'd like to be organized and have invidiual directories for each solution you write, you can use the `problemdir` command.

```
cftool problemdir [name] [language] [?template] [?--notes]
```

Note how you need to explicitly state the language. More precisely, you are telling the script to look for the `[language]` directory in `templates/`.

```
cftool problemdir 433A cpp fastio --notes
```

This will create a directory called `433A` and intialize a file called `sol.cpp` with the `fastio` template for C++ in there.

`template` is still optional. The `--notes` flag, if provided, will create a file called `notes.txt` in the directory.

### Creating a contest directory

This is peharps the only reason I wrote this script.

```
cftool contest [name] [language] [problemcount] [?template] [?--notes]
```

This commands creates a codeforces contest directory. The command syntax is almost simillar to `problemdir` with the added `problemcount` argument. 

```
cftool contest 768DivA cpp 6 fastio --notes
```

This creates a directory called `768DivA` and, following codeforces naming scheme, puts 6 files named `A, B, C, D, E, F` (from `A` to the `problemcount`-th letter of the alphabet) respectively. `problemcount` cannot exceed 26.

The directory name can have multiple words, in that case you put quotes around the name.

```
cftool contest "696 Div B" py 5 default --notes
```

This command also supports exclusion of the `template` argument and `--notes` flag.

### Creating a contest directory with problem directories

This command has the same syntax as `contest`, but instead of creating files, it creates a directory for each problem, each having a file called `sol`.

```
cftool contestwpdir "593 Div 3" cpp 8 fastio --notes
```

Note: The command name is shorthand for `contest with problem directory`, this should help you remember the name.

## Adding your own templates

If you have a better, or a personal template you'd like to use, you can do so.

First, create a new directory in the `templates/` directory of the script. The name of this directory **must** be the file extension your language uses. i.e `py`, `cpp`, `js` etc. There already are some premade directories.

Next, create a file called `default` in the directory with your language extension (i.e `default.cpp` or `default.py`). This is template used by the script when the `template` argument is not provided. You can leave this file empty if you want.

Now to add a template, create a file with the desired name (The language extension must be included with filename)

Once you are done, you need to reinstall the script. Navigate to the directory with the `setup.py` file and run-

```
pip install .
```

If all went well you should be able to access the template now, i.e-

```
cftool problem test.java myshinyjavatemplate
```

## Executable?

I plan making a the script a binary executable in the future, so you don't need python installed to run it.

## Contributing

It'd be greatly appreciated if you PR useful templates to the project. If you use the script, consider starring it so more people can find it.

