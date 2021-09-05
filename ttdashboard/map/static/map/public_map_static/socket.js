function createSocket(gameId) {
    const socket = new WebSocket('ws://'
        + window.location.host
        + '/ws/game/'
        + gameId
        + '/'
    );

socket.onmessage = function (e) {
    const message = JSON.parse(e.data);
    const event = message.event;
    const data = message.data;
    const newGameState = message.new_game_data;

    console.log(newGameState);
    console.log(event, data);
    switch (event) {
        case 'move':
            mapDict = makeMapDict(newGameState.players);
            movePlayer(data.position, data.direction, data.newActionPoints, newGameState);
            break;
        case "shoot":
            mapDict = makeMapDict(newGameState.players);
            shootBullet(data.coordsStart, data.coordsEnd, data.newAttackerActionPoints, data.newDeffenderHealth, data.deffenderRange);
            break;
    };
}

socket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};
}