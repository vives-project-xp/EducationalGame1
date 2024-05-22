<script>
  import { RouterLink, RouterView } from 'vue-router'

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

<template>
  <header>
    
  </header>
  <div class="wrapper">
      <nav class="navbar navbar-expand-lg sticky-top">
        <RouterLink to="/" class="nav-link nav-link-custom">
          Home
        </RouterLink>
        <RouterLink to="/info" class="nav-link nav-link-custom">Info</RouterLink>
        <RouterLink to="/missions" class="nav-link nav-link-custom">Missions</RouterLink>
        <RouterLink to="/about" class="nav-link nav-link-custom">About</RouterLink>
        <RouterLink to="/download" class="button">Download game</RouterLink>
      </nav>
    </div>
  <RouterView />
  <footer>
    <div class="footerMenu" >
    <p>Project made by Esteban Desmedt, Jasper Vantuyne, Olivier Westerman and Xander Vyvey in 2024 for VIVES</p>
    </div>
  </footer>
</template>

<style>
  body {
    background-color: #001a2b;
  }

  .navbar {
    color: white;
    display: flex;
    justify-content: start;
    align-items: center;
    margin: 20px;
  }

  .nav-link {
    color: white;
    margin-right: 120px;
    padding: 8px;
    border-radius: 10px;
  }

  .nav-link:hover {
    background-color: #d549a1;
    border-radius: 10px;
    text-align: center;
  }

  nav {
      display: flex;
      align-items: center;
  }

  .image {
  width: 120px;
  }

  .button {
    display: inline-block;
    text-decoration: none;
    padding: 14px 40px;
    color: #fff;
    background-image: linear-gradient(45deg, #df4881, #c430d7);
    font-size: 14px;
    border-radius: 30px;
    border-top-right-radius: 0;
    width: 200px;
    margin-left: auto;
  }

  .button:hover {
    background-image: linear-gradient(45deg, #c430d7, #df4881);
  }

  .footerMenu {
    background-color: #f8f4f0;
    color: gray;
    border-top-left-radius: 80px;
    border-top-right-radius: 80px;
    text-align: center;
    padding: 40px;
  /* position: fixed; */
    bottom: 0;
    width: 100%;
    }

</style>
