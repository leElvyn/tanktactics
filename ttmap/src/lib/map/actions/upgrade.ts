
import { MoveEvent, UpgradeEvent } from "../interfaces";
import { redrawPlayer } from "../mapDrawing";
import { TILE_SIZE } from "../mapMain";
import anime from "../anime"
import { notifyMe } from "../notifications";

export async function upgradeRange(event: UpgradeEvent) {
    let position_string = event.player.tank.x + "_" + event.player.tank.y
    let playerCanvas = <HTMLCanvasElement> document.getElementById("player_" + position_string);
    let rangeDiv = document.getElementById("range_" + position_string);
    
    notifyMe(`${event.player.name} just upgraded their range.\n${event.player.name} now has a ${event.new_range} tiles range.`)

    setTimeout(() => {
        redrawPlayer(playerCanvas.getContext("2d"), event.player);
    }, 400);

    await anime({
        targets: rangeDiv,
        width: (event.new_range * 2  + 1)*  TILE_SIZE + "px",
        height: (event.new_range * 2 + 1) * TILE_SIZE + "px",
        left: (event.player.tank.x - event.new_range) * TILE_SIZE + "px",
        top: (event.player.tank.y - event.new_range) * TILE_SIZE + "px",
        duration: 1000
    }).finished

}