import { registerGestures } from "./mapMouvement.js";
import { drawMap, fetchGame } from "./mapDrawing.js";
import { registerInteractions } from "./mapInteractions.js"
import { createSocket } from "./socket.js";
import { Game } from "./interfaces.js";
import { movePlayer } from "./actions.js";

export const TILE_SIZE = 50;

var map = document.getElementById("map");

var game: Game;

async function main(map: HTMLElement) {
    registerGestures(map);
    game = await fetchGame()
    await drawMap(map, game);
    
    await registerInteractions(map)

    await createSocket(game, map)
}

main(map)


