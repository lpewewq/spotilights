<script>
    import Checkbox from "@smui/checkbox";
    import { Item, Label, Meta } from "@smui/list";
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let model;
    export let schema;

    let checked = model;
    $: {
        dispatch("changed", {
            value: checked,
        });
    }
</script>

<Item>
    <Label>{schema.description}</Label>
    <Meta>
        <Checkbox bind:checked />
    </Meta>
</Item>
