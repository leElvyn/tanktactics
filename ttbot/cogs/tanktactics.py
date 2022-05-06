import discord
from discord import Interaction, app_commands
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

        self.bot: commands.Bot = bot
        self.browser = None
        super().__init__()

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

        print('TankTactics is ready.')

    async def generate(self, focus_id):
        page = await self.browser.newPage()
        await page.setViewport({"width":1024, "height":1024})
        if focus_id != False:
            await page.goto(f'http://127.0.0.1:8000/map/guild/869906440268173333?focus_player_id={focus_id}')
        else:
            await page.goto(f'http://127.0.0.1:8000/map/guild/869906440268173333')

        await asyncio.sleep(0.3) #it sometimes blur, making sure it REALLy is loaded

        image_name = str(datetime.datetime.utcnow().timestamp())
        image_name = image_name.replace('.', '-') # to avoid problems with dots in file names
        image_name += '.png'
        image_path = os.getcwd() + 'tanktactics/static/static/staticmaps/' + image_name
        await page.screenshot({'path': image_path, "width":1024, "height":1024})
        await page.close()
        image_bin = open(image_path, 'rb')

        image_url = "https://tank-tactics.com/staticmaps/" + image_name
        return image_url

    async def fetch_player(self, interaction, player_id, guild_id, run_checks=True):
        async with self.session.get(self.get_api_url(f'guild/{guild_id}/players/{player_id}')) as response:
            if response.status == 404:
                await interaction.followup.send("You are not in the game")
                return 404
            player = await response.json()
            if player["is_dead"] == True and run_checks:
                await interaction.followup.send("You are dead")
                return False

            if player["tank"]["action_points"] <= 0:
                ## await interaction.respond("You are out of action points.")
                # here, is_disabled is true
                return (player, True)
        return (player, False)

    async def fetch_player_raw(self, player_id, guild_id):
        """fetch players without performing checks"""
        async with self.session.get(self.get_api_url(f'guild/{guild_id}/players/{player_id}')) as response:
            player = await response.json()
        
        return player

    async def fetch_game(self, interaction, guild_id):
        async with self.session.get(self.get_api_url(f'guild/{guild_id}')) as response:

            game = await response.json()
        return game

    async def create_player(self, guild_id, player: discord.Member):
        async with self.session.post(self.get_api_url(f"guild/{guild_id}/players/create"), json={"discord_id": player.id, "name": player.name, "avatar_url": player.avatar.url}) as response:
            if response.status == 201:
                return True
            else:
                return False

    async def log(self, game, message):
        channel = await self.bot.fetch_channel(game["logs_channel"])
        await channel.send(message)

    @app_commands.command(name="move")
    async def move(self, interaction: Interaction):
        await interaction.response.defer()

        data = await self.fetch_player(interaction, interaction.user.id, interaction.guild.id)
        if data == 404:
            return

        url = await self.generate(interaction.user.id)

        game = await self.fetch_game(interaction, interaction.guild.id)
        if not game:
            return
        embed = discord.Embed(title=_("Current game state :"))
        embed.set_image(url=url)
        view = tt_views.MoveView(self, interaction, data, game)

        message = await interaction.followup.send(embed=embed, view=view)
        await view.wait()
        await interaction.edit_original_message(view=view)


    @app_commands.command(name="shoot")
    async def shoot(self, interaction: Interaction):
        await interaction.response.defer()

        data = await self.fetch_player(interaction, interaction.user.id, interaction.guild.id)
        if data == False:
            return
        
        url = await self.generate(interaction.user.id)

        embed = discord.Embed(title=_("Current game state :"))
        embed.set_image(url=url)

        game = await self.fetch_game(interaction, interaction.guild.id)

        view = tt_views.ShootView(self, interaction, data, game, is_friendly=False)

        await interaction.followup.send(embed=embed, view=view)

        await view.wait()
        await interaction.edit_original_message(view=view)


    @app_commands.command(name="transfer")
    async def transfer(self, interaction: Interaction):
        await interaction.response.defer()

        data = await self.fetch_player(interaction, interaction.user.id, interaction.guild.id)
        if data == 404:
            return

        url = await self.generate(interaction.user.id)

        embed = discord.Embed(title=_("Current game state :"))
        embed.set_image(url=url)

        game = await self.fetch_game(interaction, interaction.guild.id)

        view = tt_views.ShootView(self, interaction, data, game, is_friendly=True)

        message = await interaction.followup.send(embed=embed, view=view)
        await view.wait()
        await interaction.edit_original_message(view=view)

    @app_commands.command(name="upgrade")
    async def upgrade(self, interaction: Interaction):
        await interaction.response.defer()

        data = await self.fetch_player(interaction, interaction.user.id, interaction.guild.id)
        if not data:
            return
        
        url = await self.generate(interaction.user.id)

        embed = discord.Embed(title=_("Current game state :"))
        embed.set_image(url=url)

        game = await self.fetch_game(interaction, interaction.guild.id)

        view = tt_views.UpgradeRangeView(self, interaction, data, game)

        await interaction.followup.send(embed=embed, view=view)
        await view.wait()
        await interaction.edit_original_message(view=view)


    @app_commands.command(name="game")
    async def game(self, interaction: Interaction):
        await interaction.response.defer()

        data = await self.fetch_player(interaction, interaction.user.id, interaction.guild.id, False)
        if not data:
            url = await self.generate(False)
        else:
            url = await self.generate(interaction.user.id)


        embed = discord.Embed(title=_("Current game state :"))
        embed.set_image(url=url)
        if data:
            view = tt_views.GameOverviewView(self, interaction, data)
            await interaction.followup.send(embed=embed, view=view)
        else:
            await interaction.followup.send(embed=embed)




    @app_commands.command(name="register")
    async def register(self, interaction: Interaction):
        if not await self.create_player(interaction.guild.id, interaction.user):
            await interaction.response.send_message("An error occured during registration.")
        else:
            await interaction.response.send_message("You're registered !")


    @app_commands.command(name="vote")
    async def vote(self, interaction: Interaction, player: discord.Member):
        data = await self.fetch_player(interaction, interaction.user.id, interaction.guild.id, run_checks=False)
        target = await self.fetch_player(interaction, player.id, interaction.guild.id, run_checks=False)
        game = await self.fetch_game(interaction, interaction.guild.id)

        if data == 404:
            await interaction.followup.send("You are not in the game.", ephemeral=True)
            return
        
        if target == 404:
            await interaction.followup.send("The player you're trying to vote for isn't in the game.", ephemeral=True)
            return
        target = target[0]
        data = data[0]

        if target["is_dead"] == True:
            await interaction.followup.send("The player you're trying to vote for is dead.", ephemeral=True)
            return

        if data["is_dead"] == False:
            await interaction.followup.send("Only dead players can vote.", ephemeral=True)
            return

        if data["ad_vote"] != None:
            await interaction.followup.send("You already voted today.", ephemeral=True)
            return

        url = self.get_api_url("guild") + "/" + str(interaction.guild.id) + "/" + "players" + "/" + str(interaction.user.id) + "/" + "vote"
        json_data = {"target_id": player.id}
        async with self.session.get(url, json=json_data) as resp:
            reply = await resp.json()
            if resp.status == 200:
                print(data, target)
                await interaction.response.send_message("Vote done.\n")
                await self.log(game, f"{data['name']} voted for {target['name']}.\n{target['name']} now has {reply['vote_number']} vote(s) today.")
        
