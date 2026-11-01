<script>
  export let count = 0
  export function helper() {}
  const name = ''
  const $ref = null
  let list = [1, 2]
  const store = readable(0)
  const add = () => {
    list.push(3)
    count++
    store.set(4)
  }
  onMount(async () => {
    setInterval(() => {}, 1000)
  })
  const send = () => dispatch('x')
</script>

<input bind:value={name} />
<form on:submit={add}>
  <button onclick={add}>ok</button>
</form>
<p>{$missing}</p>
{#each list as item}
  <li>{item}</li>
{/each}
{#await promise}
  <p>...</p>
{:then data}
  <p>{data}</p>
{/await}
<slot />
<slot />
