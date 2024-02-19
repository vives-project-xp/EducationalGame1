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
          <img :src="image" alt="logo" class="image">
        </RouterLink>
        <RouterLink to="/info" class="nav-link nav-link-custom">Info</RouterLink>
        <RouterLink to="/missions" class="nav-link nav-link-custom">Missions</RouterLink>
        <RouterLink to="/about" class="nav-link nav-link-custom">About</RouterLink>
        <RouterLink to="/download" class="button">Download € 25,99</RouterLink>
      </nav>
    </div>
  <RouterView />
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
  }

  .nav-link {
    color: white;
    margin-right: 120px;
    padding: 8px;
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
</style>
