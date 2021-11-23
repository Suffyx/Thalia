"""
MIT License

Copyright (c) 2021 Suffyx

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

import discord
from discord.ext import commands

import shelve
import json
import os

from .Context import Context

from discord.interactions import Interaction

# from utils import __build_database

def recursive_object_builder(d):
    """Returns a dictionary as an object class.

    Parameters:
      d: dict - The dictionary whose keys and values will become an object.
    """
    if isinstance(d, list):
        d = [recursive_object_builder(x) for x in d]

    if not isinstance(d, dict):
        return d

    class Obj:
        pass

    obj = Obj()

    for o in d:
        obj.__dict__[o] = recursive_object_builder(d[o])

    return obj

class Thalia(commands.AutoShardedBot):
    """Build and run base Thalia class.

    Child of `discord.ext.commands.AutoShardedBot`
    """

    def __init__(self, *args, **kwargs):
        self.__config_state = False
        self.__config = None
        
        super().__init__(
            command_prefix=self.__get_prefix,
            intents=discord.Intents.all(),
            strip_after_prefix=True,
            case_insensitive=True,
            chunk_guilds_at_startup=False,
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=f"{self.config.DEFAULT_PREFIX}help"
            ),
            *args,
            **kwargs
        )

        self.__default_prefix = self.config.DEFAULT_PREFIX

        #     self.db = {
        #       "prefixes": shelve.open(self.config.PREFIX_TABLE_PATH),
        #       "guilds": shelve.open(self.config.GUILD_TABLE_PATH),
        #       "users": shelve.open(self.config.USER_TABLE_PATH)
        #     }

        # makes sure that the database has all necessary attributes to run the bot properly
        #     __build_database(self.db)
            
        self.rooms = {} # set up rooms dictionary so that plugins.rooms.EventHandler and plugins.rooms.RoomCommands can remain consistent

#     @property
#     def db(self):
#         """Returns a dictionary of open shelves."""
#         return {
#             "prefixes": shelve.open(self.config.PREFIX_TABLE_PATH),
#             "guilds": shelve.open(self.config.GUILD_TABLE_PATH),
#             "users": shelve.open(self.config.USER_TABLE_PATH),
#         }

    @property
    def config(self):
        """Build and return config.json as an object."""
        # returns config object that has already been loaded if it has been loaded in the past
        if self.__config_state:
            return self.__config
        with open(os.getenv("CONFIG_PATH")) as f:
            config_obj = recursive_object_builder(json.load(f))

        self.__config_state = True
        self.__config = config_obj
        return config_obj

    def __get_prefix(self, bot, message: discord.Message):
        """Returns a guild's set prefix or the default prefix.

        Parameters:
           message: discord.Message - The context message for the prefix.
        """
#         if not message.guild:
#             return self.__default_prefix

#         elif str(message.guild.id) not in self.db["prefixes"]:
#             return self.__default_prefix

#         else:
#             return self.db["prefixes"][str(message.guild.id)]

        return self.__default_prefix

#     async def process_commands(self, message: Message) -> None:
#         """|coro|

#         This function processes the commands that have been registered
#         to the bot and other groups. Without this coroutine, none of the
#         commands will be triggered.
#         By default, this coroutine is called inside the :func:`.on_message`
#         event. If you choose to override the :func:`.on_message` event, then
#         you should invoke this coroutine as well.
#         This is built using other low level tools, and is equivalent to a
#         call to :meth:`~.Bot.get_context` followed by a call to :meth:`~.Bot.invoke`.
#         This also checks if the message's author is a bot and doesn't
#         call :meth:`~.Bot.get_context` or :meth:`~.Bot.invoke` if so.
#         Parameters
#         -----------
#         message: :class:`discord.Message`
#             The message to process commands for.
#         """
#         if message.author.bot:
#             return

#         ctx = await self.get_context(message, Context)
#         await self.invoke(ctx)

    async def on_message(self, message: discord.Message):
        """The general on_message event listener. When overridden, commands will not register unless this function, or any equivalent is likewise called.

        Parameters:
           message: discord.Message - The message registered by the listener.
        """
        await self.process_commands(message)
        
#     async def process_application_commands(self, interaction: Interaction) -> None:
#         """|coro|
#         This function processes the commands that have been registered
#         to the bot and other groups. Without this coroutine, none of the
#         commands will be triggered.
#         By default, this coroutine is called inside the :func:`.on_interaction`
#         event. If you choose to override the :func:`.on_interaction` event, then
#         you should invoke this coroutine as well.
#         This function finds a registered command matching the interaction id from
#         :attr:`.ApplicationCommandMixin.application_commands` and runs :meth:`ApplicationCommand.invoke` on it. If no matching
#         command was found, it replies to the interaction with a default message.
#         .. versionadded:: 2.0
#         Parameters
#         -----------
#         interaction: :class:`discord.Interaction`
#             The interaction to process
#         """
#         if interaction.type not in (
#             InteractionType.application_command, 
#             InteractionType.auto_complete
#         ):
#             return

#         try:
#             command = self._application_commands[interaction.data["id"]]
#         except KeyError:
#             self.dispatch("unknown_command", interaction)
#         else:
#             if interaction.type is InteractionType.auto_complete:
#                 ctx = await self.get_autocomplete_context(interaction)
#                 ctx.command = command
#                 return await command.invoke_autocomplete_callback(ctx)
            
#             ctx = await self.get_application_context(interaction)
#             ctx.command = command
#             self.dispatch("application_command", ctx)
#             try:
#                 if await self.can_run(ctx, call_once=True):
#                     await ctx.command.invoke(ctx)
#                 else:
#                     raise CheckFailure("The global check once functions failed.")
#             except DiscordException as exc:
#                 await ctx.command.dispatch_error(ctx, exc)
#             else:
#                 self.dispatch("application_command_completion", ctx)

    async def get_application_context(
        self, interaction: Interaction, cls=None
    ) -> Context:
        r"""|coro|
        Returns the invocation context from the interaction.
        This is a more low-level counter-part for :meth:`.process_application_commands`
        to allow users more fine grained control over the processing.
        Parameters
        -----------
        interaction: :class:`discord.Interaction`
            The interaction to get the invocation context from.
        cls
            The factory class that will be used to create the context.
            By default, this is :class:`.ApplicationContext`. Should a custom
            class be provided, it must be similar enough to
            :class:`.ApplicationContext`\'s interface.
        Returns
        --------
        :class:`.ApplicationContext`
            The invocation context. The type of this can change via the
            ``cls`` parameter.
        """
        if cls is None:
            cls = Context
        return cls(self, interaction)
