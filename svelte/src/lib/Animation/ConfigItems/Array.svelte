<script>
    import List, { Item, Meta, Label } from "@smui/list";
    import Checkbox from "@smui/checkbox";

    export let model;
    export let schema;
</script>

{#if schema.items.type == "boolean"}
    <List checkList>
        {#each model as m, i}
            <Item>
                <Label>{schema.description} {i}</Label>
                <Meta>
                    <Checkbox bind:checked={m} />
                </Meta>
            </Item>
        {/each}
    </List>
{/if}
