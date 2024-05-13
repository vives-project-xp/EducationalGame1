<script>
</script>

<template>
  <main>
    <div class="mainInfo">
    <h1>How does it work?</h1>
    <p>On this page you'll find more about the board and PC-game.</p>
    </div>
    <div class="tutorial">
    <h2>What?</h2>
    <p>In this project we aim to create an educational game that consists of 3 large parts: A pc game made with Pygame, a board game version based on the PC game and this website to integrate and provide functionality to both versions.
      On each of these platform we aim to inform our users and incorporate themes concerning climate change and the reality of its consequences depending on humanity's choices.</p><br>
      <p></p>
    </div>
    <div class="manual">
    <h2>Board game</h2>
    <p>You can find the manual for the board game <a href="https://github.com/vives-project-xp/EducationalGame1/tree/main/Board%20Game/Rules/English%20Version/Player%20Rules%20v02%20.md" target="_blank">here</a>.</p>
    <img src="/img/board.png" alt="board game">
  </div>
  <div class="tutorial2">
  <h1>PC game</h1>
  <p>During the online game the player will have to balance the size of their income, population and CO2 emmisions as well as create their own imaginary city on a gridlike structure by building and upgrading structures. The game runs until the grid is fully occupied and upgraded or until the player's CO2 emmision score goes too low at which point they lose. If 
    you want more information, you can find it <a href="https://github.com/vives-project-xp/EducationalGame1/blob/main/GameDocumentation/gameloop.md" target="_blank">here</a>.
  <img src="/img/gameplay.png" alt="gameplay">
  </p>

  </div>
  </main>
</template>

<style scoped>
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

    .tutorial {
      background-color: #f8f4f0;
      color: black;
      height: 300px;
      border-radius: 80px;
      padding: 50px;
      text-align: center;
    }

    .tutorial2 {
      background-color: #f8f4f0;
      color: black;
      height: 750px;
      border-radius: 80px;
      padding: 50px;
      text-align: center;
      margin-bottom: 50px;
    }

    h2 {
        font-size: 30px;
        margin-bottom: 30px;
        font-family: 'Public Pixel', sans-serif;
    }

    .manual {
        color: white;
        padding: 50px;
        text-align: center;
    }

    main {
        margin-top: 50px;
    }

    img {
        width: 50%;
        margin-top: 20px;
    }
</style>