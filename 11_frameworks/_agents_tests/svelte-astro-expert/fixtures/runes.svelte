<script>
  let count = $state(0)
  let { title } = $props()
  let double = $derived(count * 2)
</script>
<button onclick={() => count++}>{title} {double}</button>
