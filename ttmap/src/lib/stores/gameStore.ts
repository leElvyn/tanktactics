import type { Game } from '$lib/map/interfaces';
import { writable, type Writable } from 'svelte/store';

export const gameStore: Writable<Game|undefined> = writable(undefined);