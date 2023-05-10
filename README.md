# tanktactics

A full stack ultra minimalistic massively multiplayer online game, with a discord bot and a live map on a website.

This game requires players to form alliances and betray each other in other to try to be the last player remaining.

## Rules of the game

- each tank represents a player
- each tank has 3 HP
- every player receives 1 action point per day
- at any moment, a player can use an action point to either : 
  - move his tank of 1 tile
  - shoot a tank if he is in his range (your default range is 2 tiles, diagonal included), which will make him lose 1 HP. if a players loses all of his HPs, he’s eliminated
  - transfer action points to another player in range. This action has no cost
  - upgrade his range of 1 tile

- Every day, every eliminated player votes for the player they want to help. If a player has at least 3 votes, he receives 1 action point.

## The stack

### The bot :

A discord.py bot that allows players to interact with the game on a discord server.

*the bot isn't currently integrated to the stack, and needs fixes to account for the newer versions*

### The backend : 

A django app that manages tasks actions, and the database. Every actions requires sending a get or post request to the API. It also features a real time websocket, using django channels. This websocket sends map actions such as a player moving, upgrading it's range, shooting another player ...

### The frontend :
aka "the map"

This is a svelte kit app. It fetches the state of the game to the backend, and draws it in the frontend with canvas and div elements. The map has an absolute position and that position is changed when dragging the map around. 

When the page is loaded, a websocket connection is opened with the backend to display actions played live.

# Usage

This project builds cleanly with docker compose. Just copy `docker-compose.dev.yml` to `docker-compose.yml` and launch with `docker compose up`. Add `-d` to daemonize your add and run it in the background.

Do the same with `docker-compose.prod.yml` for the production environment. Make sure to fill all keys correctly.

# Special Thanks 

Thanks a lot to Luke Muscat (@pgmuscat) for the original rules of the game, and allowing me to use them.
