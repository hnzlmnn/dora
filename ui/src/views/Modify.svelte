<script>
    import {TableSort} from 'svelte-tablesort'
    import DecodedData from "../components/DecodedData.svelte";

    export let router;
    let error = null;

    function setLine(entry) {
        app.api.setLine(entry.context, entry.line, entry.id).then(response => {
            location.href = `/query/${entry.context}`;
        }).catch(e => {
            error = e;
        });
        return false
    }
</script>

<div>
    <h1>Modify</h1>
    {#if error !== null }
        <div class="alert alert-danger" role="alert">{error}</div>
    {/if}
    {#if router.params.context === undefined }
        <div class="alert alert-warning" role="alert">No context selected! Go to <a href="/query">Query</a> and select a context to edit.</div>
    {:else}
        {#if router.params.line === undefined }
            <div class="alert alert-warning" role="alert">No line selected! Go to <a href="/query">Query</a> and select a context and line to edit.</div>
        {:else}
            {#await app.api.getEntriesForLine(router.params.context, router.params.line)}
                Loading...
            {:then data}
                <h2>{router.params.context}</h2>
                <h3>Select entry for line {router.params.line}:</h3>
                <TableSort items={data} class="table table-striped">
                    <tr slot="thead">
                        <th scope="col">#</th>
                        <th scope="col">Source</th>
                        <th scope="col" data-sort="v6">IPv6</th>
                        <th scope="col" data-sort="received_at">Received At</th>
                        <th scope="col">Data (gray mean not decodable)</th>
                    </tr>
                    <tr slot="tbody" let:item={item}>
                            <td scope="row"><a href="/modify/{router.params.context}/{router.params.line}" on:click={(e) => {e.preventDefault();setLine(item);}}>{item.id}</a></td>
                            <td scope="row">{item.source}</td>
                            <td class="marker">
                                {#if item.v6}<span class="text-success">&check;</span>{:else}<span class="text-danger">&times;</span>{/if}
                            </td>
                            <td>{item.received_at}</td>
                            <td><DecodedData data={item.data}></DecodedData></td>
                    </tr>
                </TableSort>
            {:catch error}
                <div class="alert alert-danger" role="alert">{error}</div>
            {/await}
        {/if}
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