<script>
	import Spotify from './Spotify.svelte';
	import Brightness from './Brightness.svelte';
	import FillAnimation from './FillAnimation.svelte';
	import RainbowAnimation from './RainbowAnimation.svelte';
	import PrideAnimation from './PrideAnimation.svelte';
	import TheaterAnimation from './TheaterAnimation.svelte';
	import SpotifyAnimation from './SpotifyAnimation.svelte';
</script>

<main>
	<Spotify/>
	<Brightness/>
	<SpotifyAnimation/>
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
