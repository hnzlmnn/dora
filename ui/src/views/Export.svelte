<script>
    import { onMount, onDestroy } from 'svelte';

    export let router;
    let error = null;
    let editor;
    let loading = true;
    function mountEditor(data) {
        editor = CodeMirror(document.getElementById('codemirror-container'), {
            value: data,
            // mode:  "javascript"
            lineNumbers: true,
            lineWrapping: false,
            readOnly: true,
        })
    }
    onDestroy(() => {
        if (editor) {
            editor.dispose();
            const model = editor.getModel();
            if (model) model.dispose();
        }
    });
    onMount(async () => {
        if (router.params.context === undefined) return;
		app.api.exportEntry(router.params.context).then(data => {
		    mountEditor(data);
        }).catch(e => { error = e }).then(() => { loading = false });
	});

    function toggleWordWrap() {
        if (!editor) return;
        console.log(editor, editor.options.lineWrapping);
        editor.setOption("lineWrapping", !editor.options.lineWrapping);
    }
</script>

<div class="d-flex flex-column flex-grow-1">
    <h1>Export</h1>
    {#if router.params.context === undefined }
        <div class="alert alert-warning" role="alert">No context selected! Go to <a href="/query">Query</a> and select a context to export.</div>
    {:else}
        {#if loading }
            Loading...
        {:else}
            {#if error !== null }
                <div class="alert alert-danger" role="alert">{error}</div>
            {:else}
                Loaded
            {/if}
        {/if}
        <div class="btn-toolbar" role="toolbar">
            <div class="btn-group mr-2" role="group">
                <button type="button" class="btn btn-secondary" on:click={toggleWordWrap}>Line wrap</button>
                <button type="button" class="btn btn-secondary">2</button>
                <button type="button" class="btn btn-secondary">3</button>
                <button type="button" class="btn btn-secondary">4</button>
            </div>
            <div class="btn-group mr-2" role="group" aria-label="Second group">
                <button type="button" class="btn btn-secondary">5</button>
                <button type="button" class="btn btn-secondary">6</button>
                <button type="button" class="btn btn-secondary">7</button>
            </div>
            <div class="btn-group" role="group" aria-label="Third group">
                <button type="button" class="btn btn-secondary">8</button>
            </div>
        </div>
        <div id="codemirror-container" class="flex-grow-1"></div>
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

    #codemirror-container {
        width: 100%;
    }

    :global(.CodeMirror) {
        height: 100% !important;
        text-align: left;
    }

    :global(.CodeMirror .CodeMirror-line) {
        /*white-space: pre !important;*/
    }
</style>