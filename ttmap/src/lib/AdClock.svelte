<script lang="ts">
	import type { Game } from './interfaces';
	import { gameStore } from './stores/gameStore';

	let game = $gameStore;

    let days: number;
    let hours: number;
    var minutes: number;
    var seconds: number;

 
	function CountDownTimer(end: number) {

		let _second = 1000;
		let _minute = _second * 60;
		let _hour = _minute * 60;
		let _day = _hour * 24;
		let timer: number;

		function showRemaining() {
			let now = new Date().getTime();
			let distance = end - now;
			if (distance < 0) {
				clearInterval(timer);
				return;
			}
			days = Math.floor(distance / _day);
			hours = Math.floor((distance % _day) / _hour);
			minutes = Math.floor((distance % _hour) / _minute);
			seconds = Math.floor((distance % _minute) / _second);

		}
        showRemaining()

		timer = setInterval(showRemaining, 1000);
	}

    CountDownTimer(new Date(game!.next_ad_end).valueOf() - (new Date().getTimezoneOffset() * 60 * 1000)); // 7);

</script>

<div class="font-bold text-2xl">
    <span>Next Action Hour in : </span><span class="w-80 inline-block">{minutes} minutes and {seconds} seconds.</span>
</div>
