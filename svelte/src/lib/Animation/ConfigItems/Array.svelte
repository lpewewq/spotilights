<script>
    import List from "@smui/list";
    import BooleanConfig from "./Boolean.svelte";
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let model;
    export let schema;
</script>

<List checkList>
    {#each model as sub_model, i}
        {#if schema.items.type == "boolean"}
            <BooleanConfig
                model={sub_model}
                {schema}
                on:changed={(event) => {
                    model[i] = event.detail.value;
                    dispatch("changed", {
                        value: model,
                    });
                }}
            />
        {/if}
    {/each}
</List>
