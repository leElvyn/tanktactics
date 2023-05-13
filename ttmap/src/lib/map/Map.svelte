<script lang="ts">
	import { onMount } from 'svelte';
	import { gameStore } from '../stores/gameStore';
	import { fetchGame } from './mapDrawing';

	let map;

	onMount(async () => {
		let gameID = window.location.pathname.split('/')[2];
		let url = '/api/guild/' + gameID;
		let game = await fetchGame(url);

		gameStore.set(game);

		(await import('./mapMain')).main(map, game);
	});
</script>

<div id="map" bind:this={map} />