<script>
    import Slider from "@smui/slider";
    import FormField from "@smui/form-field";
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

<FormField align="end" style="display: flex;">
    <Slider
        style="flex-grow: 1;"
        bind:value
        min={schema.minimum}
        max={schema.maximum}
        step={schema.multipleOf}
    />
    <span
        slot="label"
        style="padding-right: 12px; width: max-content; display: block;"
    >
        <p>{value} {schema.description}</p>
    </span>
</FormField>
