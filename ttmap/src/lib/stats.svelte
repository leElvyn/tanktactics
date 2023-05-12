<script lang="ts">
	import type { Game } from './map/interfaces';
	import { gameStore } from './stores/gameStore';
	import { get } from 'svelte/store';

	let game: Game = get(gameStore) as Game;

    gameStore.subscribe((value) => {
		game = value as Game;
	});
	let label = '';
	let red_heart = '❤️ ';
	let black_heart = '🖤 ';
	for (let i = 0; i < 3; i++) {
		if (i < game.self.tank.health_points) {
			label += red_heart;
		} else {
			label += black_heart;
		}
	}

	let voteSelectVisible;
</script>

<div class="card p-4 m-3 ml-4 mr-4 w-10/12 flex justify-center">
	{#if !game.self.is_dead}
		<span class="font-sans font-semibold text-center">
			{game.self.name} &nbsp;&nbsp;
			<span class="bg-yellow-300 text-black h-6 w-6 inline-block text-center">
				{game.self.tank.range}
			</span>&nbsp;&nbsp;
			<span class="bg-green-500 rounded-full h-6 w-6 inline-block text-center">
				{game.self.tank.action_points}
			</span>
			{label}
		</span>
	{:else}
		<div class="flex justify-center w-full">
			{#if game.self.ad_vote}
				{game.self.ad_vote?.name}
			{:else}
				<button class="action-button btn variant-filled" type="button">Vote</button>
			{/if}
		</div>
	{/if}
</div>
