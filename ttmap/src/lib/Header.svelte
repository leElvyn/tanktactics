<script lang="ts">
	import { AppBar } from '@skeletonlabs/skeleton';
	import AdClock from './AdClock.svelte';
	import type { Game } from './map/interfaces';

	export let gamePromise: Promise<Game>;
</script>

<AppBar>
	<svelte:fragment slot="lead">
		<span class="text-4xl font-bold">Tactics</span>
	</svelte:fragment>
	<svelte:fragment slot="trail">
		{#await gamePromise then game}
			<AdClock />
		{/await}
	</svelte:fragment>
</AppBar>
