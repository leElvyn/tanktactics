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
	let self: Player = $selfStore!;

	gameStore.subscribe((value) => {
		game = value!;
	});

	let popupSettings: PopupSettings = {
		event: 'focus-click',
		target: 'popupAutocomplete',
		placement: 'bottom',
		middleware: {}
	};
	const popupHover: PopupSettings = {
		event: 'hover',
		target: 'popupHover',
		placement: 'left'
	};

	let selectedPlayerInput: string = '';
	let selectedPlayerId: string = '';
	let selectedApAmount = 1;
	let previousAp = selectedApAmount;

	function onPopupDemoSelect(event: any) {
		selectedPlayerInput = event.detail.label;
		selectedPlayerId = event.detail.value;
	}

	function validator(node: HTMLInputElement, value: number) {
		return {
			update(value: number) {
				selectedApAmount = selectedApAmount == null || selectedApAmount < (parseInt(node.min)) || selectedApAmount > parseInt(node.max)  ? previousAp : value;
				previousAp = selectedApAmount;
			}
		};
	}

	async function attack() {
		let res = await fetch('/api/guild/1/players/@me/transfer', {
			method: 'POST',
			headers: {
				'Content-Type': 'Application/Json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			body: JSON.stringify({
				defender_id: String(selectedPlayerId),
				ap_number: parseInt(selectedApAmount as unknown as string)
			}),
			credentials: 'same-origin'
		});
		if (res.status != 200) {
			console.error(res.text);
		}
	}

	let playerList: AutocompleteOption[] = [];

	$: {
		console.log(selectedApAmount);
		playerList = [];
		game.players.forEach((player) => {
			if (player.is_dead) {
				return;
			}
			let distance = Math.max(
				Math.abs(self.tank.x - player.tank.x),
				Math.abs(self.tank.y - player.tank.y)
			);
			if (distance <= self.tank.range && distance != 0) {
				// != 0 to exclude ourself
				playerList.push({ label: player.name, value: player.id });
			}
		});
	}
</script>

<div class="mt-4 card p-3 flex flex-col" transition:scale>
	<div class="input-group input-group-divider grid-cols-[auto_1fr_auto]" use:popup={popupSettings}>
		<input
			class="input autocomplete"
			type="search"
			name="autocomplete-search"
			bind:value={selectedPlayerInput}
			placeholder="Rechercher un joueur à proximité ..."
			on:input={() => (selectedPlayerId = '')}
			on:submit={attack}
		/>
	</div>
	<input
		class="input input-group-shim mt-4"
		type="number"
		bind:value={selectedApAmount}
		use:validator={selectedApAmount}
		min="1"
		max={self.tank.action_points}
		step="1"
		use:popup={popupHover}
	/>
	<button
		class="variant-filled-secondary mt-4 rounded-lg py-2"
		disabled={selectedPlayerId === '' && selectedApAmount !== null}
		on:click={attack}>Transférer</button
	>
	<div data-popup="popupAutocomplete" class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto">
		<Autocomplete
			bind:input={selectedPlayerInput}
			options={playerList}
			on:selection={onPopupDemoSelect}
		/>
	</div>
</div>

<div class="card p-4 variant-filled-secondary" data-popup="popupHover">
	<p>Quantité de points d'action à transférer</p>
	<div class="arrow variant-filled-secondary" />
</div>
