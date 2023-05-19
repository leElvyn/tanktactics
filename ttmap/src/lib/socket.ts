import { movePlayer, attackPlayer, upgradeRange, transferToPlayer, vote } from "./actions"
import type { Game, MoveEvent, ShootEvent, UpgradeEvent, VoteEvent } from "./interfaces"
import { gameStore } from "./stores/gameStore";
import { selfStore } from "./stores/selfStore"
import { addMessage } from "./logs/logs";

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

        gameStore.set(message.new_game_data);

        switch (event) {
            case 'move':
                let moveEvent: MoveEvent = data;
                movePlayer(moveEvent);
                addMessage(`${moveEvent.player.name} vient de se déplacer en ${moveEvent.position.x + moveEvent.direction.x} ${moveEvent.position.y + moveEvent.direction.y}`)
                break;
            case 'shoot':
                let shootEvent: ShootEvent = data;
                attackPlayer(shootEvent);
                addMessage(`${shootEvent.offensive_player.name} vient d'attaquer ${shootEvent.defensive_player.name}. ${shootEvent.defensive_player.name} ${shootEvent.defensive_player.tank.health_points == 0 ? "est mort." : `possède encore ${shootEvent.defensive_player.tank.health_points} PV.`}`)
                break;
            case 'upgrade':
                let upgradeEvent: UpgradeEvent = data;
                upgradeRange(upgradeEvent);
                addMessage(`${upgradeEvent.player.name} vient d'améliorer sa portée. Nouvelle portée : ${upgradeEvent.new_range}`)
                break;
            case 'transfer':
                let transferEvent: ShootEvent = data;
                await transferToPlayer(transferEvent);
                addMessage(`${transferEvent.offensive_player.name} vient de transférer ${transferEvent.ap_amount} PA à ${transferEvent.defensive_player.name}`)
                break;
            case 'vote':
                let voteEvent: VoteEvent = data;
                await vote(voteEvent);
                addMessage(`${voteEvent.voting_player.name} vient de voter pour ${voteEvent.receiving_player.name}. Votes : ${voteEvent.receiving_player.vote_received}.`)
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