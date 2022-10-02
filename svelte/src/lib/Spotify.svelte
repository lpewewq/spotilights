<script>
    async function oauth() {
		let body = await fetch("/api/spotify/oauth").then(response => response.json());
		window.location.replace(body.authorize_url);
	}
    async function getMe() {
		return await fetch("/api/spotify/current-user").then(response => response.json());
	}
</script>

<main>
	<div>
		{#await getMe()}
			Loading...
		{:then current_user}
			{#if current_user == null}
				<button on:click={oauth}>
					Connect Spotify
				</button>
			{:else}
				<h1>{ current_user.display_name}</h1> 
			{/if}
		{/await}
	</div>
</main>
 
<style>
	h1 {
		color: #ff3e00;
		font-size: 1em;
		font-weight: 100;
	}
</style>
