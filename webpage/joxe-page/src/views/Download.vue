<script>
export default {
  methods: {
    downloadGame() {
      window.location.href = '../resources/exe.win-amd64-3.12';
    }
  }
}
</script>

<template>
  <main>
    <div class="mainInfo">
    <button @click="downloadGame">Click here to download the game</button>
    </div>
  </main>
</template>

<style scoped>
  .mainInfo {
      color: white;
      margin-left: 20px;
      margin-bottom: 40px;
  }

  h1 {
      font-size: 50px;
      margin-bottom: 30px;
      font-family: 'Public Pixel', sans-serif;
  }
</style>