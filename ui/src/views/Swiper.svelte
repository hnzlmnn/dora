<script>
    let error = null;
    let context;
    let command;
    let tool;
    let payload;

    function copy() {
        const copyText = document.querySelector("#swiper-result");
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");
    }

    function generateContext() {
        app.api.generateContext(command, tool).then(c => {
            context = c;
        }).catch(e => {
            error = e;
        });
    }

    function generate() {
        app.api.generatePayload(context, tool, command).then(p => {
            payload = p;
        }).catch(e => {
            error = e;
        });
    }
</script>

<div>
    <h1>Swiper</h1>
    {#if error !== null }
        <div class="alert alert-danger" role="alert">{error}</div>
    {/if}
    <div class="form-group">
        <label for="swiper-generate-context">Context</label>
        <div class="input-group mt-3">
            <input type="text" class="form-control" id="swiper-generate-context" bind:value={context} />
            <div class="input-group-append">
                <button class="btn btn-outline-success" type="button" on:click={generateContext}>Generate</button>
            </div>
        </div>
        <small class="form-text text-muted">Enter the context or generate.</small>
    </div>
    <div class="form-group">
        <label for="swiper-generate-command">Command</label>
        <input type="text" class="form-control" id="swiper-generate-command" bind:value={command} />
        <small class="form-text text-muted">Enter the command that should be executed.</small>
    </div>
    <div class="form-group">
        <label for="swiper-generate-tool">Tool</label>
        <select class="form-control" id="swiper-generate-tool" bind:value={tool}>
          <option value="dig">Dig</option>
          <option value="drill">Drill</option>
          <option value="nslookup">Nslookup</option>
        </select>
        <small class="form-text text-muted">Select the tool to be used for extraction.</small>
    </div>
    <button type="submit" class="btn btn-primary mt-2" on:click={generate}>Generate</button>
    <div class="input-group mt-3">
      <input type="text" class="form-control" readonly value={payload} id="swiper-result">
      <div class="input-group-append">
        <button class="btn btn-outline-success" type="button" on:click={copy}>Copy</button>
      </div>
    </div>
</div>