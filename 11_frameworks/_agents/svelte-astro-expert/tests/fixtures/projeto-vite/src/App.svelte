<script>
  import { onMount, createEventDispatcher } from 'svelte'
  import { username } from './store.js'
  export let disabled = false
  const dispatch = createEventDispatcher()
  let list = [1, 2, 3]
  let name = ''
  let myInput
  const add = () => {
    list.push(4)
    list = list
    dispatch('added', { total: list.length })
  }
  onMount(() => {
    myInput.focus()
    const interval = setInterval(() => console.log('tick'), 1000)
    return () => clearInterval(interval)
  })
</script>

<style>
  h1 { color: purple; }
</style>

<h1>Hello {$username}</h1>
<input bind:this={myInput} bind:value={name} {disabled} />
<button on:click|preventDefault={add}>+</button>
<ul>
  {#each list as item (item)}
    <li>{item}</li>
  {/each}
</ul>
{#await promise}
  <p>...</p>
{:then data}
  <p>{data}</p>
{:catch error}
  <p>error</p>
{/await}
<slot name="before" />
<slot />
