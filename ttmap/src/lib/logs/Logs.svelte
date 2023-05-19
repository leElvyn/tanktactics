<script lang="ts">
	import { writable } from "svelte/store";

	import { messages } from "./logs";
</script>

<div class="card w-11/12 h-3/6 mt-4 p-2 overflow-scroll">
	{#each $messages as message}
		<span class="inline-block mb-2">{message}</span>
	{/each}
</div>