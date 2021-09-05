var heartRed = new Image();
heartRed.src = "/static/map/public_map_static/assets/heart-red.png"

var heartBlack = new Image();
heartBlack.src = "/static/map/public_map_static/assets/heart-black.png"


function drawHeart(ctx, numberAlive) {
    for (var i = 1; i <= 3; i++) {
        if (numberAlive < i) {
            ctx.drawImage(heartBlack, (5 + i * 100), 380, 90, 90)
        }
        else {
            ctx.drawImage(heartRed, (5 + i * 100), 380, 90, 90)
        }
    }

}

function calculateInversePowerOf2(number) {
    var power = 0;
    while (number > 1) {
        number = number / 2;
        power++;
    }
    return power;
}

function drawActionPoints(ctx, number) {
    ctx.font = "bold 80px Arial";
    ctx.textAlign = "center";
    ctx.fillStyle = "rgb(78, 255, 60)";
    ctx.beginPath();
    ctx.arc(90, 256, 60, 0, 2 * Math.PI);
    ctx.fill();
    ctx.fillStyle = "rgb(70, 70, 70)";
    ctx.fillText(number, 90, 284);
}
function drawRange(ctx, number) {
    ctx.font = "bold 80px Arial";
    ctx.textAlign = "center";
    ctx.fillStyle = "#FFED4D";
    ctx.fillRect(370, 200, 112, 112);
    ctx.fillStyle = "rgb(70, 70, 70)";
    ctx.fillText(number, 427, 288);
}

function drawRangeRepresentation(ctx, range, color) {
    ctx.globalAlpha = 0.3;
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, 512, 512);
    ctx.globalAlpha = 1;
}

function drawPlayer(player, ctx) {
    //ctx.clearRect(0, 0, 512, 512);
    ctx.fillStyle = "rgb(52, 201, 182)";
    ctx.fillRect(156, 156, 200, 200);

    drawRangeRepresentation(ctx, player.tank.range, player.player_color);
    ctx.globalAlpha = 1;
    ctx.fillStyle = "rgb(40, 40, 40)";
    ctx.textAlign = "center";
    ctx.font = "bold 80px Arial";
    ctx.fillText(player.name, 256, 110);
    drawHeart(ctx, player.tank.health_points);
    drawActionPoints(ctx, player.tank.action_points);
    drawRange(ctx, player.tank.range);
}


/*
function drawRangeSurroundings(players, excluded_coordinates= [{x: -1, y: -1}]) {
    players.some(player => {
        if (player.is_dead) {
            return;
        }
        if (player.tank.x == excluded_coordinates[0].x && player.tank.y == excluded_coordinates[0].y) {
            return;
        }
        range = player.tank.range;
        for (var j = -range; j <= range; j++) {
            for (var k = -range; k <= range; k++) {
                if (j == 0 && k == 0) {
                }
                else if (player.tank.x + j < 0 || player.tank.x + j > map_x || player.tank.y + k < 0 || player.tank.y + k > map_y) {
                }
                else {
                    var id = (player.tank.x + j).toString() + "_" + (player.tank.y + k).toString();
                    var currentCanvas = document.getElementById(id);

                    var ctx = currentCanvas.getContext('2d');
                    ctx.globalAlpha = 0.2;
                    ctx.fillStyle = player.player_color;
                    ctx.fillRect(0, 0, 512, 512);

                }
            }
        }

    });
}

function drawPlayers(players) {
    players.some(player => {
        if (player.is_dead) {
            return;
        }
        var canvas = document.getElementById(player.tank.x.toString() + "_" + player.tank.y.toString());
        var ctx = canvas.getContext("2d");
        drawPlayer(player, ctx);
    });
}
*/
function markPlayers(players, mapDict) {
    // populate the map dict with the players
    players.some(player => {
        if (player.is_dead) {
            return;
        }
        playerDict = mapDict[player.tank.x.toString() + "_" + player.tank.y.toString()];
        playerDict.player = player;
    });
}
function markPlayersRanges(players, mapDict, excluded_coordinates= [{x: -1, y: -1}]) {
    players.some(player => {
        if (player.is_dead) {
            return;
        }
        if (player.tank.x == excluded_coordinates[0].x && player.tank.y == excluded_coordinates[0].y) {
            return;
        }
        range = player.tank.range;
        for (var j = -range; j <= range; j++) {
            for (var k = -range; k <= range; k++) {
                if (j == 0 && k == 0) {
                }
                else if (player.tank.x + j < 0 || player.tank.x + j > map_x || player.tank.y + k < 0 || player.tank.y + k > map_y) {
                }
                else {
                    var id = (player.tank.x + j).toString() + "_" + (player.tank.y + k).toString();
                    var playerDict = mapDict[id];
                    playerDict.ranges.push(player.player_color);
                }
            }
        }

    });
}

fetch(url).then(res => res.json()).then(data => {
    console.log(data);
    window.globalData = data;
    //createSocket(data.id);
    map_x = data.grid_size_x;
    map_y = data.grid_size_y;

    mapDict = {};
    // this is the dict that contains the map. We first populate the dict with every cell as empty
    // this is for heavy optimization reasons, so we can only load the cells that are viewed on the map
    for (var i = 0; i <= map_x; i++) {
        for (var j = 0; j <= map_y; j++) {
            mapDict[i.toString() + "_" + j.toString()] = {
                x: i,
                y: j,
                ranges: [],
                player: null
            }
        }
    }
    markPlayers(data.players, mapDict);
    markPlayersRanges(data.players, mapDict);
    L.GridLayer.MapTile = L.GridLayer.extend({
        createTile: function (coords) {
            var canvas = document.createElement('canvas');
            if (coords.x == 6 && coords.y == 0) {
                console.log(canvas);
            }
            if (coords.x > map_x || coords.y > map_y || coords.x < 0 || coords.y < 0) {
                return canvas;
            }

            canvas.setAttribute("height", "512");
            canvas.setAttribute("width", "512");


            canvas.style.outline = '8px solid rgb(162, 162, 162)';

            canvas.style.borderRadius = '5px';

            var id = coords.x + "_" + coords.y;
            canvas.id = id;
            var tileDict = mapDict[id];
            if (tileDict.ranges.length > 0) {
                var ctx = canvas.getContext('2d');
                ctx.globalAlpha = 0.2;
                tileDict.ranges.forEach(color => {
                    ctx.fillStyle = color;
                    ctx.fillRect(0, 0, 512, 512);
                });
            }
            if (tileDict.player != null) {
                var ctx = canvas.getContext('2d');
                drawPlayer(tileDict.player, ctx);
            }
            canvas.classList += "canvas_tile";

            return canvas;
        }
    });

    var loaded = false;
    function load() {
        if (!loaded) {
            loaded = true;
        }
        else {
            main()
        }
    }
    function main() {
        // making map global   
        map = L.map('map', {
            attributionControl: false,
            zoomControl: false,
            cursor: true,
            minZoom: 1,
            maxZoom: 7,
            zoomSnap: 0.25,
        })
        console.log(calculateInversePowerOf2(map_x) )
        map.setView(map.unproject([(map_x / 2 + 1) * 64, (map_y / 2 + 1) * 64], 4), calculateInversePowerOf2(map_x) - 3);
        
        map.setMaxBounds([map.unproject([0, 0], 4), map.unproject([64 * (map_x + 1), 64 * (map_y + 1)], 4)])

        L.gridLayer.mapTile = function (opts) {
            return new L.GridLayer.MapTile(opts);
        };

        map.addLayer(L.gridLayer.mapTile({ "minNativeZoom": 6, "maxNativeZoom": 6, "noWrap": true, "keepBuffer": Infinity, "updateWhenIdle": false }));
        map.on('click', function (e) {
            console.log(map.project(e.latlng));
        });

        function retryDrawing(id, player) {
            // sometimes, even after whenReady some tiles are not yet loaded, retry the drawing until it works
            var currentCanvas = document.getElementById(id);
            if (!currentCanvas) {
                setTimeout(retryDrawing, 20, id, player);
                return;
            }
            var ctx = currentCanvas.getContext('2d');
            ctx.globalAlpha = 0.1;
            ctx.fillStyle = player.player_color;
            ctx.fillRect(0, 0, 512, 512);
        }
        map.whenReady(function () {
            map.options.minZoom = 2.5;
            map.setZoom(4);
        });
    }


    heartBlack.onload = load();
    heartRed.onload = load();
});