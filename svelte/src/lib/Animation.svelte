<script>
    export let name;
    export let model;

    async function start() {
        await fetch("/api/animator/start", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: name, model: model }),
        });
    }
</script>

<main>
    <button on:click={start}> {name} </button>
</main>

<style>
    button {
        color: #ff3e00;
    }
    main {
        display: grid;
        padding: 16px;
        box-shadow: 2px 2px 2px #111;
        border: 2px solid #111;
    }
</style>
