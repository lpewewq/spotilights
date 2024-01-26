<script>
    import List, { Item, Text, Graphic } from "@smui/list";
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let schema;
    export let model;
    export let selected_key;
    export let path = "";
    export let expanded = false;
</script>

<Item
    activated={selected_key == path + "/"}
    on:click={() => {
        expanded = !expanded;

        dispatch("select", {
            model: model,
            model_schema: schema.definitions[model.name],
            key: null,
            schema: null,
            selected_key: path + "/",
        });
    }}
>
    <Graphic class="material-icons" aria-hidden="true"
        >subdirectory_arrow_right</Graphic
    >
    <Text>{schema.definitions[model.name].title}</Text>
</Item>

{#if expanded}
    {#if Object.entries(model).length > 1}
        <List style="padding-left: 10px;">
            {#each Object.entries(model) as [key, value]}
                {#if key == "animation"}
                    <svelte:self
                        {schema}
                        model={model.animation}
                        {selected_key}
                        path={path + "/" + model.name}
                        on:select
                    />
                {:else if key == "animations"}
                    <List>
                        {#each model.animations as sub_model, i}
                            <svelte:self
                                {schema}
                                model={sub_model}
                                {selected_key}
                                path={path + "/" + i + sub_model.name}
                                on:select
                            />
                        {/each}
                    </List>
                {:else if key != "name"}
                    <Item
                        activated={selected_key == path + "/" + key}
                        on:click={() => {
                            dispatch("select", {
                                model: model,
                                model_schema: schema.definitions[model.name],
                                key: key,
                                schema: schema.definitions[model.name]
                                    .properties[key],
                                selected_key: path + "/" + key,
                            });
                        }}
                    >
                        <Graphic class="material-icons" aria-hidden="true"
                            >tune</Graphic
                        >
                        <Text
                            >{schema.definitions[model.name].properties[key]
                                .title}</Text
                        >
                    </Item>
                {/if}
            {/each}
        </List>
    {:else}
        <p>No configs</p>
    {/if}
{/if}
