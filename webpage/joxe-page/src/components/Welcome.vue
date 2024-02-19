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
  <h1>Welcome!</h1>
  <p>JOXE is an upcoming game, online and offline. On this site you'll find
    more about the board game and additional missions to unlock the online game for free!
  </p>
  <p>Carousel showing online game trivia here?</p>
</div>
</template>

// Style section
<style>
  *{
      box-sizing: border-box;
      font-family: 'Poppins', sans-serif;
  }

  .content {
    margin-top: 50px;
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
