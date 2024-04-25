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
    <h1>Online game</h1>
    <p>This unique city builder game, made in Python, is the main part of Joxe. During the game the player has to balance the size of their income, population and CO2 emmisions as well as create their own imaginary city on a gridlike structure by building and upgrading structures. The game runs until the grid is fully occupied and upgraded or until the player's CO2 emmision score goes too low at which point they lose.</p>
  </div>
</div>
<div class="boardgameInfo">
  <h1>Board Game</h1>
  <p>There is also a board game version, an offline version of the pygame. THis is a grid-based puzzle game similar to existing games like Cathedral, Patchwork and My City. During the game the 2-4 players will be able to place tiles in various shapes and sizes on a grid in which they must balance the size of their population and Climate Impact. The game runs until all tiles have filled up the board or until no tiles are left at which point a winner is calculated by the points they acrued during the game. A Tutorial video on how to play and a downloadable manual will be provided on the webpage. Missions will also be available via the webpage in which the players will get to play with an altered ruleset or start with a prewritten board state to overcome these challenges.</p>
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
</style>
