<script>
	import Spotify from "./lib/Spotify.svelte";
	import Brightness from "./lib/Brightness.svelte";
	import Animations from "./lib/Animations.svelte";
</script>

<main>
	<Spotify />
	<Brightness />
	<Animations />
</main>

<style>
	main {
		text-align: center;
		margin: 0 auto;
	}
</style>
