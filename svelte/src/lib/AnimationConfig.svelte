<script>
    import Drawer, {
        AppContent,
        Content,
        Header,
        Title,
        Subtitle,
    } from "@smui/drawer";
    import List, { Item, Text, Separator, Graphic } from "@smui/list";

    import ColorConfig from "./AnimationConfigItems/Color.svelte";
    import NumericalConfig from "./AnimationConfigItems/Numerical.svelte";

    export let schema;
    export let model;

    let unique = {};
    let config_key = null;
    let access_chain = [];
    let current_model = model;
    let current_schema = schema.definitions[model.name];
    let current_path = model.name;

    function update_chain() {
        let m = model;
        let path = m.name;
        for (let i in access_chain) {
            m = access_chain[i](m);
            path += " / " + m.name;
        }
        current_model = m;
        current_schema = schema.definitions[current_model.name];
        current_path = path;
        config_key = null;
    }
</script>

<div class="drawer-container">
    <Drawer>
        <Header>
            <Title>{current_schema.title}</Title>
            <Subtitle>{current_schema.description}</Subtitle>
        </Header>
        <Content>
            <List>
                <Separator />
                {#each Object.entries(current_model) as [key, value]}
                    {#if key != "name"}
                        <Item
                            activated={config_key === key}
                            on:click={() => {
                                config_key = key;
                                unique = {};
                            }}
                        >
                            {#if key == "animation" || key == "animations"}
                                <Graphic
                                    class="material-icons"
                                    aria-hidden="true"
                                    >subdirectory_arrow_right</Graphic
                                >
                            {:else}
                                <Graphic
                                    class="material-icons"
                                    aria-hidden="true">tune</Graphic
                                >
                            {/if}
                            <Text>{current_schema.properties[key].title}</Text>
                        </Item>
                    {/if}
                {/each}
                <Separator />
                <Item
                    disabled={current_model == model}
                    on:click={() => {
                        access_chain.pop();
                        update_chain();
                        if ("animation" in current_model) {
                            config_key = "animation";
                        } else if ("animations" in current_model) {
                            config_key = "animations";
                        }
                    }}
                >
                    <Graphic class="material-icons" aria-hidden="true"
                        >navigate_before</Graphic
                    >
                    <Text>Back</Text>
                </Item>
            </List>
        </Content>
    </Drawer>
    <AppContent class="app-content">
        <main class="main-content">
            <!-- <p>{current_path}</p> -->
            {#if config_key != null}
                {#if config_key == "animation"}
                    <List>
                        <Item
                            on:click={() => {
                                access_chain.push((m) => m.animation);
                                update_chain();
                            }}
                        >
                            <Graphic class="material-icons" aria-hidden="true"
                                >navigate_next</Graphic
                            >
                            <Text
                                >{schema.definitions[
                                    current_model.animation.name
                                ].title}</Text
                            >
                        </Item>
                    </List>
                {:else if config_key == "animations"}
                    <List>
                        {#each current_model["animations"] as animation, i}
                            <Item
                                on:click={() => {
                                    access_chain.push((m) => m.animations[i]);
                                    update_chain();
                                }}
                            >
                                <Graphic
                                    class="material-icons"
                                    aria-hidden="true">navigate_next</Graphic
                                >
                                <Text
                                    >{schema.definitions[animation.name]
                                        .title}</Text
                                >
                            </Item>
                        {/each}
                    </List>
                {:else}
                    {#key unique}
                        <p>{current_schema.properties[config_key].title}</p>
                        {#if "config_type" in current_schema.properties[config_key]}
                            {#if current_schema.properties[config_key].config_type == "Numerical"}
                                <NumericalConfig
                                    bind:model={current_model[config_key]}
                                    schema={current_schema.properties[
                                        config_key
                                    ]}
                                />
                            {:else if current_schema.properties[config_key].config_type == "Color"}
                                <ColorConfig
                                    bind:model={current_model[config_key]}
                                />
                            {:else}
                                <p>Config type not implemented.</p>
                            {/if}
                        {:else}
                            <p>Not implemented.</p>
                        {/if}
                    {/key}
                {/if}
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
