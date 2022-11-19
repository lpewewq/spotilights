<script>
    import Drawer, {
        AppContent,
        Content,
        Header,
        Subtitle,
        Title,
    } from "@smui/drawer";
    import { Separator } from "@smui/list";

    import ArrayConfig from "./ConfigItems/Array.svelte";
    import BooleanConfig from "./ConfigItems/Boolean.svelte";
    import StringConfig from "./ConfigItems/String.svelte";
    import ColorConfig from "./ConfigItems/Color.svelte";
    import NumericalConfig from "./ConfigItems/Numerical.svelte";
    import ConfigList from "./ConfigList.svelte";

    export let schema;
    export let model;

    let select = {
        model: model,
        model_schema: schema.definitions[model.name],
        key: null,
        schema: null,
        selected_key: "/",
    };

    function onChange(event) {
        select.model[select.key] = event.detail.value;
    }
</script>

<div class="drawer-container">
    <Drawer>
        <Content>
            <ConfigList
                {schema}
                {model}
                selected_key={select.selected_key}
                expanded={true}
                on:select={(event) => {
                    select = event.detail;
                }}
            />
        </Content>
    </Drawer>
    <AppContent class="app-content">
        <main class="main-content">
            {#if select != null}
                <Header>
                    <Title>{select.model_schema.title}</Title>
                    <Subtitle>{select.model_schema.description}</Subtitle>
                </Header>
                <Separator />
                {#key select.key}
                    {#if select.key != null}
                        <p>{select.schema.title}</p>
                        {#if select.schema.type == "number"}
                            <NumericalConfig
                                model={select.model[select.key]}
                                schema={select.schema}
                                on:changed={onChange}
                            />
                        {:else if select.schema.type == "color"}
                            <ColorConfig
                                model={select.model[select.key]}
                                on:changed={onChange}
                            />
                        {:else if select.schema.type == "array"}
                            <ArrayConfig
                                model={select.model[select.key]}
                                schema={select.schema}
                                on:changed={onChange}
                            />
                        {:else if select.schema.type == "boolean"}
                            <BooleanConfig
                                model={select.model[select.key]}
                                schema={select.schema}
                                on:changed={onChange}
                            />
                        {:else if select.schema.type == "string"}
                            <StringConfig
                                model={select.model[select.key]}
                                schema={select.schema}
                                on:changed={onChange}
                            />
                        {:else}
                            <p>Type not implemented.</p>
                        {/if}
                    {:else}
                        <p>Nothing selected.</p>
                    {/if}
                {/key}
            {:else}
                <p>Nothing selected.</p>
            {/if}
        </main>
    </AppContent>
</div>

<style>
    /* These classes are only needed because the
      drawer is in a container on the page. */
    .drawer-container {
        position: relative;
        display: flex;
        height: 350px;
        max-width: 600px;
        border: 1px solid
            var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.1));
        overflow: hidden;
        z-index: 0;
    }

    * :global(.app-content) {
        flex: auto;
        overflow: auto;
        position: relative;
        flex-grow: 1;
    }

    .main-content {
        overflow: auto;
        padding: 16px;
        height: 100%;
        box-sizing: border-box;
    }
</style>
