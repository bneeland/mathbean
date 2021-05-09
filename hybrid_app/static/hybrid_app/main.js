const app = Vue.createApp({
  data() {
    return {
      blocks: null
    }
  },
  mounted() {
    axios
      .get('../api/block-list/' + {{ pk }})
      .then(response => {
        this.blocks = response.data
      })
  }
})

app.component('block-item', {
  delimiters: ["[[", "]]"],
  props: ['block'],
  template: '<p>[[ block.type ]]</p>'
})

app.mount('#app')
