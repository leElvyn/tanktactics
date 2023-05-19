<script async lang="ts">
	import type { Game } from '$lib/interfaces';

	import Tile from './Tile.svelte';
	import Player from './Player.svelte';

	import { gamePromise, gameStore } from '../stores/gameStore';
	import { selfStore } from '$lib/stores/selfStore';
	import { TILE_SIZE, playerId } from '$lib/consts';

	import { onMount } from 'svelte';
	import { registerGestures } from './mapMouvement';
	import { createSocket } from '$lib/socket';
	import Range from './Range.svelte';

	let map: HTMLElement;
	let game = $gameStore as Game;

	$: {
		if (map) {
			registerGestures(map);
		}
	}

	gamePromise.then((game) => {
		createSocket(game);
	});
</script>

{#await gamePromise then game}
	<div
		id="map"
		class="absolute overflow-hidden"
		bind:this={map}
		style="width:{game.grid_size_x * TILE_SIZE}px;height:{game.grid_size_y * TILE_SIZE}px"
	>
		{#each { length: game.grid_size_x } as _, i}
			{#each { length: game.grid_size_y } as _, j}
				<Tile x={i} y={j} />
			{/each}
		{/each}

		{#each game.players as player}
			{#if !player.is_dead}
				<Player playerId={player.id} />
				<Range playerId={player.id} />
			{/if}
		{/each}
	</div>
{/await}

<style>
</style>
