class Parser:
    def __init__(self):
        self._commands = {}
        self.alias_table = {}

    def parse(self, command, arguments):
        name = self.alias_table.get(command, None)
        if name is None:
            raise CommandNotFound

        command = self._commands.get(name, None)
        return command._parse_and_invoke(arguments)

    def command(self, parser_func, **kwargs):
        def decorator(func):
            command = Command(func, parser_func, **kwargs)

            if command.name in self._commands:
                raise CommandAlreadyRegistered("This command has already been reigstered.")

            if not isinstance(command.aliases, (list, tuple)):
                raise Exception("aliases must be a list or tuple.")
            
            for alias in command.aliases:
                if alias in self.alias_table:
                    raise CommandAlreadyRegistered("This alias has already been registered.")

            self._commands[command.name] = command
            for alias in command.aliases:
                self.alias_table[alias] = command.name
            self.alias_table[command.name] = command.name

            return command 
        return decorator

    @property
    def commands(self):
        return [command for command in self._commands.values()]

class Command:
    def __init__(self, func, parser_func, **kwargs):
        self.name = kwargs.get('name') or func.__name__
        self.aliases = kwargs.get('aliases') or []
        self.usage = kwargs.get('usage') or 'Not provided.'
        self.help = func.__doc__ or 'Not provided.'

        self.callback = func
        self.parser_func = parser_func

    def _parse_and_invoke(self, arguments):
        args = self.parser_func(arguments)
        return self.callback(*args)

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

class CommandNotFound(Exception):
    pass

class CommandAlreadyRegistered(Exception):
    pass

################ TESTS

parser = Parser()

def parse_foo(arglist):
    return (arglist[0],)

@parser.command(parse_foo, name = 'bar', aliases = ['baz'], usage = 'foo [bar]')
def foo(bar):
    print(bar)

# parser.parse('baz', ['aa'])
    


