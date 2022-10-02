<script>
	function start() {
		fetch("/api/strip/pride", {
			method: "POST",
		});
	}
</script>

<main>
	<h1>Pride</h1>
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
