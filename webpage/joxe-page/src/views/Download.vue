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
    <button @click="downloadGame" class="button">Click here to download the game</button>
    </div>
  </main>
</template>

<style scoped>

.button {
    text-decoration: none;
    padding: 14px 40px;
    color: #fff;
    display: block;
    margin: 0 auto;
    background-image: linear-gradient(45deg, #df4881, #c430d7);
    font-size: 14px;
    border-radius: 30px;
    width: 200px;
    margin-left: auto;
  }

  .button:hover {
    background-image: linear-gradient(45deg, #c430d7, #df4881);
  }
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