class Parser:
    def __init__(self):
        self._commands = {}
        self.alias_table = {}

    def parse(self, command, arguments, flags):
        name = self.alias_table.get(command, None)
        if name is None:
            raise CommandNotFound

        command = self._commands.get(name, None)
        return command._parse_and_invoke(arguments, flags)

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

    def parse_flags(self, args):
        flags, notflags = ({}, [])
        x = 0
        while x < len(args):
            arg = args[x]
            if arg.startswith('--') and len(arg) > 2:
                flags[arg[2:]] = True
            elif arg.startswith('-') and len(arg) > 1:
                try:
                    if args[x+1].startswith('-'): # Store flags. These are currently unused.
                        raise Exception(f'No value was provided for flag {arg}')
                    flags[arg[1:]] = args[x+1] # The next argument should be the value

                except IndexError:
                    raise Exception(f'Unexpected end of input after flag declaration.')
                x += 1 # We will skip the next index
            else:
                notflags.append(arg)
            x += 1

        return flags, notflags

    @property
    def commands(self):
        return [command for command in self._commands.values()]

class Command:
    def __init__(self, func, parser_func, **kwargs):
        self.name = kwargs.get('name') or func.__name__
        self.aliases = kwargs.get('aliases') or []
        self.usage = kwargs.get('usage', None)
        self.help = func.__doc__ or None

        self.callback = func
        self.parser_func = parser_func
        self.params = self.callback.__code__.co_varnames[:self.callback.__code__.co_argcount]
        self.flags = kwargs.get('flags', [])

        for flag in self.flags:
            if flag not in self.params:
                raise Exception(f'Flag "{flag}" is not an argument in function {self.callback}')

    def _parse_and_invoke(self, arguments, flags):
        args = self.parser_func(arguments)
        
        requiredflags = [flag for flag in flags if flag in self.flags] 
        ignoredflags = [flag for flag in flags if flag not in requiredflags]

        for flag in ignoredflags:
            print(f'Ignoring unexpected flag: "{flag}"')

        for flag in requiredflags:
            args[flag] = flags[flag]

        return self(**args)

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

class CommandNotFound(Exception):
    pass

class CommandAlreadyRegistered(Exception):
    pass

