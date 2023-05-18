import anime, { speed } from "animejs";
import type { ShootEvent } from "../interfaces";


export async function shootPlayer(event: ShootEvent) {
    console.log(event)
    // off = offensive player
    // def = defending player
    
    let offPosition = event.offensive_player.tank.x + "_" + event.offensive_player.tank.y;
    let defPosition = event.defensive_player.tank.x + "_" + event.defensive_player.tank.y;
    let offCanvas = <HTMLCanvasElement> document.getElementById("player_" + offPosition);
    let defCanvas = <HTMLCanvasElement> document.getElementById("player_" + defPosition);
    let offRangeDiv = document.getElementById("range_" + offPosition);
    let defRangeDiv = document.getElementById("range_" + defPosition);



    // HERE COMES THE MAAAAAATH

    let offCanvasCenter: [number, number] = [offCanvas.offsetLeft + offCanvas.offsetWidth / 2, offCanvas.offsetTop + offCanvas.offsetHeight / 2]
    let defCanvasCenter: [number, number] = [defCanvas.offsetLeft + defCanvas.offsetWidth / 2, defCanvas.offsetTop + defCanvas.offsetHeight / 2]

    let deltaX = offCanvasCenter[0] - defCanvasCenter[0];
    let deltaY = offCanvasCenter[1] - defCanvasCenter[1];
    var angle = Math.atan2(deltaY, deltaX) + (Math.PI / 2);

    let projectile = document.createElement("div");
    projectile.id = "proj_" + offPosition;
    projectile.style.width = "5px";
    projectile.style.height = "10px";
    
    projectile.style.left = offCanvasCenter[0] + "px";
    projectile.style.top = offCanvasCenter[1] + "px";

    projectile.style.position = "absolute";
    projectile.style.zIndex = "5";
    projectile.style.transform = `rotate(${angle}rad)`;

    projectile.style.backgroundColor = "red";
    let map = document.getElementById("map");
    map!.appendChild(projectile);

    await anime({
        targets: projectile,
        left: defCanvasCenter[0],
        top: defCanvasCenter[1],
        easing: "easeInOutCirc",
        duration: Math.sqrt(deltaX**2 + deltaY**2) * 10
    }).finished;

    projectile.remove();

    let hurtOverlay = document.createElement("div");

    hurtOverlay.style.width = "50px";
    hurtOverlay.style.height = "50px"
    hurtOverlay.style.left = defCanvas.style.left;
    hurtOverlay.style.top = defCanvas.style.top;
    hurtOverlay.style.position = "absolute";

    hurtOverlay.style.zIndex = "20"

    hurtOverlay.style.backgroundColor = "red";
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
    
    // redrawPlayer(defCanvas.getContext("2d"), event.defensive_player);
}