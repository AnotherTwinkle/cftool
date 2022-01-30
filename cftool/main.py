#!usr/bin/env python
import sys
import os

def get_template_code(lang, template):
    l = __file__.split(os.path.sep)
    del l[-1]
    if os.name == 'nt':
        l[0] = l[0] + os.path.sep

    td = os.path.join(*l, "templates", lang, f'{template}.{lang}')

    if os.path.exists(td):
        f = open(td, 'r')
        code = f.read()
        f.close()
    else:
        code = ''

    return code

def makenotesfile(directory):
    with open(os.path.join(directory, 'notes.txt'), 'w') as f:
        f.write('')

def problem(file, directory, template):
    """Create a single file with given template."""

    lang = file.split('.')[-1]
    code = get_template_code(lang, template)

    with open(os.path.join(directory, file), 'w') as f:
        f.write(code)

def problemdir(name, directory, lang, template, notes = False):
    """Put the solution file in a directory, add a notes.txt optionally"""
    directory = os.path.join(directory, name)
    os.mkdir(directory)
    problem(f'sol.{lang}', directory, template)
    if notes:
        makenotesfile(directory)
    
def contest(name, directory, lang, problemcount, template, notes = False):
    """Create a directory, and create an file for each invidiual solution (Follows codeforces naming scheme)"""

    import string
    directory = os.path.join(directory, name)
    os.mkdir(directory)
    for i in range(problemcount):
        problem(f'{string.ascii_uppercase[i]}.{lang}', directory, template)

    if notes:
        makenotesfile(directory)

def contestwpdir(name, directory, lang, problemcount, template, notes = False):
    """Same as contest, however a new directory is created for each solution file"""

    import string
    directory = os.path.join(directory, name)
    os.mkdir(directory)
    for i in range(problemcount):
        s = string.ascii_uppercase[i]
        problemdir(s, directory, lang, template)

    if notes:
        makenotesfile(directory)

def get(l, i, d):
    try:
        return l[i]
    except IndexError:
        return d

def main(): 
    n = 1
    target = get(sys.argv, n, None)
    directory = os.getcwd()
    
    # TODO: Make the following code less repetitive.
    if target == 'problem':
        # prog contest [file] ?[template]
        file = sys.argv[n + 1]
        template = get(sys.argv, n + 2, 'default')

        problem(file, directory, template)

    elif target == 'problemdir':
        # prog contest [name] [lang] ?[template] ?[--notes]
        name = sys.argv[n + 1]
        lang = sys.argv[n + 2]
        template = get(sys.argv, n + 3, 'default')
        if template == '--notes': # We're doing a bit of hack here to make template optional.
            notes = True
            template = 'default'
        else:
            notes = get(sys.argv, n + 4, '') == '--notes'

        problemdir(name, directory, lang, template, notes)

    elif target == 'contest':
        # prog contest [name] [lang] [problemcount] ?[template] ?[--notes]
        name = sys.argv[n + 1]
        lang = sys.argv[n + 2]
        problemcount = int(sys.argv[n + 3])
        if problemcount not in range(1, 27):
            return print('Problemcount cannot be lower than 0 or higher than 26')

        template = get(sys.argv, n + 4, 'default')
        if template == '--notes':
            notes = True
            template = 'default'
        else:
            notes = get(sys.argv, n + 5, '') == '--notes'

        contest(name, directory, lang, problemcount, template, notes)

    elif target == 'contestwpdir':
        # prog contestwpdir [name] [lang] [problemcount] ?[template] ?[--notes]
        name = sys.argv[n + 1]
        lang = sys.argv[n + 2]
        problemcount = int(sys.argv[n + 3])
        if problemcount not in range(1, 27):
            return print('Problemcount cannot be lower than 0 or higher than 26')
        template = get(sys.argv, n + 4, 'default')
        if template == '--notes':
            notes = True
            template = 'default'
        else:
            notes = get(sys.argv, n + 5, '') == '--notes'

        contestwpdir(name, directory, lang, problemcount, template, notes)

    elif target is None:
        print('No command was provided')

    else:
        print('Unknown command.')

if __name__ == "__main__":
    main()
    
