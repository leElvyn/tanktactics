import type { MoveEvent } from "../interfaces";
import { TILE_SIZE } from "$lib/consts";
import anime from "animejs"

export function movePlayer(event: MoveEvent) {
    let position_string = event.position.x + "_" + event.position.y
    let playerCanvas = <HTMLCanvasElement> document.getElementById("player_" + position_string);
    let rangeDiv = document.getElementById("range_" + position_string);

    let move_x = event.direction.x
    let move_y = event.direction.y

    if (move_x == 1 || move_x == -1) {
        anime({
            targets: "#player_" + position_string,
            left: (event.position.x + move_x) * TILE_SIZE,
            duration: 1000,
            easing: "easeInOutSine"
        });
        anime({
            targets: "#range_" + position_string,
            left: (event.position.x + move_x - event.player.tank.range) * TILE_SIZE,
            duration: 1000,
            easing: "easeInOutSine"
        });
    }
    if (move_y == 1 || move_y == -1) {
        anime({
            targets: "#player_" + position_string,
            top: (event.position.y + move_y) * TILE_SIZE,
            duration: 1000,
            easing: "easeInOutSine"
        });
        anime({
            targets: "#range_" + position_string,
            top: (event.position.x + move_y - event.player.tank.range) * TILE_SIZE,
            duration: 1000,
            easing: "easeInOutSine"
        });
    }
    // redrawPlayer(playerCanvas.getContext("2d"), event.player);
    let new_position = (event.position.x + event.direction.x) + "_" + (event.position.y + event.direction.y);
    playerCanvas.id = "player_" + new_position;
    playerCanvas.setAttribute("position", new_position)
    rangeDiv!.id = "range_" + new_position;
    rangeDiv!.setAttribute("position", new_position)
}