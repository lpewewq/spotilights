<script>
	import LayoutGrid, { Cell } from "@smui/layout-grid";
	import Spotify from "./lib/Spotify.svelte";
	import Brightness from "./lib/Brightness.svelte";
	import Animations from "./lib/Animations.svelte";
</script>

<LayoutGrid>
	<Cell span={12}>
		<Spotify />
	</Cell>
	<Cell span={12}>
		<Brightness />
	</Cell>
	<Cell span={12}>
		<Animations />
	</Cell>
</LayoutGrid>
