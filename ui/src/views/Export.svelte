<script>
    import {TableSort} from 'svelte-tablesort'
    import DecodedData from "../components/DecodedData.svelte";

    export let router;
</script>

<div>
    <h1>Export</h1>
    {#if router.params.context === undefined }
        <div class="alert alert-warning" role="alert">No context selected! Go to <a href="/query">Query</a> and select a context to export.</div>
    {:else}
        {#await app.api.exportEntry(router.params.context)}
            Loading...
        {:then data}
            <h2>{router.params.context}</h2>
<!--            <pre>{#each data as line}{decodeData(line)}{/each}</pre>-->
            <textarea value={data} class="source"></textarea>
        {:catch error}
            <div class="alert alert-danger" role="alert">{error}</div>
        {/await}
    {/if}
</div>

<style>
    input {
        width: 100%;
    }

    :global(table td.marker) {
        padding: 0 !important;
        font-size: 200%;
    }

</style>