from errbot import BotPlugin, botcmd


class Alias(BotPlugin):
    """
    Alias command for Errbot.
    """

    def callback_message(self, mess):
        command = mess.body.split(' ', 1)

        if len(command) > 0:
            alias = command[0].strip(self._bot.bot_config.BOT_PREFIX)
            args = ''

            if len(command) > 1:
                args = command[1]

            if alias in self:
                mess.body = u'{0}{1} {2}'.format(
                    self._bot.bot_config.BOT_PREFIX,
                    self[alias],
                    args
                )
                self._bot.process_message(mess)

    @botcmd
    def alias(self, mess, args):
        """List all aliases."""
        if len(args) < 2:
            return self.alias_list(mess, args)

    @botcmd(split_args_with=None, admin_only=True)
    def alias_add(self, mess, args):
        """Define a new alias."""
        if len(args) < 2:
            return 'usage: !alias add <name> <command>'

        name = args.pop(0)
        command = ' '.join(args)

        if name in self:
            return 'An alias with that name already exists.'

        self[name] = command

        return 'Alias created.'

    @botcmd(admin_only=True)
    def alias_remove(self, mess, args):
        name = args

        if not name:
            return 'usage: !alias remove <name>'

        try:
            del self[name]
            return 'Alias removed.'
        except KeyError:
            return 'That alias does not exist. ' \
                   'Use !alias list to see all aliases.'

    @botcmd
    def alias_list(self, mess, args):
        """List all aliases."""
        if len(self) > 0:
            return 'All Aliases :\n' + u'\n'.join(
                ['!' + alias + ' = !' + self[alias] for alias in self])
        else:
            return 'No aliases found. Use !alias add to define one.'
