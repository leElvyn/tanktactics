bullet = L.icon({
    iconUrl: '/static/map/public_map_static/assets/bullet.png',

    iconSize: [5, 10],
    iconAnchor: [2.5, 5],
    popupAnchor: [0, -5],
});

function shootBullet(coordsStart, coordsEnd, newAttackerActionPoints, newDefenderHealth) {
    var deltaX = coordsStart.x - coordsEnd.x;
    var deltaY = coordsStart.y - coordsEnd.y;
    var angle = Math.atan2(deltaY, deltaX) * (180 / Math.PI);
    // create the trajectory of the bullet
    var line = L.polyline([map.unproject([coordsStart.x * 64 + 32, coordsStart.y * 64 + 32], 4), map.unproject([coordsEnd.x * 64 + 32, coordsEnd.y * 64 + 32], 4)]);
    
    //create the bullet
    var marker = L.animatedMarker(line.getLatLngs(), { 
    distance: 600000,
    duration: 3,
    icon: bullet,
    rotationAngle: angle + 90,
        onEnd: function() {
            map.removeLayer(this);
            hurtAnimation(coordsEnd, 3, newDefenderHealth);
            if (newDefenderHealth <= 0) {
                var deadTile = document.getElementById(coordsEnd.x + "_" + coordsEnd.y);
                newNode = deadTile.cloneNode(true);
                newCtx = newNode.getContext("2d");
                newCtx.clearRect(0, 0, newNode.width, newNode.height);
                deadTile.parentNode.appendChild(newNode);
                deadTile.style.opacity = 0;
                setTimeout(function() {
                    deadTile.remove();
                }, 2000);
            }
        }
    });

    map.addLayer(marker);
    marker._icon.style.display = 'none'; // the marker takes a bit less than a second to animate, hid it for now
    setTimeout(function() {
        marker._icon.style.display = 'block'; // show the marker
        drawActionPoints(document.getElementById(coordsStart.x + "_" + coordsStart.y).getContext("2d"), newAttackerActionPoints); // override the attacker's action points
    }, 940);

} 

function hurtAnimation(playerCoord, repeat, newDefenderHealth) {
    // keep track of the number of times we've repeated
    loops = 0;
    var canvas = document.getElementById(playerCoord.x + "_" + playerCoord.y);
    var ctx = canvas.getContext("2d");
    ctx.globalAlpha = 0.11;
    ctx.fillStyle = "red";
    original = ctx.getImageData(0, 0, ctx.canvas.width, ctx.canvas.height);

    function fadeOut(timestamp) {
        ctx.putImageData(original, 0, 0);
        ctx.globalAlpha -= 0.1;
        console.log(ctx.globalAlpha);
        ctx.fillRect(0,0,512,512);
        
        if (ctx.globalAlpha <= 0.15) {
            ctx.putImageData(original, 0, 0);
            if (loops < repeat) {
                loops++;
                window.requestAnimationFrame(fadeIn);
            }
            else {
                // end of the animation
                ctx.globalAlpha = 1;
                drawHeart(ctx, newDefenderHealth);
                return
            }
        }
        window.requestAnimationFrame(fadeOut);
        
    }

    function fadeIn(timestamp) {

        
        ctx.globalAlpha += 0.1;
        console.log(ctx.globalAlpha);
        ctx.putImageData(original, 0, 0);
        ctx.fillRect(0,0,512,512);
        
        if (ctx.globalAlpha >= 0.5) {
            window.requestAnimationFrame(fadeOut);
            return
        }
        //ctx.globalAlpha = 1.0;
        window.requestAnimationFrame(fadeIn);
    }
    window.requestAnimationFrame(fadeIn);
}

function movePlayer(currentPosition, direction, newActionPoints, newData) {

    var currentPlayer
    newData.players.forEach(player => {
        if (player.tank.x == currentPosition.x + direction.x && player.tank.y == currentPosition.y+ direction.y) {
            currentPlayer = player;
        }
    });
    var everyCanvas = document.getElementsByClassName("canvas_tile");
    var range = currentPlayer.tank.range + 1;

    for (var i = 0; i < everyCanvas.length; i++) {
        var canvas = everyCanvas[i];
        if (currentPosition.x + range >= canvas.getAttribute("x") && currentPosition.x - range <= canvas.getAttribute("x") && currentPosition.y + range >= canvas.getAttribute("y") && currentPosition.y - range <= canvas.getAttribute("y")) { 
            ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    }
    drawRangeSurroundings(globalData.players, [currentPosition]);
    drawPlayers(globalData.players);

    var tile = document.getElementById(currentPosition.x + "_" + currentPosition.y);
    var clonedTile = tile.cloneNode(true);
    var clonedCtx = clonedTile.getContext("2d");
    var ctx = tile.getContext("2d");
    clonedCtx.clearRect(0, 0, tile.width, tile.height);
    tile.parentNode.appendChild(clonedTile);
    tile.style.outline = ""
    tile.style.left = direction.x * 256 + "px";
    tile.style.top = direction.y * 256 + "px";

    canvasData = ctx.getImageData(0, 0, ctx.canvas.width, ctx.canvas.height);
    newCtx = document.getElementById((currentPosition.x + direction.x) + "_" + (currentPosition.y + direction.y)).getContext("2d");

    globalData = newData;
    console.log(newData);
    
    setTimeout(function() {
        newCtx.putImageData(canvasData, 0, 0);
        tile.remove();
        console.log(newActionPoints);
        drawActionPoints(newCtx, newActionPoints);
        everyCanvas = document.getElementsByClassName("canvas_tile");
        for (var i = 0; i < everyCanvas.length; i++) {
            var canvas = everyCanvas[i];
            console.log(canvas);
            ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
        drawRangeSurroundings(globalData.players);
        drawPlayers(globalData.players);
    }, 2000);
}