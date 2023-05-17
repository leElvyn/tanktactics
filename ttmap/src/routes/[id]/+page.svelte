<script lang="ts">
	import Map from '$lib/map/Map.svelte';
	import Sidebar from '$lib/Sidebar.svelte';

	import Header from '$lib/Header.svelte';

	import { Modal, AppShell, AppBar } from '@skeletonlabs/skeleton';
	import { gameStore } from '$lib/stores/gameStore';
	import type { Game } from '$lib/map/interfaces';

	let promiseResolve: (value: Game) => void;
	let gamePromise = new Promise<Game>((executor) => {
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
		<Header bind:gamePromise/>
	</svelte:fragment>
	<svelte:fragment slot="sidebarRight">
		{#await gamePromise then game}
			<Sidebar />
		{/await}
	</svelte:fragment>
	<Map />
</AppShell>
