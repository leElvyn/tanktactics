<script lang="ts">
import { modalStore, type ModalSettings } from '@skeletonlabs/skeleton';
const alert: ModalSettings = {
	type: 'alert',
	// Data
	title: 'Example Alert',
	body: 'This is an example modal.',
	image: 'https://i.imgur.com/WOgTG96.gif',
};
</script>

<div class="actions-list flex-col items-center flex">
    <button class="action-button" type="button" on:click={() => {console.log(modalStore);modalStore.trigger(alert)}}>Move</button>
    <button class="action-button" type="button">Attack</button>

</div>

<style>
    .action-button {
        @apply btn variant-filled mt-4 w-20;
    }
</style>