import { TILE_SIZE } from "./script.js";
import anime from "./anime.js";
export function movePlayer(event) {
    let position_string = event.position.x + "_" + event.position.y;
    let playerCanvas = document.getElementById("player_" + position_string);
    let rangeDiv = document.getElementById("range_" + position_string);
    let move_x = event.direction.x;
    let move_y = event.direction.y;
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
}
export function shootPlayer() {
}
