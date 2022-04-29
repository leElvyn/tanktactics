from operator import is_
import discord
from discord import interactions
from discord.ext import commands

import tt_views
import aiohttp
import pyppeteer
import asyncio
import inspect
import datetime
import os
import gettext

_ = gettext.gettext

class TankTactics(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
        self._last_member = None
        self.browser = None # we can't init browser here because it's async TO FIX

    def get_api_url(self, object):
        return f'http://127.0.0.1:8000/api/{object}'

    async def initialize(self, token, emoji_guild):
        self.emoji_guild_id = emoji_guild
        self.browser = await pyppeteer.launch(args=['--no-sandbox'], autoClose = False)
        await self.browser.newPage()
        headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        }

        clientSession = aiohttp.ClientSession(headers=headers)
        self.session = clientSession


    @commands.Cog.listener()
    async def on_ready(self):
        emojis_ids = {}
        emoji_guild = self.bot.get_guild(self.emoji_guild_id)
        for emoji in emoji_guild.emojis:
            emojis_ids[emoji.name] = emoji.id
        
        self.emojis_ids = emojis_ids

        self.beta_events_channel = self.bot.get_channel(735590589879095648) ###################### FOR BETA, SHOULD BE REMOVED 

        print('TankTactics is ready.')

    async def generate(self, focus_id):
        page = await self.browser.newPage()
        await page.setViewport({"width":1024, "height":1024})

        page.on("console", lambda message: print(message.text))
        await page.goto(f'http://127.0.0.1:8000/map/guild/869906440268173333?focus_player_id={focus_id}')
        await asyncio.sleep(0.5) #it sometimes blur, making sure it REALLy is loaded

        image_name = str(datetime.datetime.utcnow().timestamp())
        image_name = image_name.replace('.', '-') # to avoid problems with dots in file names
        image_name += '.png'
        image_path = os.getcwd() + '/static/staticmaps/' + image_name
        print(image_path)
        await page.screenshot({'path': image_path, "width":896, "height":896})
        await page.close()
        image_bin = open(image_path, 'rb')

        image_url = "https://tank-tactics.com/staticmaps/" + image_name
        return image_url

    async def fetch_player(self, ctx, player_id, guild_id, run_checks=True):
        async with self.session.get(self.get_api_url(f'guild/{guild_id}/players/{player_id}')) as response:
            print(response)
            if response.status == 404:
                await ctx.respond("You are not in the game")
                return 404
            player = await response.json()
            print(player)
            if player["is_dead"] == True and run_checks:
                await ctx.respond("You are dead")
            if player["tank"]["action_points"] <= 0:
                ## await ctx.respond("You are out of action points.")
                # here, is_disabled is true
                return (player, True)
        return (player, False)

    async def fetch_player_raw(self, player_id, guild_id):
        """fetch players without performing checks"""
        async with self.session.get(self.get_api_url(f'guild/{guild_id}/players/{player_id}')) as response:
            player = await response.json()
        
        return player

    async def fetch_game(self, ctx, guild_id):
        async with self.session.get(self.get_api_url(f'guild/{guild_id}')) as response:

            game = await response.json()
        return game

    async def create_player(self, guild_id, player: discord.Member):
        async with self.session.post(self.get_api_url(f"guild/{guild_id}/players/create"), json={"discord_id": player.id, "name": player.name, "avatar_url": player.avatar.url}) as response:
            print(response)
            if response.status == 201:
                return True
            else:
                return False

    async def log(self, game, message):
        channel = self.bot.get_channel(game["logs_channel"])
        await channel.send(message)

    @commands.slash_command()
    async def move(self, ctx):
        data = await self.fetch_player(ctx, ctx.author.id, ctx.guild.id)
        if data == 404:
            return

        url = await self.generate(ctx.author.id)

        game = await self.fetch_game(ctx, ctx.guild.id)
        embed = discord.Embed(title=_("Current game state :"))
        embed.set_image(url=url)
        view = tt_views.MoveView(self, ctx, data, game)

        message = await ctx.respond(embed=embed, view=view)
        await view.wait()
        await message.message.edit(view=view)


    @commands.slash_command()
    async def shoot(self, ctx):
        data = await self.fetch_player(ctx, ctx.author.id, ctx.guild.id)
        if data == 404:
            return
        
        url = await self.generate(ctx.author.id)

        embed = discord.Embed(title=_("Current game state :"))
        embed.set_image(url=url)

        game = await self.fetch_game(ctx, ctx.guild.id)

        view = tt_views.ShootView(self, ctx, data, game, is_friendly=False)

        message = await ctx.respond(embed=embed, view=view)

        await view.wait()
        await message.message.edit(view=view)


    @commands.slash_command()
    async def transfer(self, ctx: discord.ApplicationContext):
        data = await self.fetch_player(ctx, ctx.author.id, ctx.guild.id)
        if data == 404:
            return

        url = await self.generate(ctx.author.id)

        embed = discord.Embed(title=_("Current game state :"))
        embed.set_image(url=url)

        game = await self.fetch_game(ctx, ctx.guild.id)

        view = tt_views.ShootView(self, ctx, data, game, is_friendly=True)

        message = await ctx.respond(embed=embed, view=view)
        await view.wait()
        await ctx.interaction.response.edit_message(view=view)

    @commands.slash_command()
    async def upgrade(self, ctx):
        data = await self.fetch_player(ctx, ctx.author.id, ctx.guild.id)
        if data == 404:
            return
        
        url = await self.generate(ctx.author.id)

        embed = discord.Embed(title=_("Current game state :"))
        embed.set_image(url=url)

        game = await self.fetch_game(ctx, ctx.guild.id)

        view = tt_views.UpgradeRangeView(self, ctx, data, game)

        await ctx.respond(embed=embed, view=view)
        await view.wait()
        await ctx.interaction.response.edit_message(view=view)


    @commands.slash_command()
    async def game(self, ctx):
        print("t")
        data = await self.fetch_player(ctx, ctx.author.id, ctx.guild.id)
        if data == 404:
            return
        
        url = await self.generate(ctx.author.id)

        embed = discord.Embed(title=_("Current game state :"))
        embed.set_image(url=url)

        game = await self.fetch_game(ctx, ctx.guild.id)

        view = tt_views.GameOverviewView(self, ctx, data)

        message = await ctx.respond(embed=embed, view=view)
        await view.wait()
        await ctx.interaction.response.edit_message(view=view)

    @commands.slash_command(guild_ids=[613018525111549953])
    async def register(self, ctx: discord.ApplicationContext):
        print("t")
        if not await self.create_player(ctx.guild.id, ctx.author):
            await ctx.respond("You are already registered")
        else:
            await ctx.respond("Vous êtes inscrit !")


    @commands.slash_command()
    async def vote(self, ctx, player: discord.Member):
        data = await self.fetch_player(ctx, ctx.author.id, ctx.guild.id, run_checks=False)
        target = await self.fetch_player(ctx, player.id, ctx.guild.id, run_checks=False)
        game = await self.fetch_game(ctx, ctx.guild.id)

        if data == 404:
            await ctx.respond("You are not in the game.", ephemeral=True)
            return
        
        if target == 404:
            await ctx.respond("The player you're trying to vote for isn't in the game.", ephemeral=True)
            return
        target = target[0]
        data = data[0]
        if target["is_dead"] == True:
            await ctx.respond("The player you're trying to vote for is dead.", ephemeral=True)
            return

        if data["is_dead"] == False:
            await ctx.respond("Only dead players can vote.", ephemeral=True)
            return

        if data["ad_vote"] != None:
            await ctx.respond("You already voted today.", ephemeral=True)
            return

        url = self.get_api_url("guild") + "/" + str(ctx.guild.id) + "/" + "players" + "/" + str(ctx.author.id) + "/" + "vote"
        data = {"target_id": player.id}
        async with self.session.get(url, json=data) as resp:
            reply = await resp.json()
            if resp.status == 200:
                await ctx.respond("Vote done.\n")
                await self.log(game, f"{data['name']} voted for {target['name']}. {target['name']} now has {reply['vote_number']} votes today.")
        