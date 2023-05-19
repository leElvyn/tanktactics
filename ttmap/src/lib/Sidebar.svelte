<script lang="ts">
	import ActionList from './ActionList.svelte';
	import { slide } from 'svelte/transition';
	import Stats from './Stats.svelte';
	import type { Game } from './interfaces';
	import { gameStore } from './stores/gameStore';
	import { onMount } from 'svelte';
	import { selfStore } from './stores/selfStore';
	import Logs from './logs/Logs.svelte';

	let game = $gameStore;
	let self = $selfStore;

    // This is used in interactions to check if the map should zoom or not
	let hovered = false;
    let sidebarElement: HTMLElement;
    $:{
        if (sidebarElement != null) {
            sidebarElement.setAttribute("hovered", String(hovered))
        }
    }
</script>

<div
	class="md:visible invisible
            absolute right-0 h-screen w-3/12 bg-slate-500 items-center
            flex flex-col"
    id="sidebarElement"
	transition:slide
    bind:this={sidebarElement}
	on:mouseover={() => {hovered = true;}}
	on:focus ={() => {hovered = true;}}
	on:mouseout ={() => {hovered = false;}}
	on:blur ={() => {hovered = false;}}>
	<Stats />
	{#if !self?.is_dead}
		<ActionList />
	{/if}

	<Logs/>
</div>
