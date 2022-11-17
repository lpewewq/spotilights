<script>
    import Card, { Actions } from "@smui/card";
    import Accordion, {
        Content as AccordionContent,
        Header,
        Panel,
    } from "@smui-extra/accordion";
    import Badge from "@smui-extra/badge";
    import Button, { Label } from "@smui/button";
    import AnimationConfig from "./AnimationConfig.svelte";

    export let schema;
    export let model;

    async function start() {
        await fetch("/api/animator/start", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(model),
        });
    }
</script>

<Card>
    <Accordion>
        <Panel>
            <Header>
                <h1>
                    {model.name}
                </h1>
            </Header>
            <AccordionContent>
                <AnimationConfig {schema} model={model.animation} />
            </AccordionContent>
        </Panel>
    </Accordion>

    <Actions fullBleed>
        <Button on:click={start}>
            <Label>Start</Label>
            <i class="material-icons" aria-hidden="true">play_circle</i>
            {#if model.needs_spotify}
                <Badge color="black" aria-label="Animation needs Spotify">
                    <img
                        src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg"
                        alt="Spotify"
                    />
                </Badge>
            {/if}
        </Button>
    </Actions>
</Card>

<style>
    img {
        border-radius: 50%;
        border: 2px solid #111;
        height: 25px;
    }
    h1 {
        color: #ff3e00;
        font-size: 2em;
        font-weight: 100;
    }
</style>
