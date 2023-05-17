import { movePlayer, shootPlayer, upgradeRange } from "./actions"
import { transferToPlayer } from "./actions/transfer";
import { vote } from "./actions/vote";
import { Game, MoveEvent, ShootEvent, UpgradeEvent, VoteEvent } from "./interfaces"

export async function createSocket(game: Game, map: HTMLElement) {
    const socket = new WebSocket('ws://'
        + window.location.host
        + '/ws/game/'
        + game.guild_id
        + '/'
    );

    socket.onmessage = async function (e) {
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
            case 'transfer':
                let transferEvent: ShootEvent = data;
                console.log(transferEvent);
                await transferToPlayer(transferEvent);
                break;
            case 'vote':
                let voteEvent: VoteEvent = data;
                console.log(voteEvent);
                await vote(voteEvent);
                break;
        };
    }

    socket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };
}