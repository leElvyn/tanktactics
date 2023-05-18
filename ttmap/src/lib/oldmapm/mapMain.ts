import { registerGestures } from "./mapMouvement";
import { drawMap } from "./mapDrawing";
import { registerInteractions } from "./mapInteractions"
import { gameStore } from "../stores/gameStore"
import { createSocket } from "./socket";
import { Game } from "./interfaces";
import { transferToPlayer } from "./actions/transfer";

export const TILE_SIZE = 50;


export async function main(map: HTMLElement, game: Game) {
    
    //@ts-ignore
    window.transfer = transferToPlayer



    await drawMap(map, game);

}



