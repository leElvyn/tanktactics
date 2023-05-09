# tanktactics
A full stack ultra minimalistic massively multiplayer online game, with a discord bot and a live map on a website.

This project is composed of 3 parts : 

### The bot :

A discord.py bot that allows players to interact with the game on a discord server.

### The backend : 

A django app that manages tasks actions, and the database.

### The frontend :
aka "the map"

A TS app to view the current state of the game. It gets compiled to JS in the [/ttdashboard/map/static/map/map_static](https://github.com/leElvyn/tanktactics/tree/master/ttdashboard/map/static/map/map_static) dir.


# Usage

This project builds cleanly with docker compose. Just copy `docker-compose.dev.yml` to `docker-compose.yml` and launch with `docker compose up`. Add `-d` to daemonize your add and run it in the background.

Do the same with `docker-compose.prod.yml` for the production environment. Make sure to fill all keys correctly.

# Special Thanks 

Thanks a lot to Luke Muscat (@pgmuscat) for the original rules of the game, and allowing me to use them.
