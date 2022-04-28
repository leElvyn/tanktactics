import { TILE_SIZE } from "./script.js";
export function movePlayer(event) {
    let playerCanvas = document.getElementById("player_" + event.old_x + "_" + event.old_y);
    let rangeDiv = document.getElementById("range_" + event.old_x + "_" + event.old_y);
    let move_x = event.new_x - event.old_x;
    let move_y = event.new_y - event.old_y;
    let framesReaming = TILE_SIZE;
    animatePlayerMove();
    function animatePlayerMove() {
        console.log(event);
        if (move_x == 1 || move_x == -1) {
            playerCanvas.style.left = parseInt(playerCanvas.style.left) + 1 * move_x + "px";
            rangeDiv.style.left = parseInt(rangeDiv.style.left) + 1 * move_x + "px";
        }
        if (move_y == 1 || move_y == -1) {
            playerCanvas.style.top = parseInt(playerCanvas.style.top) + 1 * move_y + "px";
            rangeDiv.style.top = parseInt(rangeDiv.style.top) + 1 * move_y + "px";
        }
        if (framesReaming <= 0) {
            return;
        }
        framesReaming--;
        window.requestAnimationFrame(animatePlayerMove);
    }
}
export function shootPlayer() { }
//# sourceMappingURL=actions.js.map