<script lang="ts">
	import { AppBar } from '@skeletonlabs/skeleton';
	import AdClock from './AdClock.svelte';
	import type { Game } from './interfaces';
	
	import { gamePromise } from './stores/gameStore';

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
