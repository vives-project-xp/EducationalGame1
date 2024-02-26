//Logic section
<script>
  import Carousel from '../components/Carousel.vue'
   export default{
        components: {
            Carousel
        },
        
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
  <Carousel />
</div>
<div class="whiteBg">
  <div class="missionsInfo">
    <h1>Missions</h1>
    <p>On this site, additional missions for the board game will appear. They will unlock codes which will you make able to play the online game.</p>
  </div>
</div>
<div class="boardgameInfo">
  <h1>Board Game</h1>
  <p>There will also be a board game version. Our goal is for a grid-based puzzle game similar to existing games like Cathedral, Patchwork and My City. During the game the 2-4 players will be able to place tiles in various shapes and sizes on a grid in which they must balance the size of their population and Climate Impact. The game runs until all tiles have filled up the board or until no tiles are left at which point a winner is calculated by the points they acrued during the game. A Tutorial video on how to play and a downloadable manual will be provided on the webpage. Missions will also be available via the webpage in which the players will get to play with an altered ruleset or start with a prewritten board state to overcome these challenges.</p>
</div>
<div class="footerMenu">
  <p>Project made by Esteban Desmedt, Jasper Vantuyne, Olivier Westerman and Xander Vyvey in 2024 for VIVES</p>
</div>
</template>

// Style section
<style>
  *{
      box-sizing: border-box;
      font-family: 'Poppins', sans-serif;
  }

  .content h1 {
    font-size: 70px;
    color: white;
  }

  .content p {
    margin: 10px 0 30px;
    color: white
  }

  .whiteBg {
    background-color: #f8f4f0;
    color: black;
    height: 400px;
    border-radius: 80px;
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

  .missionsInfo {
    padding: 50px;
    text-align: center;
  }

  .missionsInfo h1{
    font-size: 50px;
    margin-bottom: 50px;
    font-family: 'Public Pixel', sans-serif;
  }

  .boardgameInfo {
    color: white;
    padding: 50px;
    text-align: center;
  }

  .boardgameInfo h1{
    font-size: 50px;
    margin-bottom: 50px;
    font-family: 'Public Pixel', sans-serif;
  }

  .footerMenu {
    background-color: #f8f4f0;
    color: gray;
    border-top-left-radius: 80px;
    border-top-right-radius: 80px;
    text-align: center;
    padding: 40px;
  }
</style>
