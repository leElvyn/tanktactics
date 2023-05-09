<script lang="ts">
    import { onMount } from "svelte";

    let map;
    onMount(async () => {
        (await import("./mapMain")).main(map)
    });
</script>
    <div id="map" bind:this={map} />
