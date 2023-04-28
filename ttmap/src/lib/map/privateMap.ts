import { TILE_SIZE } from "./mapMain.js"

export function focusMap(map: HTMLElement, grid_size_x: number, grid_size_y: number) {
    document.getElementById("background").style.background = "#333333"
    // @ts-ignored
    let focusObj = JSON.parse(focus);
    let focusCanvas = document.getElementById("player_" + focusObj.x + "_" + focusObj.y)

    let bodyRect = document.getElementById("background").getBoundingClientRect();
    map.style.transform = `scale(${calculateScale(grid_size_x, grid_size_y, focusObj.range)})`

    let playerRect = focusCanvas.getBoundingClientRect();

    let pageCenterX = bodyRect.width / 2
    let pageCenterY = bodyRect.height / 2

    let missingLengthX = pageCenterX - playerRect.x
    let missingLengthY = pageCenterY - playerRect.y

    map.style.left = parseInt(map.style.left) + missingLengthX + "px" 
    map.style.top = parseInt(map.style.top) + missingLengthY + "px" 

    if (missingLengthX > 0) {
        map.style.left = parseInt(map.style.left) - 25 + "px"
    }
    else {
        map.style.left = parseInt(map.style.left) + 25 + "px"
    }
    if (missingLengthY > 0) {
        map.style.top = parseInt(map.style.top) - 25 + "px"
    }
    else {
        map.style.top = parseInt(map.style.top) + 25 + "px"
    }

}

function calculateScale(grid_size_x, grid_size_y, range) {
    return (6.5 - Math.sqrt(range)) / 3;
}