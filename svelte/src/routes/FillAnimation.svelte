<script>
    import { browser } from '$app/environment';

    let color = "#FF0000";
    function hex_to_RGB(hex) {
        var m = hex.match(/^#?([\da-f]{2})([\da-f]{2})([\da-f]{2})$/i);
        return {
            r: parseInt(m[1], 16),
            g: parseInt(m[2], 16),
            b: parseInt(m[3], 16)
        };
    }
	function start() {
        if(browser && color != null) {
            let rgb = hex_to_RGB(color);
            fetch("/api/strip/fill", {
                method: "POST",
                headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({red: rgb.r, green: rgb.g, blue: rgb.b})
            });
        }
	}
</script>

<main>
	<h1>Fill</h1>
	<input type="color" bind:value={color}>
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
