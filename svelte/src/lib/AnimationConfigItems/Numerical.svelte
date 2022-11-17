<script>
    import Slider from "@smui/slider";
    import FormField from "@smui/form-field";

    export let model;
    export let schema;
</script>

<FormField align="end" style="display: flex;">
    <Slider
        style="flex-grow: 1;"
        bind:value={model}
        min={schema.minimum}
        max={schema.maximum}
        step={schema.multipleOf}
    />
    <span
        slot="label"
        style="padding-right: 12px; width: max-content; display: block;"
    >
        <p>{model} {schema.description}</p>
    </span>
</FormField>
