<script>
    import { browser } from '$app/environment';

    let delay = 20;
	function start() {
        if(browser) {
            fetch("/api/strip/rainbow", {
                method: "POST",
                body: (delay / 1000).toString()
            });
        }
	}
</script>

<main>
	<h1>Rainbow</h1>
	<input type="range" min=0 max=100 bind:value={delay}>
    <button on:click={start}>Start</button>
</main>

<style>
	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 1.5em;
		font-weight: 100;
	}
</style>
