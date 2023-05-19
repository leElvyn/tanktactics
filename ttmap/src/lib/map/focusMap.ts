
interface Focus {
    x: number,
    y: number,
    range: number,
}

export function focusMap(map: HTMLElement, grid_size_x: number, grid_size_y: number, focus: Focus) {
    let focusCanvas = document.getElementById("player_" + focus.x + "_" + focus.y)

    let bodyRect = document.getElementById("body")!.getBoundingClientRect();
    map.style.transform = `scale(${calculateScale(grid_size_x, grid_size_y, focus.range)})`

    let playerRect = focusCanvas!.getBoundingClientRect();

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

function calculateScale(grid_size_x: number, grid_size_y: number, range: number) {
    return (6.5 - Math.sqrt(range)) / 3;
}