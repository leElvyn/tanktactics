import { movePlayer, shootPlayer, upgradeRange } from "./actions.js"
import { Game, MoveEvent, ShootEvent, UpgradeEvent } from "./interfaces"

export async function createSocket(game: Game, map: HTMLElement) {
    const socket = new WebSocket('ws://'
        + window.location.host
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
                let moveEvent: MoveEvent = data;
                movePlayer(moveEvent);
                break;
            case 'shoot':
                let shootEvent: ShootEvent = data;
                shootPlayer(shootEvent);
                break;
            case 'upgrade':
                let upgradeEvent: UpgradeEvent = data;
                console.log(upgradeEvent);
                upgradeRange(upgradeEvent);
                break;
        };
    }

    socket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };
}