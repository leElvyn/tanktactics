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
	import { selfStore } from '$lib/stores/selfStore';
	import type { Game, Player } from '$lib/interfaces';


	let game = $gameStore;
	let self: Player;

	selfStore.subscribe((value) => {
		self = value as Player
	})

	gameStore.subscribe((value) => {
		game = value as Game;
	});
	async function move(direction: number[]) {
		// direction is a tuple that can be added to current coordinates.
		console.log(self!.tank.x)
		console.log(self!.tank.y)
		
		console.log(direction)
		let res = await fetch('/api/guild/1/players/@me/move', {
			method: 'POST',
			headers: {
				'Content-Type': 'Application/Json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			body: JSON.stringify({
				x: self!.tank.x + direction[0],
				y: self!.tank.y + direction[1]
			}),
			credentials: 'same-origin'
		});
		if (res.status == 200) {
			let data = await res.json();
		}
		else {
			console.error(await res.json())
		}
	}
</script>

<div class="text-token w-full max-w-sm space-y-2">
	<div class="mt-4 card p-3 flex flex-col justify-center" transition:scale>
		<div class="flex justify-center">
			<button type="button" class="invisible m-1 btn-icon variant-filled-secondary"
				><Fa icon={faArrowLeft} /></button
			>
			<button type="button" class="m-1 btn-icon variant-filled-secondary" on:click={() => move([0, -1])} disabled={self?.tank.y == 0}
				><Fa icon={faArrowUp} /></button
			>
			<button type="button" class="invisible m-1 btn-icon variant-filled-secondary"
				><Fa icon={faArrowLeft} /></button
			>
		</div>
		<div class="flex justify-center">
			<button type="button" class="m-1 btn-icon variant-filled-secondary" on:click={() => move([-1, 0])} disabled={self?.tank.x == 0}
				><Fa icon={faArrowLeft} /></button
			>
			<button type="button" class="invisible m-1 btn-icon variant-filled-secondary"
				><Fa icon={faArrowLeft} /></button
			>
			<button type="button" class="m-1 btn-icon variant-filled-secondary" on:click={() => move([1, 0])} disabled={self?.tank.x == game?.grid_size_x}
				><Fa icon={faArrowRight} /></button
			>
		</div>
		<div class="flex justify-center">
			<button type="button" class="invisible m-1 btn-icon variant-filled-secondary"
				><Fa icon={faArrowLeft} /></button
			>
			<button type="button" class="m-1 btn-icon variant-filled-secondary" on:click={() => move([0, 1])} disabled={self?.tank.y == game?.grid_size_y}
				><Fa icon={faArrowDown} /></button
			>
			<button type="button" class="invisible m-1 btn-icon variant-filled-secondary"
				><Fa icon={faArrowLeft} /></button
			>
		</div>
	</div>
</div>
<style>
</style>
