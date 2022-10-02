<script>
	import Spotify from './lib/Spotify.svelte';
	import Brightness from './lib/Brightness.svelte';
	import FillAnimation from './lib/FillAnimation.svelte';
	import RainbowAnimation from './lib/RainbowAnimation.svelte';
	import PrideAnimation from './lib/PrideAnimation.svelte';
	import TheaterAnimation from './lib/TheaterAnimation.svelte';
</script>

<main>
	<Spotify/>
	<Brightness/>
	<FillAnimation/>
	<RainbowAnimation/>
	<PrideAnimation/>
	<TheaterAnimation/>
</main>

<style>
	main {
		text-align: center;
		margin: 0 auto;
	}
</style>
