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

from subprocess import call
from os import chdir


class ErrorHandler(commands.Cog):
    """Initialize Error Cog

    Parameters:
       bot: core.Thalia - The bot on which the cog is loaded. Passed by setup function in plugins/core/__init__.py
    """

    def __init__(self, bot: Thalia:
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(ctx: Context, error: Exception):
        """Run script 'thaliaError.sh', and pass the error, so that error messages continue output even if Thalia is silenced or made a background process.

        Parameters:
           ctx: core.Context - The context for the command which produced the error
           error: Exception - The exception which was produced by the command. Not to be confused with outputs of the core.Context.error() method
        """
        chdir("../../../scripts/")
        i = error.replace("'", "\\'")
        call(f"./thaliaError.sh '{i}'", shell=True)
        chdir("../plugins/core/error/")
