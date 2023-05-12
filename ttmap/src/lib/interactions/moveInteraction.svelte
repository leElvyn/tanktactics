<script lang="ts">
	import Fa from 'svelte-fa/src/fa.svelte';
	import { faArrowLeft, faArrowRight, faArrowDown, faArrowUp } from '@fortawesome/free-solid-svg-icons';

    import { scale } from "svelte/transition"

</script>

<div class="mt-4 card p-3 flex flex-col" transition:scale>
	<div>
		<button type="button" class="invisible arrow-button"><Fa icon={faArrowLeft} /></button>
        <button type="button" class="arrow-button"><Fa icon={faArrowUp} /></button>
		<button type="button" class="invisible arrow-button"><Fa icon={faArrowLeft} /></button>
	</div>
	<div>
		<button type="button" class="arrow-button"><Fa icon={faArrowLeft} /></button>
		<button type="button" class="invisible arrow-button"><Fa icon={faArrowLeft} /></button>
		<button type="button" class="arrow-button"><Fa icon={faArrowRight} /></button>
	</div>
	<div>
		<button type="button" class="invisible arrow-button"><Fa icon={faArrowLeft} /></button>
		<button type="button" class="arrow-button"><Fa icon={faArrowDown} /></button>
		<button type="button" class="invisible arrow-button variant-filled"><Fa icon={faArrowLeft} /></button>
	</div>
</div>

<style>
    .arrow-button {
        @apply m-1 btn-icon variant-filled;
    }
</style>