<script>
    export let model;

    let hex = rgbToHex(model.r, model.g, model.b);

    $: {
        model = hexToRgb(hex);
    }

    function rgbToHex(r, g, b) {
        return (
            "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)
        );
    }
    function hexToRgb(hex) {
        let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result
            ? {
                  r: parseInt(result[1], 16),
                  g: parseInt(result[2], 16),
                  b: parseInt(result[3], 16),
              }
            : null;
    }
</script>

<input type="color" bind:value={hex} />
