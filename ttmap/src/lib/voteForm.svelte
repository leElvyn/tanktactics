<script lang="ts">
	import type { AutocompleteOption, PopupSettings } from '@skeletonlabs/skeleton';
	import { Autocomplete } from '@skeletonlabs/skeleton';
	import { popup } from '@skeletonlabs/skeleton';
	import { get } from 'svelte/store';
	import { gameStore } from './stores/gameStore';
	import type { Game } from './interfaces';
	import { getCookie } from './utils';

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

	const playerList: AutocompleteOption[] = [];
	const playerNamesList: string[] = [];

	$: {
		game.players.forEach((player) => {
			if (!player.is_dead) {
				playerList.push({ label: player.name, value: player.id });
				playerNamesList.push(player.name);
			}
		});
		console.log(playerNamesList);
	}

	let playerVoteInput: string = '';
	let playerVoteId: string = '';

	function onPopupDemoSelect(event: any) {
		playerVoteInput = event.detail.label;
		playerVoteId = event.detail.value;
	}
	async function vote() {
		console.log(playerVoteId);
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
		console.log(data);
	}
</script>

<div class="text-token w-full max-w-sm space-y-2">
	<div class="input-group input-group-divider grid-cols-[auto_1fr_auto]">
		<input
			class="input autocomplete"
			type="search"
			name="autocomplete-search"
			bind:value={playerVoteInput}
			placeholder="Search alive players ..."
			use:popup={popupSettings}
			on:input={() => (playerVoteId = '')}
		/>
		<button class="variant-filled-secondary" disabled={playerVoteId === ''} on:click={vote}
			>Vote</button
		>
	</div>
	<div data-popup="popupAutocomplete" class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto">
		<Autocomplete
			bind:input={playerVoteInput}
			options={playerList}
			on:selection={onPopupDemoSelect}
		/>
	</div>
</div>
