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

import asyncio

import discord
from discord.ext import commands
from discord.commands import slash_command, Option

from core import Thalia

from constants import VOICE_JOIN_ID
from constants import GENERAL_CATEGORY_ID
from constants import GUILD_IDS

from async_timeout import timeout


class EventHandler(commands.Cog):
    """Initialize EventHandler Cog

    Parameters:
       bot: core.Thalia - The bot on which the cog is loaded. Passed by setup function in plugins/core/__init__.py
    """

    def __init__(self, bot: Thalia):
        self.bot = bot

        # bot.loop.create_task(self.room_handler_task())

    async def check_categories(self, guild):
        for category in guild.categories:
            if len(category.channels) == 0:
                await category.delete()

    # async def author_getter(room):
    #     while True:
    #         if self.bot.rooms[room]['author'] not in self.bot.rooms[room]['vc'].members:
    #             await asycio.sleep(5) # save some memory or whatever
    #             continue
    #         else:
    #             return

    # async def room_handler_task(self):
    #     while True:
    #         for room in self.bot.rooms:
    #             if self.bot.rooms[room]['author'] not in self.bot.rooms[room]['vc'].members:
    #                 try:
    #                     async with timeout(300):
    #                         await self.author_getter(room)
    #                 except asyncio.TimeoutError:
    #                     await self.bot.rooms[room]['vc'].delete()
    #                     await self.bot.rooms[room]['tc'].delete()
    #                     del self.bot.rooms[room]

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Handle voice state updates.

        Parameters:
           member: discord.Member - The member to whom the update pertains.
           before: payload - The data object of the state before the update.
           after: payload - The data object of the state after the update.
        """
        if before.channel.members == after.channel.members and before.channel.id == after.channel.id: # Ignore non join, move, or leave events
            return
        
        # on join
        if before.channel is None and after.channel is not None:
            await self.on_member_join(member, after)

        # on leave
        elif before.channel is not None and after.channel is None:
            await self.on_member_leave(member, before)

        # on move
        elif before.channel is not None and after.channel is not None:
            await self.on_member_move(member, before, after)

    async def on_member_join(self, member, context):
        """Handle voice channel joins.

        Parameters:
           member: discord.Member - The member to whom the join pertains.
           context: payload - The data object of the voice state.
        """
        if context.channel.id == VOICE_JOIN_ID:
            if member.name.lower().endswith("s") == False:
                name = member.name + "'s" + " Lounge"
            else:
                name = (
                    member.name + "'" + " Lounge"
                )  # make channel name scheme consistent with English grammar rules
            category = discord.utils.get(
                context.channel.guild.categories, id=GENERAL_CATEGORY_ID
            )
            voice_channel = await context.channel.guild.create_voice_channel(
                name, category=category
            )
            text_channel = await context.channel.guild.create_text_channel(
                name, category=category
            )

            await text_channel.set_permissions(
                context.channel.guild.default_role,
                overwrite=discord.PermissionOverwrite(view_channel=False),
            )

            # add room to bot cache
            self.bot.rooms[str(voice_channel.id)] = {}
            self.bot.rooms[str(voice_channel.id)]["vc"] = voice_channel
            self.bot.rooms[str(voice_channel.id)]["tc"] = text_channel
            self.bot.rooms[str(voice_channel.id)]["author"] = member
            self.bot.rooms[str(voice_channel.id)]["kicked"] = []

            await member.move_to(voice_channel)

        else:
            await self.bot.rooms[str(context.channel.id)]["tc"].set_permissions(
                member, view_channel=True
            )

    async def on_member_leave(self, member, context):
        """Handle voice channel leave.

        Parameters:
           member: discord.Member - The member to whom the leave pertains.
           context: payload - The data object of the voice state.
        """
        if context.channel.id == VOICE_JOIN_ID:
            pass

        if str(context.channel.id) in self.bot.rooms:
            await self.bot.rooms[str(context.channel.id)]["tc"].set_permissions(
                member, view_channel=False
            )

            if self.bot.rooms[str(context.channel.id)]["author"].id == member.id:
                embed = discord.Embed(
                    description="**⚠️ The channel owner has left. The room will expire in 5 minutes. ⚠️**",
                    color=discord.Colour.red(),
                )
                await self.bot.rooms[str(context.channel.id)]["tc"].send(embed=embed)

                try:
                    await self.bot.wait_for(
                        "voice_state_update",
                        check=lambda _member, _before, _after: _member.id
                        == self.bot.rooms[str(context.channel.id)]["author"].id
                        and _after.channel.id == context.channel.id,
                        timeout=300,
                    )

                    embed = discord.Embed(
                        description="** Expiration cancelled. **",
                        color=discord.Colour.green(),
                    )

                    await self.bot.rooms[str(context.channel.id)]["tc"].send(
                        embed=embed
                    )

                except:
                    guild = context.channel.guild
                    await self.bot.rooms[str(context.channel.id)]["tc"].delete()
                    await self.bot.rooms[str(context.channel.id)]["vc"].delete()
                    await self.check_categories(guild)

    async def on_member_move(self, member, before, after):
        """Handle voice channel leave.

        Parameters:
           member: discord.Member - The member to whom the move pertains.
           before: payload - The data object of the voice state before the move.
           after: payload - The data object of the voice state after the move.
        """
        if before.channel.id == VOICE_JOIN_ID:
            await self.bot.rooms[str(after.channel.id)]["tc"].set_permissions(
                member, view_channel=True
            )
            return
        if after.channel.id == VOICE_JOIN_ID:
            await self.on_member_join(member, after)
            return

        else:
            if str(before.channel.id) not in self.bot.rooms:
                await self.bot.rooms[str(after.channel.id)]["tc"].set_permissions(
                    member, view_channel=True
                )
            if self.bot.rooms[str(before.channel.id)]["author"].id == member.id:
                await self.on_member_leave(member, before)

            else:
                await self.bot.rooms[str(before.channel.id)]["tc"].set_permissions(
                    member, view_channel=False
                )
                await self.bot.rooms[str(after.channel.id)]["tc"].set_permissions(
                    member, view_channel=True
                )
