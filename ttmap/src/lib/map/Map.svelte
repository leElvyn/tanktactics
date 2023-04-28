<script lang="ts">
    import { onMount } from "svelte";
    import { main } from "./mapMain";

    let map;
    onMount(async () => {
        console.log("map")
        main(map);
    });
</script>
    <div id="map" bind:this={map} />
