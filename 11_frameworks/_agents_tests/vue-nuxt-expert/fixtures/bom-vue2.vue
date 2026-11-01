<template>
  <div>
    <p>Hello {{ name }}</p>
    <a :href="url">link</a>
    <form @submit.prevent="send"><input @input="changed"></form>
  </div>
</template>

<script>
export default {
  props: { color: String },
  data() {
    return { name: 'Flavio', url: '/x' }
  },
  methods: {
    send() { this.$emit('sent', this.name) }
  }
}
</script>

<style scoped>
p { color: red }
</style>
