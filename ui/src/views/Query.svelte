<script>
    import {TableSort} from 'svelte-tablesort'
    import DecodedData from "../components/DecodedData.svelte";

    export let router;
    let context = router.params.context || '16eac0d58adf480fb7f760a86e988c85';
    let error = null;


    function setContext(ctx) {
        location.href = `/query/${ctx || context}`;
    }

    function unsetContext() {
        location.href = '/query';
    }

    function modifyLine(context, line) {
        location.href = `/modify/${context}/${line}`;
    }

    function decodeData(data) {
        try {
            return atob(data);
        } catch (e) {
            return data;
        }
    }

    function autoselectLines(context) {
        app.api.autoselectLines(context).then(response => {
            location.reload();
        }).catch(e => {
            error = e;
        });
        return false
    }
</script>

<div>
    <h1>Query</h1>
    <div class="input-group mb-3">
        <input type=text class="form-control" placeholder="Context (must be 32 characters)" bind:value={context} />
        <div class="input-group-append">
            <button class="btn btn-success" type="button" on:click={() => setContext()} disabled={context.length !== 32}>Select</button>
            <button class="btn btn-warning" type="button" on:click={unsetContext}>Clear</button>
        </div>
    </div>
    {#if error !== null }
        <div class="alert alert-danger" role="alert">{error}</div>
    {/if}
    {#if router.params.context !== undefined }
        {#await app.api.getSummary(router.params.context)}
            Loading...
        {:then data}
            <h2>{router.params.context}</h2>
            {#if data.missing.length > 0 }
                <h3>Missing lines (afaik):</h3>
                <button class="btn btn-warning" type="button" on:click={(e) => {e.preventDefault();autoselectLines(router.params.context);}}>Automatically assign lines</button>
                <ul>
                {#each data.missing as i}
                    <li><a href="/modify/{router.params.context}/{i}" on:click={() => modifyLine(router.params.context, i)}>{i}</a></li>
                {/each}
                </ul>
            {:else}
                <button class="btn btn-warning" type="button" on:click={(e) => {e.preventDefault();autoselectLines(router.params.context);}}>Automatically assign lines</button>
            {/if}
            <h3>Assigned data so far:</h3>
            <TableSort items={Object.values(data.lines)} class="table table-striped">
                <tr slot="thead">
                    <th scope="col">Source</th>
                    <th scope="col">IPv6</th>
                    <th scope="col" data-sort="received_at">Received At</th>
                    <th scope="col" data-sort="line">Line</th>
                    <th scope="col">Data (gray mean not decodable)</th>
                </tr>
                <tr slot="tbody" let:item={item}>
                        <td scope="row">{item.source}</td>
                        <td class="marker">
                            {#if item.v6}<span class="text-success">&check;</span>{:else}<span class="text-danger">&times;</span>{/if}
                        </td>
                        <td>{item.received_at}</td>
                        <td><a href="/modify/{router.params.context}/{item.line}" on:click={() => modifyLine(router.params.context, item.line)}>{item.line}</a></td>
                        <td><DecodedData data={item.data}></DecodedData></td>
                </tr>
            </TableSort>
        {:catch error}
            <div class="alert alert-danger" role="alert">{error}</div>
        {/await}
    {:else}
        {#await app.api.listContexts()}
            Loading...
        {:then data}
            <table class="table table-striped">
                <thead>
                <tr>
                    <th scope="col">Context</th>
                    <th scope="col"># entries</th>
                    <th scope="col"># lines</th>
                </tr>
                </thead>
                <tbody>
                {#each data as { context, entries, lines }, i}
                    <tr>
                        <td scope="row"><a href="/query/{context}" on:click={() => setContext(context)}>{context}</a></td>
                        <td>{entries}</td>
                        <td>{lines}</td>
                    </tr>
                {/each}
                </tbody>
            </table>
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