import { registerGestures } from "./mapMouvement.js";
import { drawMap, fetchGame } from "./mapDrawing.js";
import { registerInteractions } from "./mapInteractions.js";
import { createSocket } from "./socket.js";
import { focusMap } from "./privateMap.js";
export const TILE_SIZE = 50;
var map = document.getElementById("map");
var game;
import { upgradeRange } from "./actions.js";
async function main(map) {
    // DEBUG ONLY 
    // @ts-ignore
    window.upgradeRange = upgradeRange;
    window.map = map;
    registerGestures(map);
    game = await fetchGame();
    await drawMap(map, game);
    await registerInteractions(map);
    // @ts-ignore
    if (is_public) {
        await createSocket(game, map);
    }
    else {
        document.getElementById("background").style.background = "#333333";
    }
    // @ts-ignore
    if (is_focused) {
        focusMap(map, game.grid_size_x, game.grid_size_y);
    }
}
main(map);
