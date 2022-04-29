import { movePlayer } from "./actions.js"
import { Game, MoveEvent } from "./interfaces"

export async function createSocket(game: Game, map: HTMLElement) {
    const socket = new WebSocket('ws://'
        + "tank-tactics.com"
        + '/ws/game/'
        + game.guild_id
        + '/'
    );

    socket.onmessage = function (e) {
        const message = JSON.parse(e.data);
        const event = message.event;
        const data = message.data;

        game = message.new_game_data;
        
        switch (event) {
            case 'move':
                let event: MoveEvent = data;
                movePlayer(event);
                break;
        };
    }

    socket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };
}