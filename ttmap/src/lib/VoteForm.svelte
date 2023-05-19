<script lang="ts">
	import type { AutocompleteOption, PopupSettings } from '@skeletonlabs/skeleton';
	import { Autocomplete } from '@skeletonlabs/skeleton';
	import { popup } from '@skeletonlabs/skeleton';
	import { get } from 'svelte/store';
	import { gameStore } from './stores/gameStore';
	import type { Game } from './interfaces';
	import { getCookie } from './utils';
	import Player from './map/Player.svelte';

	export let voteSelectVisible;

	let game: Game = get(gameStore)!;

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
			if (!player.is_dead) {
				playerList.push({ label: player.name, value: player.id });
			}
		});
	}

	let playerVoteInput: string = '';
	let playerVoteId: string = '';

	function onPopupDemoSelect(event: any) {
		playerVoteInput = event.detail.label;
		playerVoteId = event.detail.value;
	}
	async function vote() {
		let res = await fetch('/api/guild/1/players/@me/vote', {
			method: 'POST',
			headers: { 
				'Content-Type': 'Application/Json',
				"X-CSRFToken": getCookie("csrftoken")
			},
			body: JSON.stringify({
				target_id: String(playerVoteId)
			}),
			credentials: 'same-origin'
		});
		let data = await res.json();
		gameStore.set(data.game);
		voteSelectVisible = false;
	}
</script>

<div class="text-token w-full max-w-sm space-y-2">
	<div class="input-group input-group-divider grid-cols-[auto_1fr_auto]" use:popup={popupSettings}>
		<input
			class="input autocomplete"
			type="search"
			name="autocomplete-search"
			bind:value={playerVoteInput}
			placeholder="Rechercher un joueur en vie ..."
			on:input={() => (playerVoteId = '')}
			on:submit={vote}
		/>
		<button class="variant-filled-secondary" disabled={playerVoteId === ''} on:click={vote}
			>Voter</button
		>
	</div>
	<div data-popup="popupAutocomplete" class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto">
		<Autocomplete
			bind:input={playerVoteInput}
			options={playerList}
			on:selection={onPopupDemoSelect}
			emptyState="Aucun joueur n'a été trouvé."
		/>
	</div>
</div>
