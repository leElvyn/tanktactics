import anime from "animejs";
import type { VoteEvent } from "../interfaces";

export async function vote(event: VoteEvent) {

    let map = document.getElementById("map");

    let recvPosition = event.receiving_player.tank.x + "_" + event.receiving_player.tank.y;

    let recvCanvas = <HTMLCanvasElement> document.getElementById("player_" + recvPosition);

    let hurtOverlay = document.createElement("div");

    hurtOverlay.style.width = "50px";
    hurtOverlay.style.height = "50px"
    hurtOverlay.style.left = recvCanvas.style.left;
    hurtOverlay.style.top = recvCanvas.style.top;
    hurtOverlay.style.position = "absolute";

    hurtOverlay.style.zIndex = "20"

    hurtOverlay.style.backgroundColor = "green";
    map!.appendChild(hurtOverlay);


    await anime({
        targets: hurtOverlay,
        opacity: [0.1, 0.6],
        loop: 6,
        duration: 200,
        direction: 'alternate',
        easing: "linear",
    }).finished;
    hurtOverlay.remove();
    
    // redrawPlayer(recvCanvas.getContext("2d"), event.receiving_player);
}