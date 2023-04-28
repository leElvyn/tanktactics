<script lang="ts">
	import Map from '$lib/map/Map.svelte';
	import {Modal, AppShell, AppBar } from '@skeletonlabs/skeleton';
	import Sidebar from '$lib/Sidebar.svelte';

	let img = new Image();
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
		<Sidebar></Sidebar>
	</svelte:fragment>
	<Map />
</AppShell>
