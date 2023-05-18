import type { Game } from '$lib/interfaces';
import { writable, type Writable } from 'svelte/store';

let promiseResolve: (value: Game) => void;
export let gamePromise = new Promise<Game>((executor) => {
    promiseResolve = executor;
});

export const gameStore: Writable<Game | undefined> = writable(undefined);

gameStore.subscribe((game) => {
    if (game !== undefined) {
        promiseResolve(game);
    }
});