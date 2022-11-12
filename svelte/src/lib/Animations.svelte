<script>
	import LayoutGrid, { Cell } from "@smui/layout-grid";
	import Animation from "./Animation.svelte";
	import LinearProgress from "@smui/linear-progress";

	async function getAnimations() {
		return await fetch("/api/animator/models").then((response) =>
			response.json()
		);
	}
</script>

{#await getAnimations()}
	<LinearProgress indeterminate />
{:then animations}
	<LayoutGrid style="padding: 0px;">
		{#each animations as animation}
			<Cell span={12}>
				<Animation {...animation} />
			</Cell>
		{/each}
	</LayoutGrid>
{/await}
