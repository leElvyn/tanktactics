import type { Game, Player } from '$lib/interfaces';
import { readable, writable, type Readable, type Writable } from 'svelte/store';
import { playerId } from '../consts';
import { gameStore } from './gameStore';

export const selfStore: Readable<Player | undefined> = readable<Player | undefined>(undefined, function start(set) {
    gameStore.subscribe((value: Game | undefined) => {
        if (value) {
            set(value.players.find((player) => player.id == playerId))
        }
    })
    return function stop() { };
});