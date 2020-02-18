<script>
    export let data;

    let decoded = null;
    try {
        decoded = atob(data);
    } catch (e) {
        // Do nothing
    }
</script>

{#if decoded === null }
    <span class="text-muted">{data}</span>
{:else}
    <span>{decoded}</span>
{/if}