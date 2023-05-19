<script lang="ts">
	import { TILE_SIZE } from '$lib/consts';
	import type { Player } from '$lib/interfaces';
	import { gameStore } from '$lib/stores/gameStore';
	import { onMount } from 'svelte';

	export let playerId: number;
	let game = $gameStore;

	gameStore.subscribe((gameValue) => {
		game = gameValue;
	});
	let player: Player;
	player = game?.players.find((value) => value.id == playerId) as Player;
	$: {
		player = game?.players.find((value) => value.id == playerId) as Player;
	}

	let playerCanvas: HTMLElement;

	onMount(() => {
		playerCanvas.style.left = player.tank.x * TILE_SIZE + 'px';
		playerCanvas.style.top = player.tank.y * TILE_SIZE + 'px';
	});

	let label = '';
	$: {
		label = '';
		let red_heart = '❤️ ';
		let black_heart = '🖤 ';
		for (let i = 0; i < 3; i++) {
			if (i < player.tank.health_points!) {
				label += red_heart;
			} else {
				label += black_heart;
			}
		}
	}
	function canvasMouseEnter(event: Event) {
		event = event as MouseEvent;

		let range = document.getElementById('range_' + player.tank.x + '_' + player.tank.y);

		range!.style.backgroundColor = range!.style.backgroundColor.replace(/[^,]+(?=\))/, '0.8');
		//range.style.border = "7px solid rgb(5, 5, 5)";
		range!.style.zIndex = '2';
	}

	function canvasMouseOut(event: Event) {
		event = event as MouseEvent;
		let element = <HTMLElement>event.target;

		let range = document.getElementById('range_' + player.tank.x + '_' + player.tank.y);

		range!.style.backgroundColor = range!.style.backgroundColor.replace(/[^,]+(?=\))/, '0.2');
		//range.style.border = "3px solid rgb(5,5,5)";

		range!.style.zIndex = '1';
	}
</script>

<div>
	<div
		bind:this={playerCanvas}
		id="player_{player.tank.x}_{player.tank.y}"
		class="player-canvas font-sans font-semibold text-center text-[9px] flex flex-col leading-3 justify-around cursor-default"
		on:mouseenter={canvasMouseEnter}
		on:mouseleave={canvasMouseOut}
	>
		{player.name}
		<div>
			<span class="bg-yellow-300 text-black h-3 w-3 inline-block text-center">
				{player.tank.range}
			</span>
			<span class="bg-green-500 rounded-full h-3 w-3 inline-block text-center">
				{player.tank.action_points}
			</span>
			<span class="bg-red-500 h-3 w-3 rounded-sm inline-block text-center">
				<div style="">{player.vote_received}</div>
			</span>
		</div>
		<div class="pb-1">{label}</div>
	</div>
</div>

<style>
	.player-canvas {
		position: absolute;
		height: 50px;
		width: 50px;
		z-index: 10;
	}
</style>
