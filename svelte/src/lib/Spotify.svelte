<script>
	let current_user_promise = get_current_user();

	async function get_current_user() {
		return await fetch("/api/spotify/current-user").then((response) =>
			response.json()
		);
	}

	async function connect() {
		let body = await fetch("/api/spotify/connect").then((response) =>
			response.json()
		);
		window.location.replace(body.authorize_url);
	}

	async function disconnect() {
		current_user_promise = await fetch("/api/spotify/disconnect", {
			method: "POST",
		}).then(() => get_current_user());
	}
</script>

<main>
	{#await current_user_promise}
		<p>Loading...</p>
	{:then current_user}
		{#if current_user == null}
			<img src="src/assets/spotify_logo.png" alt="Spotify" />
			<section>
				<h1>Not connected!</h1>
				<button on:click={connect}> Connect </button>
			</section>
		{:else}
			<img src={current_user.images[0].url} alt="Spotify" />
			<section>
				<h1>{current_user.display_name}</h1>
				<button on:click={disconnect}> Disconnect </button>
			</section>
		{/if}
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
</main>

<style>
	h1 {
		color: #ff3e00;
		font-size: 2em;
		font-weight: 100;
	}
	img {
		border-radius: 50%;
		border: 2px solid #111;
		height: 150px;
	}
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
