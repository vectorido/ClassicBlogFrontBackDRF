<template>
  <div>
    <h1>Это компонент - ребенок</h1>
    <input type="text" placeholder="Введите текст, который надо передать на страницу" v-model="text">
    <button @click='sendTopage()'>Передать на страницу</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      text: ''
    }
  },
  methods: {
    sendTopage() {
      this.$emit('sendTopage', this.text)
    }
  }
}
</script>

<style scoped>

</style>
