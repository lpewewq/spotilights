<script>
	import { onMount } from "svelte";
	import Slider from "@smui/slider";
	import Card, { Actions } from "@smui/card";
	import Button, { Label } from "@smui/button";

	let brightness = 0;
	let loaded = false;
	$: if (loaded) {
		setBrightness(brightness);
	}

	function setBrightness(brightness) {
		fetch("/api/strip/brightness", {
			method: "POST",
			body: brightness.toString(),
		});
	}
	async function getBrightness() {
		return await fetch("/api/strip/brightness")
			.then((response) => response.text())
			.then((body) => parseFloat(body));
	}
	async function stop() {
		await fetch("/api/animator/stop", {
			method: "POST",
		});
	}
	onMount(async () => {
		brightness = await getBrightness();
		loaded = true;
	});
</script>

<Card>
	<Slider
		style="flex-grow: 1;"
		bind:value={brightness}
		min={0}
		max={255}
		step={4}
		discrete
	/>
	<Actions fullBleed>
		<Button on:click={stop}>
			<Label>Stop</Label>
			<i class="material-icons" aria-hidden="true">stop_circle</i>
		</Button>
	</Actions>
</Card>
