<script lang="ts">
	import Map from '$lib/map/Map.svelte';
	import Sidebar from '$lib/Sidebar.svelte';
	import Header from '$lib/Header.svelte';

	import { Modal, AppShell, AppBar } from '@skeletonlabs/skeleton';

	import { gameStore } from '$lib/stores/gameStore';
	import { gamePromise } from '$lib/stores/gameStore';
	import type { Game } from '$lib/interfaces';
	import { onMount } from 'svelte';
	import { playerId, setPlayerId } from '$lib/consts';


	function parseReviver(key: string, value: unknown) {
		if (typeof value === 'string' && key == 'guild_id') {
			return BigInt(value);
		}
		return value;
	}

	export async function fetchGame(url: string) {
		const response = await fetch(url);
		return JSON.parse(await response.text(), parseReviver);
	}

	onMount(() => {
		let gameID = window.location.pathname.split('/')[2];
		let url = '/api/guild/' + gameID;
		fetchGame(url).then((game: Game) => {
			setPlayerId(game.self.id);
			gameStore.set(game);
		});
	});
</script>

<Modal />
<AppShell>
	<svelte:fragment slot="header">
		<Header />
	</svelte:fragment>
	<svelte:fragment slot="sidebarRight">
		{#await gamePromise then game}
			<Sidebar />
		{/await}
	</svelte:fragment>
	<Map />
</AppShell>
