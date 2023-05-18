<script lang="ts">
	import { onMount } from 'svelte';
	import { gameStore } from '../stores/gameStore';

	let map;

	onMount(async () => {
		gameStore.subscribe(async (game) => {
			if (game !== undefined) {
				(await import('./mapMain')).main(map, game);
			}
		});
	});
</script>

<div id="map" bind:this={map} />
