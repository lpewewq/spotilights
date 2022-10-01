<script>
    import { browser } from '$app/environment';

	let spotify_me = null;
	let spotify_me_fetched = false;
    function oauth() {
        if(browser) {
            fetch("/api/spotify/oauth")
            .then((response) => response.json())
            .then((data) => {
            	window.location.replace(data.authorize_url);
            })
        }
	}
    function getMe() {
        if(browser) {
            fetch("/api/spotify/current-user")
            .then((response) => response.json())
            .then((me) => {
				spotify_me_fetched = true;
				spotify_me = me;
            })
        }
	}
	getMe();
</script>

<main>
	<div>
		{#if spotify_me_fetched}
			{#if spotify_me == null}
				<button on:click={oauth}>
					Connect Spotify
				</button>
			{:else}
                <h1>{ spotify_me.display_name}</h1> 
			{/if}
		{:else}
			Loading...
		{/if}
	</div>
</main>
 
<style>
	/* img {
	    width: 5%;
	} */
	h1 {
		color: #ff3e00;
		font-size: 1.5em;
		font-weight: 100;
	}
</style>
