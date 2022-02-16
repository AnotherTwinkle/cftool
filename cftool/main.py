#!usr/bin/env python
import sys
import os
import string
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

@parser.command(name = 'problem', usage = 'problem [file] ?[template]')
def problem(ctx, name, template= 'default'):
    """Create a single file with given template."""

    lang = name.split('.')[-1]
    code = get_template_code(lang, template)

    with open(os.path.join(ctx.directory, name), 'w') as f:
        f.write(code)


@parser.add_flag(name= 'notes', default= False)
@parser.command(name = 'problemdir', aliases = ['pdir', 'pwdir'], usage = 'problemdir [name] [lang] ?[template] ?[--notes]')
def problemdir(ctx, name, lang, template= 'default'):
    """Put the solution file in a directory, add a notes.txt optionally"""

    directory = os.path.join(ctx.directory, name)
    os.mkdir(directory)

    dummyctx = clicore.Context(command= problem, directory= directory)
    problem.invoke(dummyctx, f'sol.{lang}', template)

    if ctx.flags.notes:
        makenotesfile(directory)

@parser.add_flag(name= 'notes', default= False)
@parser.command(name = 'contest', usage = 'contest [name] [lang] [problemcount] ?[template] ?[--notes]')
def contest(ctx, name, lang, problemcount : int, template= 'default'):
    """Create a directory, and create an file for each invidiual solution (Follows codeforces naming scheme)"""

    directory = os.path.join(ctx.directory, name)
    os.mkdir(directory)

    if problemcount not in range(1, 27):
        return print('Problemcount cannot be lower than 0 or higher than 26')

    dummyctx = clicore.Context(command= problem, directory= directory)

    for i in range(problemcount):
        problem.invoke(dummyctx, f'{string.ascii_uppercase[i]}.{lang}', template)

    if ctx.flags.notes:
        makenotesfile(directory)


@parser.add_flag(name= 'notes', default= False)
@parser.command(name = 'contestwpdir', aliases = ['cwpdir'], usage = 'contestwpdir [name] [lang] [problemcount] ?[template] ?[--notes]')
def contestwpdir(ctx, name, lang, problemcount : int, template= 'default'):
    """Same as contest, however a new directory is created foreach solution file"""

    directory = os.path.join(ctx.directory, name)
    os.mkdir(directory)
    dummyctx = clicore.Context(command= problemdir, directory= directory)

    if problemcount not in range(1, 27):
        return print('Problemcount cannot be lower than 0 or higher than 26')

    for i in range(problemcount):
        s = string.ascii_uppercase[i]
        problemdir.invoke(dummyctx, s, lang, template)

    if ctx.flags.notes:
        makenotesfile(directory)

def main():
    parser.run()

if __name__ == "__main__":
    main()
    
