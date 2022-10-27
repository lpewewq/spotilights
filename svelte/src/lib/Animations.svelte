<script>
	import Animation from "./Animation.svelte";

	async function getAnimations() {
		return await fetch("/api/animator/models").then((response) =>
			response.json()
		);
	}
</script>

{#await getAnimations()}
	<p>Loading...</p>
{:then animations}
	{#each animations as animation}
		<Animation {...animation} />
	{/each}
{/await}
