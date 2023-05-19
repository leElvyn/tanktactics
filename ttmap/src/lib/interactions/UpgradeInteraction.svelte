<script lang="ts">
	import type { Player } from '$lib/interfaces';
	import { selfStore } from '$lib/stores/selfStore';
	import { getCookie } from '$lib/utils';
	import { scale } from 'svelte/transition';

	let self: Player;

	selfStore.subscribe((value) => {
		self = value as Player;
	});

	async function upgrade() {
		let res = await fetch('/api/guild/1/players/@me/upgrade', {
			method: 'POST',
			headers: {
				'Content-Type': 'Application/Json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			credentials: 'same-origin'
		});
		if (res.status != 200) {
			console.error(res.text);
		}
	}

	let cost = 1;
	$: {
		cost = 1
		for (let i = 1; i < self.tank.range; i++) {
			cost += i * 2;
		}
	}
</script>

<div class="mt-4 card p-3 flex flex-col grow-2" transition:scale>
	<button class="variant-filled-secondary p-3 mx-10 rounded-lg flex items-center"
		on:click={upgrade}
		><span class="inline-block pb-1">Améliorer : &nbsp;</span>
		<span class="bg-green-500 rounded-full h-6 w-6 inline-block text-center">
			{cost}
		</span>
	</button>
</div>
