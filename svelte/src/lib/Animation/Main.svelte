<script>
	import LayoutGrid, { Cell } from "@smui/layout-grid";
	import Animation from "./Animation.svelte";
	import LinearProgress from "@smui/linear-progress";

	async function getModels() {
		return await fetch("/api/animator/models").then((response) =>
			response.json()
		);
	}
	async function getSchema() {
		return await fetch("/api/animator/schema").then((response) =>
			response.json()
		);
	}
</script>

{#await getSchema()}
	<LinearProgress indeterminate />
{:then schema}
	{#await getModels()}
		<LinearProgress indeterminate />
	{:then models}
		<LayoutGrid style="padding: 0px;">
			{#each models as model}
				<Cell span={12}>
					<Animation {schema} {model} />
				</Cell>
			{/each}
		</LayoutGrid>
	{/await}
{/await}
