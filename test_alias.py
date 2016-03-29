import os
import unittest
import alias

from flaky import flaky

from errbot.backends.test import testbot


@flaky
class TestAliasPlugin(object):
    extra_plugin_dir = '.'

    def test_command_alias_add(self, testbot):
        testbot.push_message('!alias add s status')
        assert 'Alias created.' in testbot.pop_message()

    def test_command_alias_add_exists(self, testbot):
        testbot.push_message('!alias add s status')
        assert 'Alias created.' in testbot.pop_message()
        testbot.push_message('!alias add s status')
        assert 'An alias with that name already exists.' in testbot.pop_message()

    def test_command_alias_add_usage(self, testbot):
        testbot.push_message('!alias add')
        assert 'usage: !alias add <name> <command>' in testbot.pop_message()

    def test_command_alias_list(self, testbot):
        testbot.push_message('!alias add s status')
        testbot.pop_message()
        testbot.push_message('!alias')
        assert '!s = !status' in testbot.pop_message()

    def test_command_alias_list_not_defined(self, testbot):
        testbot.push_message('!alias')
        assert 'No aliases found. Use !alias add to define one.' in testbot.pop_message()

    def test_command_alias_remove(self, testbot):
        testbot.push_message('!alias add s status')
        testbot.pop_message()
        testbot.push_message('!alias remove s')
        assert 'Alias removed.' in testbot.pop_message()
        testbot.push_message('!alias')
        assert '!s = !status' not in testbot.pop_message()

    def test_command_alias_remove_not_exists(self, testbot):
        testbot.push_message('!alias remove s')
        assert 'That alias does not exist.' in testbot.pop_message()

    def test_command_alias_remove_usage(self, testbot):
        testbot.push_message('!alias remove')
        assert 'usage: !alias remove <name>' in testbot.pop_message()
