<script>
	import { onMount } from "svelte";

	let brightness = 0;
	let slider;
	function setBrightness() {
		fetch("/api/strip/brightness", {
			method: "POST",
			body: brightness.toString(),
		});
	}
	async function getBrightness() {
		let body = await fetch("/api/strip/brightness").then((response) =>
			response.text()
		);
		brightness = parseFloat(body);
		slider.disabled = false;
	}
	onMount(async () => {
		await getBrightness();
	});
</script>

<main>
	<h1>Brightness</h1>
	<input
		type="range"
		min="0"
		max="255"
		bind:this={slider}
		bind:value={brightness}
		on:change={setBrightness}
		disabled
	/>
</main>

<style>
	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 1em;
		font-weight: 100;
	}
</style>
