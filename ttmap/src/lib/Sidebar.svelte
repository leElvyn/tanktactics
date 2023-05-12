<script lang="ts">
    import ActionList from "./actionList.svelte";
    import { slide } from "svelte/transition"
</script>
<div class="md:visible invisible absolute right-0 h-screen w-1/4 bg-slate-500" transition:slide>

    <ActionList />
</div>