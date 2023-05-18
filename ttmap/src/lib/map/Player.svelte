<script lang="ts">
	import type { Player } from '$lib/interfaces';

	export let player: Player;

	let label = '';
	let red_heart = '❤️ ';
	let black_heart = '🖤 ';
	for (let i = 0; i < 3; i++) {
		if (i < player.tank.health_points!) {
			label += red_heart;
		} else {
			label += black_heart;
		}
	}
</script>

<canvas height="512" width="512" />
<div>
	<div class="card p-4 m-3 ml-4 mr-4 w-11/12 flex justify-center">
		<span class="font-sans font-semibold text-center">
			{player.name} &nbsp;&nbsp;
			<span class="bg-yellow-300 text-black h-6 w-6 inline-block text-center">
				{player.tank.range}
			</span>&nbsp;&nbsp;
			<span class="bg-green-500 rounded-full h-6 w-6 inline-block text-center">
				{player.tank.action_points}
			</span>
			{label}
		</span>
	</div>
</div>
