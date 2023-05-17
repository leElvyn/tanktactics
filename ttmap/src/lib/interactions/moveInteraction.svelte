<script lang="ts">
	import Fa from 'svelte-fa/src/fa.svelte';
	import {
		faArrowLeft,
		faArrowRight,
		faArrowDown,
		faArrowUp
	} from '@fortawesome/free-solid-svg-icons';

	import { scale } from 'svelte/transition';
	import { getCookie } from '$lib/utils';
	import { gameStore } from '../stores/gameStore';

	let game = $gameStore;

	async function move(direction: number[]) {
		// direction is a tuple that can be added to current coordinates.
		let res = await fetch('/api/guild/1/players/@me/move', {
			method: 'POST',
			headers: {
				'Content-Type': 'Application/Json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			body: JSON.stringify({
				x: game!.self.tank.x + direction[0],
				y: game!.self.tank.y + direction[1]
			}),
			credentials: 'same-origin'
		});
		if (res.status == 200) {
			let data = await res.json();
			console.log(data);
			gameStore.set(data.game);
		}
		else {
			console.error(await res.json())
		}
	}
</script>

<div class="mt-4 card p-3 flex flex-col" transition:scale>
	<div>
		<button type="button" class="invisible m-1 btn-icon variant-filled"
			><Fa icon={faArrowLeft} /></button
		>
		<button type="button" class="m-1 btn-icon variant-filled" on:click={() => move([0, -1])} disabled={game?.self.tank.y == 0}
			><Fa icon={faArrowUp} /></button
		>
		<button type="button" class="invisible m-1 btn-icon variant-filled"
			><Fa icon={faArrowLeft} /></button
		>
	</div>
	<div>
		<button type="button" class="m-1 btn-icon variant-filled" on:click={() => move([-1, 0])} disabled={game?.self.tank.x == 0}
			><Fa icon={faArrowLeft} /></button
		>
		<button type="button" class="invisible m-1 btn-icon variant-filled"
			><Fa icon={faArrowLeft} /></button
		>
		<button type="button" class="m-1 btn-icon variant-filled" on:click={() => move([1, 0])} disabled={game?.self.tank.x == game?.grid_size_x}
			><Fa icon={faArrowRight} /></button
		>
	</div>
	<div>
		<button type="button" class="invisible m-1 btn-icon variant-filled"
			><Fa icon={faArrowLeft} /></button
		>
		<button type="button" class="m-1 btn-icon variant-filled" on:click={() => move([0, 1])} disabled={game?.self.tank.y == game?.grid_size_y}
			><Fa icon={faArrowDown} /></button
		>
		<button type="button" class="invisible m-1 btn-icon variant-filled"
			><Fa icon={faArrowLeft} /></button
		>
	</div>
</div>

<style>
</style>
