export async function registerInteractions(map : HTMLElement) {
    let players = document.getElementsByClassName("player-canvas")
    for (let player of players) {

        console.log("Yeh")
        player.addEventListener("mouseenter", canvasMouseEnter);
        player.addEventListener("mouseout", canvasMouseOut);
    }
}

function canvasMouseEnter(event: MouseEvent) {
    let element: HTMLElement = <HTMLElement> event.target;

    let range = document.getElementById("range_" + element.getAttribute("coordinate"));

    range.style.backgroundColor = range.style.backgroundColor.replace(/[^,]+(?=\))/, '0.8');
    //range.style.border = "7px solid rgb(5, 5, 5)";
    range.style.zIndex = "2";
}

function canvasMouseOut(event: MouseEvent) {
    let element = <HTMLElement> event.target;
    
    let range = document.getElementById("range_" + element.getAttribute("coordinate"));
    
    range.style.backgroundColor = range.style.backgroundColor.replace(/[^,]+(?=\))/, '0.2');
    //range.style.border = "3px solid rgb(5,5,5)";

    range.style.zIndex = "1";
}