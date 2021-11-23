import discord
from core import Thalia

bot = Thalia()

def main():
    """Builds and runs Thalia."""
    for item in bot.config.EXTENSIONS:
        bot.load_extension(item)
    
    bot.run(bot.config.TOKEN)
    
