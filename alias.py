from errbot import BotPlugin, botcmd


class Alias(BotPlugin):
    """
    Use shortcuts for long commands.
    """

    def callback_message(self, mess):
        command = mess.body.split(' ', 1)

        if len(command) > 0:
            alias = command[0].strip(self._bot.prefix)
            args = ''

            if len(command) > 1:
                args = command[1]

            if alias in self:
                mess.body = u'{prefix}{command} {args}'.format(
                    prefix=self._bot.prefix,
                    command=self[alias],
                    args=args
                )
                self._bot.process_message(mess)

    @botcmd
    def alias(self, mess, args):
        """List all aliases."""
        if len(args) < 2:
            return self.alias_list(mess, args)

    @botcmd(split_args_with=None)
    def alias_add(self, mess, args):
        """Define a new alias."""
        if len(args) < 2:
            return u'usage: {prefix}alias add <name> <command>'.format(
                prefix=self._bot.prefix
            )

        name = args.pop(0)
        command = ' '.join(args)

        if name in self:
            return u'An alias with that name already exists.'

        self[name] = command

        return u'Alias created.'

    @botcmd
    def alias_remove(self, mess, args):
        """Remove an alias."""
        name = args

        if not name:
            return u'usage: {prefix}alias remove <name>'.format(
                prefix=self._bot.prefix
            )

        try:
            del self[name]
            return u'Alias removed.'
        except KeyError:
            return 'uThat alias does not exist. ' \
                   'Use {prefix}alias list to see all aliases.'.format(
                       prefix=self._bot.prefix
                   )

    @botcmd
    def alias_list(self, mess, args):
        """List all aliases."""
        if len(self) > 0:
            return u'All Aliases:\n\n' + u'\n'.join(
                ['- {prefix}{alias} = {prefix}{command}'.format(
                    prefix=self._bot.prefix,
                    alias=alias,
                    command=self[alias]
                ) for alias in self])
        else:
            return u'No aliases found. ' \
                   'Use {prefix}alias add to define one.'.format(
                       prefix=self._bot.prefix
                   )
