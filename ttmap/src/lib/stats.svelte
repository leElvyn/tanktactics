<script lang="ts">
	import type { Game } from './interfaces';
	import { gameStore } from './stores/gameStore';
	import { get } from 'svelte/store';
	import VoteForm from './voteForm.svelte';
	import { selfStore } from './stores/selfStore';


	let game = $gameStore;
	let self = $selfStore;

	gameStore.subscribe((value) => {
		game = value as Game;
	});
	let label = '';
	let red_heart = '❤️ ';
	let black_heart = '🖤 ';
	for (let i = 0; i < 3; i++) {
		if (i < self?.tank.health_points!) {
			label += red_heart;
		} else {
			label += black_heart;
		}
	}

	let voteSelectVisible = false;
</script>
<div class="card p-4 m-3 ml-4 mr-4 w-11/12 flex justify-center">
	{#if !self?.is_dead}
		<span class="font-sans font-semibold text-center">
			{self?.name} &nbsp;&nbsp;
			<span class="bg-yellow-300 text-black h-6 w-6 inline-block text-center">
				{self?.tank.range}
			</span>&nbsp;&nbsp;
			<span class="bg-green-500 rounded-full h-6 w-6 inline-block text-center">
				{self?.tank.action_points}
			</span>
			{label}
		</span>
	{:else}
		<div class="flex justify-center w-full">
			{#if self?.ad_vote}
				You voted for : {self?.ad_vote?.name}
			{:else if !voteSelectVisible}
				<button
					class="action-button btn variant-filled"
					type="button"
					on:click={() => (voteSelectVisible = true)}>Vote</button
				>
			{:else}
				<VoteForm bind:voteSelectVisible />
			{/if}
		</div>
	{/if}
</div>
