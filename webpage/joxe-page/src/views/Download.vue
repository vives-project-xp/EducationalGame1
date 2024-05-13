<script>
export default {
  methods: {
    downloadGame() {
      window.location.href = '../resources/exe.win-amd64-3.12.zip';
    }
  }
}
</script>

<template>
  <main>
    <div class="mainInfo">
    <button @click="downloadGame" class="button">Click here to download the game</button>
    <p>Now the game is on your computer! If you go to the downloads folder on your computer, right click the zip folder and click on unzip. <br>In the unzipped folder you will see a file name called 'main.exe'. Click on it and after a few moments, you're able to play!
    </p>
    <img src="/img/gameplay2.png" alt="gameplay screenshot">
    <br><br><br>
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
    width: 20%;
    margin-left: auto;
    margin-bottom: 20px;
    
  }

  .button:hover {
    background-image: linear-gradient(45deg, #c430d7, #df4881);
    
  }
  .mainInfo {
      color: white;
      margin-left: 20px;
      margin-bottom: 40px;
      text-align: center;
  }

  h1 {
      font-size: 50px;
      margin-bottom: 30px;
      font-family: 'Public Pixel', sans-serif;
  }


</style>