final_ready = false;
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

function drawRangeSurroundings(players, excluded_coordinates = [{ x: -1, y: -1 }]) {
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
                    if (!currentCanvas) {
                        continue;
                    }
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
        if (!canvas) {
            return;
        }
        var ctx = canvas.getContext("2d");
        drawPlayer(player, ctx);
    });
}

fetch(url).then(res => res.json()).then(data => {
    window.globalData = data;
    map_x = data.grid_size_x;
    map_y = data.grid_size_y;
    L.GridLayer.MapTile = L.GridLayer.extend({
        createTile: function (coords) {
            var canvas = document.createElement('canvas');
            if (coords.x > map_x || coords.y > map_y || coords.x < 0 || coords.y < 0) {
                return canvas;
            }

            canvas.setAttribute("height", "512");
            canvas.setAttribute("width", "512");

            canvas.style.outline = '8px solid rgb(162, 162, 162)';

            canvas.style.borderRadius = '5px';

            canvas.id = coords.x + "_" + coords.y;
            canvas.setAttribute("x", coords.x);
            canvas.setAttribute("y", coords.y);
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
            zoomSnap: 0.1,
        })
        if (is_focused) {
            var location_focus = JSON.parse(focus)
            range = location_focus.range;
            zoom = 5.5 - Math.sqrt(range);
            var latlng = map.unproject([location_focus.x * 64 + 32, location_focus.y * 64 + 32], 4);
            map.setView(latlng, zoom);
        }
        else {
            map.setView(map.unproject([(map_x / 2 + 1) * 64 + 32, (map_y / 2 + 1) * 64 + 32], 4), 3);
        }
        //map.setMaxBounds([map.unproject([0, 0], 4), map.unproject([64 * (map_x + 1), 64 * (map_y + 1)], 4)])

        L.gridLayer.mapTile = function (opts) {
            return new L.GridLayer.MapTile(opts);
        };

        map.addLayer(L.gridLayer.mapTile({ "minNativeZoom": 6, "maxNativeZoom": 6, "noWrap": true, "keepBuffer": Infinity, "updateWhenIdle": false }));

        map.whenReady(function () {
            // we start by drawing the range so it doesn't mask the players
            drawRangeSurroundings(data.players);
            
            drawPlayers(data.players);
            map.options.minZoom = 1;
            if (is_focused) {
                console.log(focus);
                var location_focus = JSON.parse(focus)
                range = location_focus.range;
                zoom = 6.5 - Math.sqrt(range);
                var latlng = map.unproject([location_focus.x * 64 + 32, location_focus.y * 64 + 32], 4);
                map.setView(latlng, zoom);
                final_ready = true;
            }
            else {
                map.setView(map.unproject([(map_x / 2 + 1) * 64 + 32, (map_y / 2 + 1) * 64 + 32], 4), 3);
                final_ready = true;
            }
        });
    }


    heartBlack.onload = load();
    heartRed.onload = load();
});