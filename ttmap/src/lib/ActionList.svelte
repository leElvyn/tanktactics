<script lang="ts">
	import { identity } from 'svelte/internal';


	import AttackInteraction from './interactions/AttackInteraction.svelte';
    import MoveInteraction from './interactions/MoveInteraction.svelte';
	import TransferInteraction from './interactions/TransferInteraction.svelte';
	import UpgradeInteraction from './interactions/UpgradeInteraction.svelte';
	import { gameStore } from './stores/gameStore';
    import { selfStore } from './stores/selfStore';

    enum Selected {
        Nothing = 0,
        Move = 1,
        Shoot = 2,
        Transfer = 3,
        Upgrade = 4, 
        Vote = 5
    };
    
    let game = $gameStore;
    let self = $selfStore;

    selfStore.subscribe((value) => {
        self = value
    })

    let selected: Selected = Selected.Nothing;

    function assignVisible(newState: Selected) {
        if (selected == newState){
            selected = Selected.Nothing;
        }
        else {
            selected = newState; 
        }
    }
    $: {
        if (self?.tank.action_points == 0) {
            selected = Selected.Nothing
        }
    }
</script>

<div class="actions-list flex-col items-center flex w-[70%]">
    <div class="flex flex-row justify-evenly w-full">
	    <button class="action-button btn variant-filled" disabled={self?.tank.action_points == 0} type="button" on:click={() => {assignVisible(Selected.Move)}}>Move</button>
	    <button class="action-button btn variant-filled" disabled={self?.tank.action_points == 0} type="button" on:click={() => {assignVisible(Selected.Shoot)}}>Shoot</button>
    </div>
    <div class="flex flex-row justify-evenly w-full">
	    <button class="action-button btn variant-filled" disabled={self?.tank.action_points == 0} type="button" on:click={() => {assignVisible(Selected.Transfer)}}>Transfer</button>
	    <button class="action-button btn variant-filled" disabled={self?.tank.action_points == 0} type="button" on:click={() => {assignVisible(Selected.Upgrade)}}>Upgrade</button>
    </div>

    {#if selected == Selected.Move}
        <MoveInteraction />
    {/if}
    {#if selected == Selected.Shoot}
        <AttackInteraction />
    {/if}
    {#if selected == Selected.Transfer}
        <TransferInteraction />
    {/if}
    {#if selected == Selected.Upgrade}
        <UpgradeInteraction />
    {/if}
</div>

<style>
	.action-button {
		@apply mt-4 w-20;
	}
</style>
