<script lang="ts">
	import { TILE_SIZE } from '$lib/consts';
	import type { Player } from '$lib/interfaces';
	import { gameStore } from '$lib/stores/gameStore';

	export let playerId: number;
	let game = $gameStore;
	let player: Player;

	player = game?.players.find((value) => value.id == playerId) as Player
	$: {
		player = game?.players.find((value) => value.id == playerId) as Player
	}

	let range = player.tank.range;

    let new_col = player.player_color.replace(/rgb/i, "rgba");
    new_col = new_col.replace(/\)/i, ',0.3)');
</script>

<div
	class="range"
	id="range_{player.tank.x}_{player.tank.y}"
	style="left: {(player.tank.x - range) * TILE_SIZE}px;
            top: {(player.tank.y - range) * TILE_SIZE}px;
            width: {(range * 2 + 1) * TILE_SIZE}px;
            height: {(range * 2 + 1) * TILE_SIZE}px;
            background-color: {new_col};"
/>

<style>
	div {
		position: absolute;
		border: 3px solid rgb(27, 27, 27);
		-webkit-box-sizing: border-box;
		box-sizing: border-box;
		z-index: 1;
	}
</style>
