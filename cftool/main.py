#!usr/bin/env python
import sys
import os
import clicore

parser = clicore.Parser()

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

def get(l, i, d):
    try:
        return l[i]
    except IndexError:
        return d

def getrange(l, i, ds = []):
    x = 0
    r = []
    for j in range(i):
        try:
            r.append(l[j])
        except IndexError:
            r.append(ds[x])
            x += 1
    return r

def problem_parser(args):
    directory, name, template = getrange(args, 3, ['default'],)

    return {'directory' : directory, 
            'name' : name, 
            'template' : template}

@parser.command(problem_parser,
                name = 'problem',
                usage = 'problem [file] ?[template]'
                )
def problem(directory, name, template):
    """Create a single file with given template."""

    lang = name.split('.')[-1]
    code = get_template_code(lang, template)

    with open(os.path.join(directory, name), 'w') as f:
        f.write(code)


def problemdir_parser(args):
    directory, name, lang = getrange(args, 3)
    template = get(args, 3, 'default')

    return {'directory' : directory, 
            'name' : name, 
            'lang' : lang,
            'template' : template}

@parser.command(problemdir_parser,
                name = 'problemdir',
                aliases = ['pdir', 'pwdir'],
                usage = 'problemdir [name] [lang] ?[template] ?[--notes]',
                flags = ['notes']
                )
def problemdir(directory, name, lang, template, notes):
    """Put the solution file in a directory, add a notes.txt optionally"""

    directory = os.path.join(directory, name)
    os.mkdir(directory)
    problem(directory, f'sol.{lang}', template)
    if notes:
        makenotesfile(directory)

def contest_parser(args):
    # Works for contestwpdir too.
    directory, name, lang, problemcount = getrange(args, 4)
    problemcount = int(problemcount)

    if problemcount not in range(1, 27):
        raise Exception('Problemcount cannot be lower than 0 or higher than 26')

    template = get(args, 4, 'default')

    return {'directory' : directory, 
            'name' : name, 
            'lang' : lang, 
            'problemcount' : problemcount, 
            'template' : template}


@parser.command(contest_parser, 
                name = 'contest',
                usage = 'contest [name] [lang] [problemcount] ?[template] ?[--notes]',
                flags = ['notes']
                )
def contest(directory, name, lang, problemcount, template, notes):
    """Create a directory, and create an file for each invidiual solution (Follows codeforces naming scheme)"""

    import string
    directory = os.path.join(directory, name)
    os.mkdir(directory)
    for i in range(problemcount):
        problem(directory, f'{string.ascii_uppercase[i]}.{lang}', template)

    if notes:
        makenotesfile(directory)

@parser.command(contest_parser,
                name = 'contestwpdir',
                aliases = ['cwpdir'],
                usage = 'contestwpdir [name] [lang] [problemcount] ?[template] ?[--notes]',
                flags = ['notes']
                )
def contestwpdir(directory, name, lang, problemcount, template, notes):
    """Same as contest, however a new directory is created foreach solution file"""

    import string
    directory = os.path.join(directory, name)
    os.mkdir(directory)
    for i in range(problemcount):
        s = string.ascii_uppercase[i]
        problemdir(directory, s, lang, template, False)

    if notes:
        makenotesfile(directory)

def main(): 
    target = get(sys.argv, 1, None)
    directory = os.getcwd()
    args = [directory,] + sys.argv[2: len(sys.argv)]
    flags, args = parser.parse_flags(args)

    if target is None:
        return print('No command was provided')

    try:
        return parser.parse(target, args, flags)
    except clicore.CommandNotFound:
        return print('Command not found.')

if __name__ == "__main__":
    main()
    
