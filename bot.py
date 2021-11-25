import discord
from core import Thalia

bot = Thalia()


def main():
    """Builds and runs Thalia."""
    for ext in bot.config.EXTENSIONS:
        bot.load_extension(ext)

    bot.run(bot.config.TOKEN)


if __name__ == "__main__":
    main()
