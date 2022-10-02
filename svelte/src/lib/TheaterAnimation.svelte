<script>
    let delay = 50;
	function start() {
		fetch("/api/strip/theater", {
			method: "POST",
			body: (delay / 1000).toString()
		});
	}
</script>

<main>
	<h1>Theater</h1>
	<input type="range" min=0 max=100 bind:value={delay}>
    <button on:click={start}>Start</button>
</main>

<style>
	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 1em;
		font-weight: 100;
	}
</style>
