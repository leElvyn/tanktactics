import { movePlayer, attackPlayer, upgradeRange, transferToPlayer, vote} from "./actions"
import type { Game, MoveEvent, ShootEvent, UpgradeEvent, VoteEvent } from "./interfaces"
import { gameStore } from "./stores/gameStore";
import { selfStore } from "./stores/selfStore"

export async function createSocket(game: Game) {
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
        
        console.log(message.new_game_data)
        gameStore.set(message.new_game_data);
        
        switch (event) {
            case 'move':
                let moveEvent: MoveEvent = data;
                movePlayer(moveEvent);
                break;
            case 'shoot':
                let shootEvent: ShootEvent = data;
                attackPlayer(shootEvent);
                break;
            case 'upgrade':
                let upgradeEvent: UpgradeEvent = data;
                upgradeRange(upgradeEvent);
                break;
            case 'transfer':
                let transferEvent: ShootEvent = data;
                await transferToPlayer(transferEvent);
                break;
            case 'vote':
                let voteEvent: VoteEvent = data;
                await vote(voteEvent);
                break;
            case 'new_ad':
                // all we need to do is set the game
                break;
        };
    }

    socket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };
}