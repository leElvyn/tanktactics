<script lang="ts">
	import type { AutocompleteOption, PopupSettings } from '@skeletonlabs/skeleton';
	import { Autocomplete } from '@skeletonlabs/skeleton';
	import { popup } from '@skeletonlabs/skeleton';
	import { get } from 'svelte/store';
	import { gameStore } from '$lib/stores/gameStore';
	import type { Game, Player } from '$lib/interfaces';
	import { getCookie } from '$lib/utils';
	import { scale } from 'svelte/transition';
	import { selfStore } from '$lib/stores/selfStore';

	let game: Game = get(gameStore)!;
	let self: Player = get(selfStore)!;

	gameStore.subscribe((value) => {
		game = value!;
	});

	let popupSettings: PopupSettings = {
		event: 'focus-click',
		target: 'popupAutocomplete',
		placement: 'bottom',
		middleware: {}
	};

	let playerList: AutocompleteOption[] = [];

	$: {
		playerList = [];
		game.players.forEach((player) => {
			if (player.is_dead) {
				return;
			}
			let distance = Math.max(
				Math.abs(self.tank.x - player.tank.x),
				Math.abs(self.tank.y - player.tank.y)
			);
			if (distance <= player.tank.range && distance != 0) {
				console.log(distance)
				console.log(player)
				// != 0 to exclude ourself
				playerList.push({ label: player.name, value: player.id });
			}
		});
	}

	let selectedPlayerInput: string = '';
	let selectedPlayerId: string = '';

	function onPopupDemoSelect(event: any) {
		selectedPlayerInput = event.detail.label;
		selectedPlayerId = event.detail.value;
	}
	async function attack() {
		let res = await fetch('/api/guild/1/players/@me/attack', {
			method: 'POST',
			headers: {
				'Content-Type': 'Application/Json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			body: JSON.stringify({
				defender_id: String(selectedPlayerId)
			}),
			credentials: 'same-origin'
		});
		if (res.status != 200) {
			console.error(res.text);
		}
	}
</script>

<div class="mt-4 card p-3 flex flex-col" transition:scale>
	<div class="input-group input-group-divider grid-cols-[auto_1fr_auto]" use:popup={popupSettings}>
		<input
			class="input autocomplete"
			type="search"
			name="autocomplete-search"
			bind:value={selectedPlayerInput}
			placeholder="Search players in range ..."
			on:input={() => (selectedPlayerId = '')}
			on:submit={attack}
		/>
		<button class="variant-filled-secondary" disabled={selectedPlayerId === ''} on:click={attack}
			>Attack</button
		>
	</div>
	<div data-popup="popupAutocomplete" class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto">
		<Autocomplete
			bind:input={selectedPlayerInput}
			options={playerList}
			on:selection={onPopupDemoSelect}
		/>
	</div>
</div>
