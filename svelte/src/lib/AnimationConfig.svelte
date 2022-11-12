<script>
    import Drawer, {
        AppContent,
        Content,
        Header,
        Title,
        Subtitle,
    } from "@smui/drawer";
    import List, { Item, Text, Separator, Graphic } from "@smui/list";

    import NumericalConfig from "./AnimationConfigItems/Numerical.svelte";

    export let model;
    export let concrete_schema;

    let unique = {};
    let config_key = null;
    let access_chain = [];
    let current_model = model;
    let current_schema = concrete_schema;
    let current_path = model.animation;

    function update_chain() {
        let m = model;
        let schema = concrete_schema;
        let path = m.animation;
        for (let i in access_chain) {
            m = access_chain[i](m);
            schema = access_chain[i](schema);
            path += " / " + m.animation;
        }
        current_model = m;
        current_schema = schema;
        current_path = path;
        config_key = null;
    }
</script>

<div class="drawer-container">
    <Drawer>
        <Header>
            <Title>{current_model.animation}</Title>
            <Subtitle>{current_path}</Subtitle>
        </Header>
        <Content>
            <List>
                <Separator />
                {#each Object.entries(current_model.config) as [key, value]}
                    <Item
                        activated={config_key === key}
                        on:click={() => {
                            config_key = key;
                            unique = {};
                        }}
                    >
                        {#if key == "sub" || key == "subs"}
                            <Graphic class="material-icons" aria-hidden="true"
                                >subdirectory_arrow_right</Graphic
                            >
                        {:else}
                            <Graphic class="material-icons" aria-hidden="true"
                                >tune</Graphic
                            >
                        {/if}
                        <Text>{key}</Text>
                    </Item>
                {/each}
                <Separator />
                <Item
                    disabled={current_model == model}
                    on:click={() => {
                        access_chain.pop();
                        update_chain();
                        if ("sub" in current_model.config) {
                            config_key = "sub";
                        } else if ("subs" in current_model.config) {
                            config_key = "subs";
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
            {#if config_key != null}
                {#if config_key == "sub"}
                    <List>
                        <Item
                            on:click={() => {
                                access_chain.push((m) => m.config.sub);
                                update_chain();
                            }}
                        >
                            <Graphic class="material-icons" aria-hidden="true"
                                >navigate_next</Graphic
                            >
                            <Text
                                >{current_model.config[config_key]
                                    .animation}</Text
                            >
                        </Item>
                    </List>
                {:else if config_key == "subs"}
                    <List>
                        {#each current_model.config["subs"] as sub, i}
                            <Item
                                on:click={() => {
                                    access_chain.push((m) => m.config.subs[i]);
                                    update_chain();
                                }}
                            >
                                <Graphic
                                    class="material-icons"
                                    aria-hidden="true">navigate_next</Graphic
                                >
                                <Text>{sub.animation}</Text>
                            </Item>
                        {/each}
                    </List>
                {:else}
                    {#key unique}
                        <p>{current_schema.config[config_key]["title"]}</p>
                        {#if "config_type" in current_schema.config[config_key]}
                            {#if current_schema.config[config_key].config_type == "Numerical"}
                                <NumericalConfig
                                    bind:model={current_model.config[
                                        config_key
                                    ]}
                                    concrete_schema={current_schema.config[
                                        config_key
                                    ]}
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
