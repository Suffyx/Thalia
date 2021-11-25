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
from discord.commands import slash_command, Option

from core import Thalia

from constants import GUILD_IDS
from constants import CATEGORIES


class RoomCommands(commands.Cog):
    """Initialize RoomCommand Cog

    Parameters:
       bot: core.Thalia - The bot on which the cog is loaded. Passed by setup function in plugins/core/__init__.py
    """

    def __init__(self, bot: Thalia):
        self.bot = bot

    async def check_categories(self, ctx):
        for category in ctx.guild.categories:
            if len(category.channels) == 0:
                await category.delete()

    @slash_command(
        name="set-category",
        description="Sets the category of a lounge channel.",
        guild_ids=GUILD_IDS,
    )
    async def _set_category(
        self,
        ctx,
        category_name: Option(
            str,
            "The category you want to move the lounge to",
            choices=CATEGORIES,
            default="Discussion",
            required=False,
        ),
    ):
        await ctx.defer()
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a lounge to use this command.")

        if str(ctx.author.voice.channel.id) not in self.bot.rooms:
            return await ctx.respond("You must be in a lounge to use this command.")

        if (
            self.bot.rooms[str(ctx.author.voice.channel.id)]["author"].id
            != ctx.author.id
        ):
            return await ctx.respond("You must own the room to use this command.")

        try:
            category = discord.utils.get(
                ctx.guild.categories, name=category_name.lower()
            )
            if category is None:
                throw

        except:
            category = await ctx.guild.create_category_channel(category_name.lower())

        await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].edit(
            category=category
        )
        await self.bot.rooms[str(ctx.author.voice.channel.id)]["tc"].edit(
            category=category
        )

        await ctx.respond(f"Moved to **{category_name}** category.")
        await self.check_categories(ctx)

    @slash_command(name="rename", description="Renames a voice or text channel.")
    async def _rename(
        self,
        ctx,
        name: Option(str, "The new name of the channel."),
        channel: Option(
            str,
            "The type of channel you want to rename.",
            choices=["text", "voice", "both"],
            default="both",
            required=False,
        ),
    ):
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a lounge to use this command.")

        if str(ctx.author.voice.channel.id) not in self.bot.rooms:
            return await ctx.respond("You must be in a lounge to use this command.")

        if (
            self.bot.rooms[str(ctx.author.voice.channel.id)]["author"].id
            != ctx.author.id
        ):
            return await ctx.respond("You must own the room to use this command.")

        if channel == "text":
            await self.bot.rooms[str(ctx.author.voice.channel.id)]["tc"].edit(name=name)
            await ctx.respond(f"Text channel renamed to **{name}**!")

        if channel == "voice":
            await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].edit(name=name)
            await ctx.respond(f"Voice channel renamed to **{name}**!")

        if channel == "both":
            await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].edit(name=name)
            await self.bot.rooms[str(ctx.author.voice.channel.id)]["tc"].edit(name=name)
            await ctx.respond(f"Both channels renamed to **{name}**!")

    @slash_command(name="bitrate", description="Edits the bitrate of a lounge channel.")
    async def _bitrate(
        self, ctx, bitrate: Option(int, "A bitrate between 8 and 96 for the channel.")
    ):
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a lounge to use this command.")

        if str(ctx.author.voice.channel.id) not in self.bot.rooms:
            return await ctx.respond("You must be in a lounge to use this command.")

        if (
            self.bot.rooms[str(ctx.author.voice.channel.id)]["author"].id
            != ctx.author.id
        ):
            return await ctx.respond("You must own the room to use this command.")

        if bitrate < 8 or birate > 96:
            return await ctx.respond("Birate must be a number between 8 and 96.")

        await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].edit(
            bitrate=bitrate
        )
        await ctx.respond(f"Birate set to **{bitrate}**")

    @slash_command(name="lock", description="Locks a channel from members.")
    async def _lock(self, ctx):
        await ctx.defer()
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a lounge to use this command.")

        if str(ctx.author.voice.channel.id) not in self.bot.rooms:
            return await ctx.respond("You must be in a lounge to use this command.")

        if (
            self.bot.rooms[str(ctx.author.voice.channel.id)]["author"].id
            != ctx.author.id
        ):
            return await ctx.respond("You must own the room to use this command.")

        if "locked" in self.bot.rooms[str(ctx.author.voice.channel.id)]:
            if self.bot.rooms[str(ctx.author.voice.channel.id)]["locked"] == True:
                await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].edit(
                    user_limit=None
                )
                await self.bot.rooms[str(ctx.author.voice.channel.id)][
                    "vc"
                ].set_permissions(
                    ctx.guild.default_role,
                    overwrite=discord.PermissionOverwrite(connect=None),
                )

                for member in ctx.guild.members:
                    if (
                        member
                        in self.bot.rooms[str(ctx.author.voice.channel.id)]["kicked"]
                    ):
                        continue
                    await self.bot.rooms[str(ctx.author.voice.channel.id)][
                        "vc"
                    ].set_permissions(
                        member, overwrite=discord.PermissionOverwrite(connect=None)
                    )

                await ctx.respond("Voice channel **unlocked**.")
                self.bot.rooms[str(ctx.author.voice.channel.id)]["locked"] = False

            elif self.bot.rooms[str(ctx.author.voice.channel.id)]["locked"] == False:
                await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].edit(
                    user_limit=len(ctx.author.voice.channel.members)
                )
                await self.bot.rooms[str(ctx.author.voice.channel.id)][
                    "vc"
                ].set_permissions(
                    ctx.guild.default_role,
                    overwrite=discord.PermissionOverwrite(connect=False),
                )
                await ctx.respond("Voice channel **locked**.")
                self.bot.rooms[str(ctx.author.voice.channel.id)]["locked"] = True

        else:
            await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].edit(
                user_limit=len(ctx.author.voice.channel.members)
            )
            await self.bot.rooms[str(ctx.author.voice.channel.id)][
                "vc"
            ].set_permissions(
                ctx.guild.default_role,
                overwrite=discord.PermissionOverwrite(connect=False),
            )
            self.bot.rooms[str(ctx.author.voice.channel.id)]["locked"] = True
            await ctx.respond("Voice channel **locked**.")

    @slash_command(
        name="limit",
        description="Limits the number of people allowed to join a voice channel.",
    )
    async def _limit(
        self,
        ctx,
        limit: Option(
            int, "The number of people allowed to join the channel between 1-99."
        ),
    ):
        await ctx.defer()
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a lounge to use this command.")

        if str(ctx.author.voice.channel.id) not in self.bot.rooms:
            return await ctx.respond("You must be in a lounge to use this command.")

        if (
            self.bot.rooms[str(ctx.author.voice.channel.id)]["author"].id
            != ctx.author.id
        ):
            return await ctx.respond("You must own the room to use this command.")

        if limit < 1 or limit > 99:
            return await ctx.respond("Limit must be an integer between 1 and 99.")

        await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].edit(
            user_limit=limit
        )
        await ctx.respond(f"Room limit set to **{limit}**!")

    @slash_command(name="kick", description="Kicks a member from a lounge channel.")
    async def _kick(
        self,
        ctx,
        member: Option(discord.Member, "The member you want to kick from the lounge."),
    ):
        await ctx.defer()
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a lounge to use this command.")

        if str(ctx.author.voice.channel.id) not in self.bot.rooms:
            return await ctx.respond("You must be in a lounge to use this command.")

        if (
            self.bot.rooms[str(ctx.author.voice.channel.id)]["author"].id
            != ctx.author.id
        ):
            return await ctx.respond("You must own the room to use this command.")

        if member == ctx.author:
            return await ctx.respond("You cannot kick yourself.")

        await member.move_to(None)
        self.bot.rooms[str(ctx.author.voice.channel.id)]["kicked"].append(member)

        await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].set_permissions(
            member, overwrite=discord.PermissionOverwrite(connect=False)
        )

        await ctx.respond(f"Member **{member.display_name}** has been kicked.")

    @slash_command(name="delimit", description="Resets the limit on a voice channel.")
    async def _delimit(self, ctx):
        await ctx.defer()
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a lounge to use this command.")

        if str(ctx.author.voice.channel.id) not in self.bot.rooms:
            return await ctx.respond("You must be in a lounge to use this command.")

        if (
            self.bot.rooms[str(ctx.author.voice.channel.id)]["author"].id
            != ctx.author.id
        ):
            return await ctx.respond("You must own the room to use this command.")

        await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].edit(
            user_limit=None
        )
        await ctx.respond("Limit has been removed from the lounge channel.")

    @slash_command(name="invite", description="Invites a user to a voice channel.")
    async def _invite(
        self,
        ctx,
        member: Option(discord.Member, "The member you want to invite to the channel."),
    ):
        await ctx.defer()
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a lounge to use this command.")

        if str(ctx.author.voice.channel.id) not in self.bot.rooms:
            return await ctx.respond("You must be in a lounge to use this command.")

        if (
            self.bot.rooms[str(ctx.author.voice.channel.id)]["author"].id
            != ctx.author.id
        ):
            return await ctx.respond("You must own the room to use this command.")

        if (
            "locked" not in self.bot.rooms[str(ctx.author.voice.channel.id)]
            or self.bot.rooms[str(ctx.author.voice.channel.id)]["locked"] == False
        ):
            await self.bot.rooms[str(ctx.author.voice.channel.id)][
                "vc"
            ].set_permissions(
                member, overwrite=discord.PermissionOverwrite(connect=True)
            )

            if member in self.bot.rooms[str(ctx.author.voice.channel.id)]["kicked"]:
                self.bot.rooms[str(ctx.author.voice.channel.id)]["kicked"].remove(
                    member
                )

            return await ctx.respond("Member invited to the room.")

        await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].edit(
            user_limit=ctx.author.voice.channel.user_limit + 1
        )

        await self.bot.rooms[str(ctx.author.voice.channel.id)]["vc"].set_permissions(
            member, overwrite=discord.PermissionOverwrite(connect=True)
        )

        if member in self.bot.rooms[str(ctx.author.voice.channel.id)]["kicked"]:
            self.bot.rooms[str(ctx.author.voice.channel.id)]["kicked"].remove(member)

        await ctx.respond("Member invited to the room.")
