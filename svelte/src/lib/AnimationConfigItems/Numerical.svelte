<script>
    import Slider from "@smui/slider";
    import FormField from "@smui/form-field";

    export let model;
    export let concrete_schema;
</script>

<FormField align="end" style="display: flex;">
    <Slider
        style="flex-grow: 1;"
        bind:value={model}
        min={concrete_schema.minimum}
        max={concrete_schema.maximum}
        step={concrete_schema.multipleOf}
    />
    <span
        slot="label"
        style="padding-right: 12px; width: max-content; display: block;"
    >
        <p>{model}</p>
    </span>
</FormField>
