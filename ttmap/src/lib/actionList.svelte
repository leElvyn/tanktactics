<script lang="ts">

	import MoveInteraction from './interactions/moveInteraction.svelte';
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

    let selected: Selected = Selected.Nothing;

    function assignVisible(newState: Selected) {
        if (selected == Selected.Nothing){
            selected = newState; 
        }
        else {
            selected = Selected.Nothing;
        }
    }
</script>

<div class="actions-list flex-col items-center flex">
	<button class="action-button btn variant-filled" disabled={self?.tank.action_points == 0} type="button" on:click={() => {assignVisible(Selected.Move)}}>Move</button>
{#if selected == Selected.Move}
    <MoveInteraction />
{/if}
	<button class="action-button btn variant-filled" disabled={self?.tank.action_points == 0} type="button" on:click={() => {assignVisible(Selected.Move)}}>Shoot</button>
	<button class="action-button btn variant-filled" disabled={self?.tank.action_points == 0} type="button" on:click={() => {assignVisible(Selected.Move)}}>Transfer</button>
	<button class="action-button btn variant-filled" disabled={self?.tank.action_points == 0} type="button" on:click={() => {assignVisible(Selected.Move)}}>Upgrade</button>
</div>

<style>
	.action-button {
		@apply mt-4 w-20;
	}
</style>
