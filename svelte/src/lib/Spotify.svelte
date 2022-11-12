<script>
	import { onMount } from "svelte";
	import Card, { Actions } from "@smui/card";
	import Button, { Label, Icon } from "@smui/button";
	import LayoutGrid, { Cell } from "@smui/layout-grid";

	let current_user = null;

	async function getCurrentUser() {
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
		current_user = await fetch("/api/spotify/disconnect", {
			method: "POST",
		}).then(() => getCurrentUser());
	}

	onMount(async () => {
		current_user = await getCurrentUser();
	});
</script>

<Card>
	<LayoutGrid align="left">
		<Cell align="middle" span={4}>
			{#if current_user == null}
				<img
					src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg"
					alt="Spotify"
				/>
			{:else}
				<img src={current_user.images[0].url} alt="Spotify" />
			{/if}
		</Cell>
		<Cell align="middle" span={8}>
			{#if current_user == null}
				<h1>Not connected!</h1>
			{:else}
				<h1>{current_user.display_name}</h1>
			{/if}
		</Cell>
	</LayoutGrid>
	<Actions fullBleed>
		{#if current_user == null}
			<Button on:click={connect}>
				<Label>Connect</Label>
				<Icon class="material-icons">link</Icon>
			</Button>
		{:else}
			<Button on:click={disconnect}>
				<Label>Disconnect</Label>
				<Icon class="material-icons">link_off</Icon>
			</Button>
		{/if}
	</Actions>
</Card>

<style>
	h1 {
		color: #ff3e00;
		font-size: 4em;
		font-weight: 100;
	}
	img {
		border-radius: 50%;
		border: 2px solid #111;
		height: 150px;
	}
</style>
