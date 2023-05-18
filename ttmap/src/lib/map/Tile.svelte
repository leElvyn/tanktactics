<script lang="ts">
	import { TILE_SIZE } from '$lib/consts';
	import { gameStore } from '$lib/stores/gameStore';

	let game = $gameStore;

	export let x: number;
	export let y: number;

</script>

<div class="tile" id="tile_{x}_{y}" style="top: {x*TILE_SIZE}px;left: {y*TILE_SIZE}px"/>
