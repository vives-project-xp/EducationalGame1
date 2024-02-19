//Logic section
<script>
   export default{
        data(){
            return{
                image: 'img/JOXEC-noBG.png',
                image2: 'img/gameplay.png',
                image3: 'img/underconstruction.jpg'
            }
        } 
    }
</script>

// Template section
<template>
  <div class="content">
  <h1 class="animation">A new upcoming game</h1>
  <p class="animation">This site is still under construction, please come back soon!</p>
  <!-- <img :src="image2" alt="gameplay" class="animationImage"> -->
  <img :src="image3" alt="gameplay" class="animationImage">
</div>
</template>

// Style section
<style>
  *{
      box-sizing: border-box;
      font-family: 'Poppins', sans-serif;
  }

  .content {
    margin-top: 2%;
    max-width: 1000px;
  }

  .content h1 {
    font-size: 70px;
    color: white;
  }

  .content p {
    margin: 10px 0 30px;
    color: white
  }

  .animation, .animationImage {
    opacity: 0;
    transform: translateY(30px);
    animation: moveup 0.5s linear forwards;
  }

  @keyframes moveup {
    100% {
      opacity: 1;
      transform: translateY(0px);
    }
  }

  .animationImage {
    width: 400px;
    position: relative;
    bottom: 0;
  }
</style>
