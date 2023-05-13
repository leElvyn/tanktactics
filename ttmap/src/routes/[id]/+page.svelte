<script lang="ts">
	import Map from '$lib/map/Map.svelte';
	import { Modal, AppShell, AppBar } from '@skeletonlabs/skeleton';
	import Sidebar from '$lib/Sidebar.svelte';
	import { onMount } from 'svelte';
	import { gameStore } from '$lib/stores/gameStore';
	import VoteForm from '$lib/voteForm.svelte';

	let promiseResolve: (value: unknown) => void;
	let gamePromise = new Promise((executor) => {
		promiseResolve = executor;
	});
	gameStore.subscribe((game) => {
		if (game !== undefined) {
			promiseResolve(game)
		}
	});
</script>
<Modal />
<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<!--<svelte:fragment slot="lead"></svelte:fragment>-->
			<span class="text-4xl font-bold">Tactics</span>
			<!--<svelte:fragment slot="trail"></svelte:fragment>-->
		</AppBar>
	</svelte:fragment>
	<svelte:fragment slot="sidebarRight">
		{#await gamePromise then game}
			<Sidebar />
		{/await}
	</svelte:fragment>
	<Map />
</AppShell>
