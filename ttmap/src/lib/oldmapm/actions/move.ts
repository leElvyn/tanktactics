import { MoveEvent } from "../interfaces";
import { redrawPlayer } from "../mapDrawing";
import { TILE_SIZE } from "../mapMain";
import anime from "../anime"

export function movePlayer(event: MoveEvent) {
    let position_string = event.position.x + "_" + event.position.y
    let playerCanvas = <HTMLCanvasElement> document.getElementById("player_" + position_string);
    let rangeDiv = document.getElementById("range_" + position_string);

    let move_x = parseInt(event.direction.x)
    let move_y = parseInt(event.direction.y)

    if (move_x == 1 || move_x == -1) {
        anime({
            targets: "#player_" + position_string,
            left: parseInt(playerCanvas.style.left) + TILE_SIZE * move_x,
            duration: 3000,
            easing: "easeInOutSine"
        });
        anime({
            targets: "#range_" + position_string,
            left: parseInt(rangeDiv.style.left) + TILE_SIZE * move_x,
            duration: 3000,
            easing: "easeInOutSine"
        });
    }
    if (move_y == 1 || move_y == -1) {
        anime({
            targets: "#player_" + position_string,
            top: parseInt(playerCanvas.style.top) + TILE_SIZE * move_y,
            duration: 3000,
            easing: "easeInOutSine"
        });
        anime({
            targets: "#range_" + position_string,
            top: parseInt(rangeDiv.style.top) + TILE_SIZE * move_y,
            duration: 3000,
            easing: "easeInOutSine"
        });
    }
    redrawPlayer(playerCanvas.getContext("2d"), event.player);
    let new_position = (parseInt(event.position.x) + event.direction.x) + "_" + (parseInt(event.position.y) + event.direction.y);
    playerCanvas.id = "player_" + new_position;
    playerCanvas.setAttribute("position", new_position)
    rangeDiv.id = "range_" + new_position;
    rangeDiv.setAttribute("position", new_position)
}