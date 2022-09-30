<script>
    import { browser } from '$app/environment';

    let brightness = 0;
	let brightness_input_disabled = true;
	function setBrightness() {
        if(browser) {
            fetch("/api/strip/brightness", {
                method: "post",
                body: brightness.toString(),
            });
        }
	}
    function getBrightness() {
        if(browser) {
            fetch("/api/strip/brightness")
            .then((response) => response.text())
            .then((data) => {
                brightness = parseFloat(data);
				brightness_input_disabled = false;
            })
        }
	}
    getBrightness();
</script>

<main>
	<h1>Brightness</h1> 
	<input type="range" min="0" max="255" bind:value={brightness} on:change={setBrightness} disabled={brightness_input_disabled}>
	<p>
		<button on:click={setBrightness}>
			Update
		</button>
	</p>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 1.5em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
