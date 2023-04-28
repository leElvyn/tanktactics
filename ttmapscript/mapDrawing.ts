import { Game, Player } from "./interfaces";
import { TILE_SIZE } from "./mapMain.js";

var heartRed = new Image();
heartRed.src = "/src/assets/heart-red.png"

var heartBlack = new Image();
heartBlack.src = "/src/assets/heart-black.png"


export async function drawMap(map: HTMLElement, game) {
    // await fetchGame()
    drawGrid(map, game)
    drawPlayers(map, game)
    drawRangeRepresentations(map, game)

    centerMap(map)

}

function waitForStaticLoad(element: HTMLImageElement) {
    return new Promise(resolve => element.onload = resolve);
}

function parseReviver(key, value) {
    if (typeof value === 'string' && key == "guild_id") {
        return BigInt(value);
    }
    return value;
}

export async function fetchGame(url: string) {
    const response = await fetch(url)

    // come on JS, go home. You're drunk
    
    return JSON.parse(await response.text(), parseReviver)
}
function drawGrid(map: HTMLElement, game: Game) {
    for (var i = 0; i <= game.grid_size_y; i++) {

        //var row = document.createElement("div");
        //row.className = "row";
        //map.appendChild(row);
        for (var j = 0; j <= game.grid_size_x; j++) {
            var tile = document.createElement("div");
            tile.className = "tile";
            tile.id = "tile_" + j.toString() + "_" + i.toString();
            tile.setAttribute("coordinate", j.toString() + "_" + i.toString());
            tile.style.top = i * TILE_SIZE + "px";
            tile.style.left = j * TILE_SIZE + "px";
            map.appendChild(tile);
        }
    }
    map.style.width = (game.grid_size_x + 1) * TILE_SIZE + "px";
    map.style.height = (game.grid_size_y + 1) * TILE_SIZE + "px";
    map.style.clip = `rect(0, ${map.style.width}, ${map.style.height}, 0)`;
}

function drawPlayers(map: HTMLElement, game: Game) {
    for (let i = 0; i < game.players.length; i++) {
        let player = game.players[i];
        if (player.is_dead) {
            continue
        }
        let tile = document.getElementById("tile_" + player.tank.x.toString() + "_" + player.tank.y.toString());
        let canvas = document.createElement("canvas");
        canvas.setAttribute("height", "512");
        canvas.setAttribute("width", "512");
        canvas.className = "player-canvas";
        let ctx = canvas.getContext("2d");
        drawPlayer(player, ctx);
        canvas.id = "player_" + player.tank.x.toString() + "_" + player.tank.y.toString();
        canvas.setAttribute("coordinate", player.tank.x.toString() + "_" + player.tank.y.toString());
        canvas.style.top = tile.style.top;
        canvas.style.left = tile.style.left;
        map.appendChild(canvas);
    }
}

function drawPlayer(player: Player, ctx: CanvasRenderingContext2D) {

    ctx.fillStyle = "rgb(52, 201, 182)";
    ctx.fillRect(156, 156, 200, 200);

    //drawRangeRepresentation(ctx, player.tank.range, player.player_color);
    ctx.globalAlpha = 1;
    ctx.fillStyle = "rgb(220, 220, 220)";
    ctx.textAlign = "center";
    ctx.font = "bold 80px Arial";
    ctx.fillText(player.name, 256, 110);
    drawHeart(ctx, player.tank.health_points);
    drawActionPoints(ctx, player.tank.action_points);
    drawRange(ctx, player.tank.range);
}

function drawActionPoints(ctx: CanvasRenderingContext2D, number: number) {
    ctx.font = "bold 80px Arial";
    ctx.textAlign = "center";
    ctx.fillStyle = "rgb(78, 255, 60)";
    ctx.beginPath();
    ctx.arc(90, 256, 60, 0, 2 * Math.PI);
    ctx.fill();
    ctx.fillStyle = "rgb(70, 70, 70)";
    ctx.fillText(number.toString(), 90, 284);
}
function drawRange(ctx: CanvasRenderingContext2D, number: number) {
    ctx.font = "bold 80px Arial";
    ctx.textAlign = "center";
    ctx.fillStyle = "#FFED4D";
    ctx.fillRect(370, 200, 112, 112);
    ctx.fillStyle = "rgb(70, 70, 70)";
    ctx.fillText(number.toString(), 427, 288);
}

function drawHeart(ctx: CanvasRenderingContext2D, numberAlive: number) {
    for (var i = 1; i <= 3; i++) {
        if (numberAlive < i) {
            ctx.drawImage(heartBlack, (5 + i * 100), 380, 90, 90);
        }
        else {
            ctx.drawImage(heartRed, (5 + i * 100), 380, 90, 90);
        }
    }
}
function centerMap(map: HTMLElement) {
    let bodyRect = document.getElementById("background").getBoundingClientRect();
    let rect = map.getBoundingClientRect();
    map.style.left = bodyRect.width / 2 - rect.width / 2 + "px";
    map.style.top = bodyRect.height / 2 - rect.height / 2 + "px";
}

function drawRangeRepresentations(map: HTMLElement, game: Game) {
    for (let i = 0; i < game.players.length; i++) {
        let player = game.players[i];
        if (player.is_dead) {
            continue
        }
        let rangeDiv = drawRangeRepresentation(player.tank.range, player.player_color);
        let range = player.tank.range;
        rangeDiv.style.left = (player.tank.x - range) * TILE_SIZE + "px";
        rangeDiv.style.top = ( player.tank.y - range) * TILE_SIZE + "px";

        rangeDiv.id = "range_" + player.tank.x.toString() + "_" + player.tank.y.toString();
        map.appendChild(rangeDiv);
    }
}

function drawRangeRepresentation(range: number, color: string): HTMLElement {
    let rangeDiv = document.createElement("div");
    rangeDiv.className = "range";
    rangeDiv.style.width = (range * 2  + 1)*  TILE_SIZE + "px";
    rangeDiv.style.height = (range * 2 + 1) * TILE_SIZE + "px";
    let new_col = color.replace(/rgb/i, "rgba");
    new_col = new_col.replace(/\)/i,',0.3)');
    rangeDiv.style.backgroundColor = new_col;
    return rangeDiv
}

export function redrawPlayer(canvas: CanvasRenderingContext2D, player: Player) {
    canvas.clearRect(0, 0, canvas.canvas.width, canvas.canvas.height);
    drawPlayer(player, canvas);
}