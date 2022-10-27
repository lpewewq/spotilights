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
	async function stop() {
		await fetch("/api/animator/stop", {
			method: "POST",
		});
	}
	onMount(async () => {
		await getBrightness();
	});
</script>

<main>
	<input
		type="range"
		min="0"
		max="255"
		bind:this={slider}
		bind:value={brightness}
		on:change={setBrightness}
		disabled
	/>
	<button on:click={stop}> Stop </button>
</main>

<style>
	button {
		color: #ff3e00;
	}
	main {
		display: grid;
		grid-template-columns: 1fr 1fr;
		padding: 16px;
		box-shadow: 2px 2px 2px #111;
		border: 2px solid #111;
	}
</style>
