import { registerGestures } from "./mapMouvement.js";
import { drawMap, fetchGame } from "./mapDrawing.js";
import { registerInteractions } from "./mapInteractions.js"
import { createSocket } from "./socket.js";
import { Game } from "./interfaces.js";
import { focusMap } from "./privateMap.js";

export const TILE_SIZE = 50;

var map = document.getElementById("map");

var game: Game;

async function main(map: HTMLElement) {
    registerGestures(map);
    game = await fetchGame()
    await drawMap(map, game);
    
    await registerInteractions(map)

    // @ts-ignore
    if (is_public) {
        await createSocket(game, map)
    }
    else {
        document.getElementById("background").style.background = "#333333"
    }
    // @ts-ignore
    if (is_focused) {
        focusMap(map, game.grid_size_x, game.grid_size_y)
    }
}

main(map)


