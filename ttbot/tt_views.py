from discord.ext import commands

import discord
from discord.interactions import Interaction
from discord.ui import Button, View, Select
from discord.components import ActionRow
from discord import ButtonStyle, SelectOption, SelectMenu

def get_distance(tank_offender, tank_defender):
    """return the distance between the 2 tanks"""
    return max(abs((tank_offender["x"] - tank_defender["x"])), abs((tank_offender["y"] - tank_defender["y"])))

def filter_range_players(players, player_x, player_y, range):
    range_players = []
    for player in players:
        if player["is_dead"]:
            continue
        tank = player["tank"]
        distance = get_distance({"x": player_x, "y": player_y}, tank)
        if distance <= range and distance != 0:
            # th != 0 is to exclude the player himself
            range_players.append(player)
    return range_players

class Confirm(View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        print(interaction)
        print(type(interaction))
        self.value = True
        await interaction.response.pong()
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        await interaction.response.pong()
        self.stop()

class EmptyButton(Button):
    def __init__(self, row) -> None:
        #number is used to return the result of the user input
        super().__init__(style=ButtonStyle.gray, label="\u200b", disabled=True, row=row)
    
    async def callback(self, interaction: discord.Interaction):
        raise Exception("This button should never be clicked")

class ArrowButton(Button):
    def __init__(self, style, label, emoji, direction, row, disabled) -> None:
        #number is used to return the result of the user input
        super().__init__(style=style, label=label, emoji=emoji, row=row, disabled=disabled)
        self.direction = direction
    
    async def callback(self, interaction: discord.Interaction):
        if self.view.author != interaction.user:
            return
        cog = self.view.cog
        ctx = self.view.ctx
        url = cog.get_api_url("guild") + "/" + str(ctx.guild.id) + "/" + "players" + "/" + str(ctx.user.id)
        current_coordinates = {}
        # we start by getting the current users's coordinates
        async with cog.session.get(url) as resp:
            data = await resp.json()

            current_coordinates["x"] = data["tank"]["x"]
            current_coordinates["y"] = data["tank"]["y"]
        if self.direction == 0:
            current_coordinates["y"] -= 1
        elif self.direction == 1:
            current_coordinates["x"] += 1
        elif self.direction == 2:
            current_coordinates["y"] += 1
        elif self.direction == 3:
            current_coordinates["x"] -= 1
        
        # we then send the new coordinates to the server
        url = url + "/move"
        async with cog.session.get(url, json=current_coordinates) as resp:
            if resp.status != 200:
                raise Exception("Error while moving tank")
        await interaction.response.send_message(f"You moved your tank to {current_coordinates['x']}/{current_coordinates['y']}")
        await cog.log(self.view.game, f"<@{ctx.user.id}> moved his tank to {current_coordinates['x']}/{current_coordinates['y']}") 
        self.view.disable_all_arrows()
        self.view.stop()

class ActionPointsButton(Button):
    def __init__(self, row, ap_number, emojis_ids) -> None:
        
        ap_emoji_id = emojis_ids.get(f"ap{ap_number}")

        if ap_emoji_id is None:
            super().__init__(style=ButtonStyle.blurple, label=ap_number, disabled=False, row=row)
            return
        
        emoji = discord.PartialEmoji(id=ap_emoji_id, name=f"ap{ap_number}")

        super().__init__(style=ButtonStyle.blurple, label="\u200b", emoji=emoji, row=row, disabled=False)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.pong()
        
class RangeButton(Button):
    def __init__(self, row, range_value, emojis_ids) -> None:
        
        ap_emoji_id = emojis_ids.get(f"range{range_value}")

        if ap_emoji_id is None:
            super().__init__(style=ButtonStyle.blurple, label=range_value, disabled=False, row=row)
            return
        
        emoji = discord.PartialEmoji(id=ap_emoji_id, name=f"ap{range_value}")

        super().__init__(style=ButtonStyle.blurple, label="\u200b", emoji=emoji, row=row, disabled=False)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.pong()

class LifeButton(Button):
    def __init__(self, row, life_value) -> None:
        label = ""
        red_heart = "❤️ "
        black_heart = "🖤 "
        for i in range(3):
            if i < life_value:
                label += red_heart
            else:
                label += black_heart
        super().__init__(style=ButtonStyle.blurple, label=label, row=row, disabled=False)
        
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.pong()

class TextButton(Button):
    def __init__(self, row, text) -> None:
        super().__init__(style=ButtonStyle.blurple, label=text, disabled=False, row=row)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.pong()

class RangeUpgradeButton(Button):
    def __init__(self, range_value, disabled, emojis_ids, row) -> None:
        self.range_value = range_value
        
        ap_emoji_id = emojis_ids.get(f"range{range_value - 1}")

        if ap_emoji_id is None:
            super().__init__(style=ButtonStyle.green, label=range_value-1, disabled=disabled, row=row)
            return
        
        emoji = discord.PartialEmoji(id=ap_emoji_id, name=f"ap{range_value}")

        super().__init__(style=ButtonStyle.green, label="\u200b", emoji=emoji, row=row, disabled=disabled)
    async def callback(self, interaction: discord.Interaction):
        await self.view.range_upgrade_button_callback(self.range_value, interaction)
        self.disabled = True
        self.view.stop()

class NoActionPointsButton(Button):
    def __init__(self, row) -> None:
        super().__init__(style=ButtonStyle.danger, label="You're out of action points !", disabled=False, row=row)

class NearPlayerSelect(Select):
    is_friendly = None
    def __init__(self, player_list, is_disabled, is_friendly):
        self.is_friendly = is_friendly
        options = []
        for player in player_list:
            options.append(SelectOption(label=player["name"], value=player["discord_id"]))

        if is_disabled:
            placeholder = "You're out of action points !"

        elif len(player_list) == 0:
            placeholder = "There is no players in range !"
            is_disabled = True

        else:
            placeholder = "Select a player within your range." 
        
        if len(options) == 0:
            #make sure that there is always at least one placeholder
            options.append(SelectOption(label="No players in range"))

        super().__init__(min_values=1, max_values=1, options=options, placeholder=placeholder, disabled=is_disabled)

    async def callback(self, interaction: Interaction):
        if self.view.author != interaction.user:
            return

        if self.is_friendly:
            self.view.selected_player = self.values[0]
            self.view.add_select()
            await interaction.response.edit_message(view=self.view)
            return 

        cog = self.view.cog
        ctx = self.view.ctx
        url = cog.get_api_url("guild") + "/" + str(ctx.guild.id) + "/" + "players" + "/" + str(ctx.user.id) + "/" + "attack"
        data = {"defender_id": self.values[0]}
        target_member = await ctx.guild.fetch_member(self.values[0])
        async with cog.session.get(url, json=data) as resp:
            reply = await resp.json()
            if resp.status == 200:
                self.view.disable_all_selects()
                await interaction.response.send_message("Bang.\n")
                log_message = f"<@{ctx.user.id}> attacked <@{target_member.id}>.\n"
                if reply["defensive_player_dead"]:
                    log_message += f"<@{self.values[0]}> is now dead. "
                else:
                    log_message += f"<@{self.values[0]}> now has " + str(reply["defender_health"]) + " reaming health points."
                await cog.log(self.view.game, log_message)
                self.view.stop()


class NumberSelect(Select):
    def __init__(self, ap_number, placeholder, disabled=False):
        if ap_number > 25:
            ap_number = 25
        options = [SelectOption(label=i) for i in range(1, ap_number + 1)]
        super().__init__(min_values=1, max_values=1, options=options, placeholder=placeholder, disabled=disabled)

    async def callback(self, interaction: Interaction):
        await self.view.number_select_callback(self.values[0], interaction)
        self.view.disable_all_selects()
        self.view.stop()
    

class MoveView(View):
    """Directions : 
        0: up
        1: right
        2: down
        3: down
        """
    direction = None
    interaction = None 
    author = None
    game = None
    
    def __init__(self, cog_object, ctx: Interaction, player_data, game_data):
        super().__init__(timeout=500)
        self.author = ctx.user
        self.cog = cog_object
        self.ctx = ctx
        self.game = game_data
        emojis_ids = cog_object.emojis_ids
        is_disabled = player_data[1]
        player_data = player_data[0]
        
        self.add_item(EmptyButton(row=0))
        self.add_item(ArrowButton(style=ButtonStyle.blurple, label="\u200b", emoji=discord.PartialEmoji(id=860123643715125279, name="uparrow"), direction=0, row=0, disabled=(is_disabled or (player_data["tank"]["y"] == 0))))
        self.add_item(EmptyButton(row=0))
        self.add_item(TextButton(row=0, text="Action Points : "))
        self.add_item(ActionPointsButton(row=0, ap_number=player_data["tank"]["action_points"], emojis_ids=emojis_ids))
        
        self.add_item(ArrowButton(style=ButtonStyle.blurple, label="\u200b", emoji=discord.PartialEmoji(id=860123643816312852, name="leftarrow"), direction=3, row=1, disabled=(is_disabled or (player_data["tank"]["x"] == 0))))
        self.add_item(EmptyButton(row=1))
        self.add_item(ArrowButton(style=ButtonStyle.blurple, label="\u200b", emoji=discord.PartialEmoji(id=859388126653186058, name="rightarrow"), direction=1, row=1, disabled=(is_disabled or (player_data["tank"]["x"] == game_data["grid_size_x"]))))
        self.add_item(TextButton(row=1, text="Player Range : \u180e"))
        self.add_item(RangeButton(row=1, range_value=player_data["tank"]["range"], emojis_ids=emojis_ids))
        
        self.add_item(EmptyButton(row=2))
        self.add_item(ArrowButton(style=ButtonStyle.blurple, label="\u200b", emoji=discord.PartialEmoji(id=860123643300675605, name="downarrow"), direction=2, row=2, disabled=(is_disabled or (player_data["tank"]["y"] == game_data["grid_size_y"]))))
        self.add_item(EmptyButton(row=2))
        self.add_item(TextButton(row=2, text="Health :⠀"))
        self.add_item(LifeButton(row=2, life_value=player_data["tank"]["health_points"]))

        if is_disabled:
            self.add_item(NoActionPointsButton(row=3))

    def disable_all_arrows(self):
        for item in self.children:
            if isinstance(item, ArrowButton):
                item.disabled = True

class ShootView(View):
    """This View handles both shoot and transfer. is_friendly is the parameter. if friendly, when selecting someone, it ads a select for the number of AP to transfer """
    author = None
    player_dict = None
    cog = None
    ctx: discord.ext.commands.Context = None
    def __init__(self, cog_object, ctx, player_data, game_players, is_friendly):
        super().__init__(timeout=500)
        self.cog = cog_object
        self.ctx = ctx
        self.author = ctx.user
        emojis_ids = cog_object.emojis_ids
        
        is_disabled = player_data[1]
        player_data = player_data[0]

        self.player_dict = player_data
        self.game = game_players
        game_players = game_players["players"]
        
        self.add_item(TextButton(row=0, text="Action Points : "))
        self.add_item(ActionPointsButton(row=0, ap_number=player_data["tank"]["action_points"], emojis_ids=emojis_ids))

        self.add_item(TextButton(row=1, text="Player Range : \u180e"))
        self.add_item(RangeButton(row=1, range_value=player_data["tank"]["range"], emojis_ids=emojis_ids))
        
        self.add_item(TextButton(row=2, text="Health :⠀"))
        self.add_item(LifeButton(row=2, life_value=player_data["tank"]["health_points"]))

        players_list = filter_range_players(game_players,player_data["tank"]["x"], player_data["tank"]["y"] , player_data["tank"]["range"])

        self.add_item(NearPlayerSelect(player_list=players_list, is_disabled=is_disabled, is_friendly=is_friendly))

    def add_select(self):
        ap_number = self.player_dict["tank"]["action_points"]
        # we check if the select is already in the view
        for item in self.children:
            if isinstance(item, NumberSelect):
                self.remove_item(item)
        self.add_item(NumberSelect(ap_number=ap_number, placeholder="Select a number of Action Points to transfer."))

    async def number_select_callback(self, ap_number, interaction: discord.Interaction):
        """called by the Select. It is the end of the tranfer flow."""
        cog = self.cog
        ctx = self.ctx
        url = cog.get_api_url("guild") + "/" + str(ctx.guild.id) + "/" + "players" + "/" + str(ctx.user.id) + "/" + "transfer"
        print(self.selected_player)
        data = {"ap_number": int(ap_number), "defender_id": self.selected_player}
        selected_member = ctx.guild.get_member(self.selected_player)
        print(selected_member)
        async with cog.session.get(url, json=data) as resp:
            reply = await resp.json()
            if resp.status == 200:
                await cog.log(self.game, "Player {} transfered {} AP to <@{}>".format(ctx.user.name, ap_number, self.selected_player))
                await interaction.response.send_message("Transfer done.\n")
    
    def disable_all_selects(self):
        for item in self.children:
            if isinstance(item, NumberSelect) or isinstance(item, NearPlayerSelect):
                item.disabled = True


class UpgradeRangeView(View):
    """This View handles the upgrade of the range"""
    def __init__(self, cog_object, ctx , player_data, game):
        super().__init__(timeout=500)
        self.cog = cog_object
        self.ctx = ctx
        self.game = game
        self.author = ctx.user
        emojis_ids = cog_object.emojis_ids
        player_data = player_data[0]
        print(player_data["tank"]["range"])
        print(player_data["tank"]["action_points"])
        is_disabled = player_data["tank"]["action_points"] < (player_data["tank"]["range"] - 1)
        print(is_disabled)
        
        self.add_item(TextButton(row=0, text="Action Points : "))
        self.add_item(ActionPointsButton(row=0, ap_number=player_data["tank"]["action_points"], emojis_ids=emojis_ids))

        self.add_item(TextButton(row=1, text="Player Range : \u180e"))
        self.add_item(RangeButton(row=1, range_value=player_data["tank"]["range"], emojis_ids=emojis_ids))
        
        self.add_item(TextButton(row=2, text="Health :⠀"))
        self.add_item(LifeButton(row=2, life_value=player_data["tank"]["health_points"]))


        self.add_item(RangeUpgradeButton(row=3, range_value=player_data["tank"]["range"], disabled=is_disabled, emojis_ids=emojis_ids))

    def disable_all_selects(self):
        for item in self.children:
            if isinstance(item, NumberSelect):
                item.disabled = True

    async def range_upgrade_button_callback(self, current_range, interaction: discord.Interaction):
        """called by the Select. It is the end of the tranfer flow."""
        cog = self.cog
        ctx = self.ctx
        confirm_view = Confirm()
        followup = interaction.followup
        mess = await interaction.response.send_message(f"Are you sure you want to upgrade your range by 1 tile for {current_range - 1} action points ?", ephemeral=True, view=confirm_view)
        await confirm_view.wait()
        print(confirm_view.value)
        if confirm_view.value is None:
            return
        elif not confirm_view.value:
            return
        url = cog.get_api_url("guild") + "/" + str(ctx.guild.id) + "/" + "players" + "/" + str(ctx.user.id) + "/" + "upgrade"
        data = {"upgrade_size": 1}
        async with cog.session.get(url, json=data) as resp:
            reply = await resp.json()
            if resp.status == 200:
                self.disable_all_selects()
                self.stop()
                await followup.send("Range upgraded.\n")
                print(self.author)
                print(type(self.author))
                await cog.log(self.game, f"{self.author} upgraded his range to {current_range+1} tiles.")
                

class GameOverviewView(View):
    """This View handles the upgrade of the range"""
    def __init__(self, cog_object, ctx, player_data):
        super().__init__(timeout=500)
        self.cog = cog_object
        self.ctx = ctx
        self.author = ctx.user
        emojis_ids = cog_object.emojis_ids
        is_disabled = player_data[1]
        player_data = player_data[0]
        
        self.add_item(TextButton(row=0, text="Action Points : "))
        self.add_item(ActionPointsButton(row=0, ap_number=player_data["tank"]["action_points"], emojis_ids=emojis_ids))

        self.add_item(TextButton(row=1, text="Player Range : \u180e"))
        self.add_item(RangeButton(row=1, range_value=player_data["tank"]["range"], emojis_ids=emojis_ids))
        
        self.add_item(TextButton(row=2, text="Health :⠀"))
        self.add_item(LifeButton(row=2, life_value=player_data["tank"]["health_points"]))


        if is_disabled:
            self.add_item(NoActionPointsButton(row=3))