import { registerGestures } from "./mapMouvement.js";
import { drawMap, fetchGame } from "./mapDrawing.js";
import { registerInteractions } from "./mapInteractions.js"
import { gameStore } from "../stores/gameStore.js"
import { createSocket } from "./socket";
import { Game } from "./interfaces";

export const TILE_SIZE = 50;


export async function main(map: HTMLElement, game: Game) {
    registerGestures(map);


    await drawMap(map, game);

    await registerInteractions(map)

    await createSocket(game, map)
}



