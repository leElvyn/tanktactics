<script lang="ts">
    import { onMount } from "svelte";
    import { main } from "./mapMain";

    let map;
    onMount(async () => {
        main(map);
    });
</script>
    <div id="map" bind:this={map} />
