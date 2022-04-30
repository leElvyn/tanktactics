import discord
from discord.ext import commands
from discord import Intents, app_commands

import pyppeteer
import asyncio
import aiohttp
import os

from cogs.tanktactics import TankTactics
from error_handler import CommandErrorHandler
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("TT_AUTHORIZATION_TOKEN")
bot_token = os.environ.get("TT_BOT_TOKEN")

EMOJI_GUILD = 869906440268173333


async def startup():
    print("Starting up...")

    bot = commands.Bot(command_prefix='&', intents=Intents.none())

    cog = TankTactics(bot)

    await cog.initialize(token, EMOJI_GUILD)
    await bot.add_cog(cog)
    await bot.add_cog(CommandErrorHandler(bot))

    await bot.start(bot_token)


asyncio.run(startup())