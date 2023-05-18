<script lang="ts">
	import type { Game } from '$lib/interfaces';

	import Tile from './Tile.svelte';
	import Player from "./Player.svelte"

	import { gamePromise } from '../stores/gameStore';
	import { TILE_SIZE, playerId } from '$lib/consts';

	import { onMount } from 'svelte';
	import { registerGestures } from './mapMouvement';
	import { registerInteractions } from './mapInteractions';
	import { createSocket } from '$lib/socket';

	let map: HTMLElement;
	let game: Game;

	onMount(async () => {
    	registerGestures(map);
		await registerInteractions(map);

		await createSocket(game, map);
	});
</script>

{#await gamePromise then game}
	<div
		id="map"
		bind:this={map}
		style="width:{(game.grid_size_x + 1) * TILE_SIZE}px;height:{(game.grid_size_y + 1) *
			TILE_SIZE}px"
	>
		{#each { length: game.grid_size_x } as _, i}
			{#each { length: game.grid_size_y } as _, j}
				<Tile x={i} y={j} />
			{/each}
		{/each}

		{#each game.players as player}
			<Player player={player}/>
		{/each}
	</div>
{/await}

<style>
</style>
