import { registerGestures } from "./mapMouvement.js";
import { drawMap, fetchGame } from "./mapDrawing.js";
import { registerInteractions } from "./mapInteractions.js"
import { gameStore } from "../stores/gameStore.js"
import { createSocket } from "./socket";

export const TILE_SIZE = 50;


export async function main(map: HTMLElement) {
    registerGestures(map);

    let gameID = window.location.pathname.split("/")[2];
    let url = "/api/guild/" + gameID
    let game = await fetchGame(url)

    gameStore.set(game);

    await drawMap(map, game);

    await registerInteractions(map)

    await createSocket(game, map)
}



