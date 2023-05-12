<script lang="ts">
	import ActionList from './actionList.svelte';
	import { slide } from 'svelte/transition';
	import Stats from './stats.svelte';
	import { get } from 'svelte/store';
	import type { Game } from './map/interfaces';
	import { gameStore } from './stores/gameStore';

	let game = get(gameStore) as Game;
</script>

<div
	class="md:visible invisible
            absolute right-0 h-screen w-1/6 bg-slate-500 items-center
            flex flex-col"
	transition:slide>

	<Stats />
	{#if !game.self.is_dead}
		<ActionList />
	{/if}
</div>
