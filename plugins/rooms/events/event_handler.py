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

import discord
from discord.ext import commands

from core import Thalia


class EventHandler(commands.Cog):
    """Initialize EventHandler Cog

    Parameters:
       bot: core.Thalia - The bot on which the cog is loaded. Passed by setup function in plugins/core/__init__.py
    """

    def __init__(self, bot: Thalia):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Handle voice state updates.

        Parameters:
           member: discord.Member - The member to whom the update pertains.
           before: payload - The data object of the state before the update.
           after: payload - The data object of the state after the update.
        """
        # on join
        if before.channel is None and after.channel is not None:
            await self.on_member_join(member, after)
            
        # on leave
        elif before.channel is not None and after.channel is None:
            await self.on_member_leave(member, before)
            
        # on move
        elif before.channel is not None and after.channel is not None:
            await self.on_member_move(member, before, after)
            
            
    async def on_member_join(member, context):
        """Handle voice channel joins.

        Parameters:
           member: discord.Member - The member to whom the join pertains.
           context: payload - The data object of the voice state.
        """
        pass
        
    async def on_member_leave(member, context):
        """Handle voice channel leave.

        Parameters:
           member: discord.Member - The member to whom the leave pertains.
           context: payload - The data object of the voice state.
        """
        pass
        
    async def on_member_move(member, before, after):
        """Handle voice channel leave.

        Parameters:
           member: discord.Member - The member to whom the move pertains.
           before: payload - The data object of the voice state before the move.
           after: payload - The data object of the voice state after the move.
        """
        pass
