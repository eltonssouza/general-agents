<template>
  <div>
    <p>Hello {{ name; other }}</p>
    <a href="{{ url }}">link</a>
    <span v-html="userHtml"></span>
    <p>{{ name | capitalize }}</p>
    <form @submit="send"><input @change="changed"></form>
    <p>{{ $route.params.post_slug }}</p>
    <ul slot="sidebar"><li>x</li></ul>
  </div>
</template>

<script>
export default {
  props: ['color', 'size'],
  data: () => {
    return { name: 'Flavio' }
  },
  computed: {
    now: function () { return Date.now() },
    double: () => {
      return this.count * 2
    }
  },
  methods: {
    change() {
      this.color = 'red'
      this.size++
      console.log(this.data.name)
      this.$store.state.flavor = 'x'
    }
  },
  filters: { capitalize(v) { return v } }
}
router.beforeEach((to, from, next) => {
  console.log(to)
})
new Vue({ el: '#app' })
Vue.component('x-y', {})
Vue.use(VueRouter)
this.$root.$on('ev', () => {})
</script>

<style>
p { color: red }
</style>
