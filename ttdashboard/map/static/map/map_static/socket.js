import { movePlayer } from "./actions.js";
export async function createSocket(game, map) {
    const socket = new WebSocket('ws://'
        + window.location.host
        + '/ws/game/'
        + game.guild_id
        + '/');
    socket.onmessage = function (e) {
        const message = JSON.parse(e.data);
        const event = message.event;
        const data = message.data;
        game = message.new_game_data;
        switch (event) {
            case 'move':
                let event = data;
                movePlayer(event);
                break;
        }
        ;
    };
    socket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };
}
