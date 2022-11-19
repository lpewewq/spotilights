<script>
    import List, { Item, Graphic, Label } from "@smui/list";
    import Radio from "@smui/radio";
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let model;
    export let schema;

    let value = model;
    $: {
        dispatch("changed", {
            value: value,
        });
    }
</script>

<List radioList>
    {#each schema.enum as key}
        <Item>
            <Graphic>
                <Radio bind:group={value} value={key} />
            </Graphic>
            <Label>{key}</Label>
        </Item>
    {/each}
</List>
