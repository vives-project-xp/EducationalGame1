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
    <div class="navbar">
  <nav>
    <img :src="image" alt="Joxe logo" class="image">
    <ul>
      <li><a href="#">Features</a></li>
      <li><a href="#">How it works</a></li>
      <li><a href="#">Contact</a></li>
    </ul>
    <div>
    <a href="#" class="button">Download Game</a>
  </div>
  </nav>
  <div class="content">
  <h1 class="animation">A new upcoming game</h1>
  <p class="animation">This site is still under construction, please come back soon!</p>
  <!-- <img :src="image2" alt="gameplay" class="animationImage"> -->
  <img :src="image3" alt="gameplay" class="animationImage">
</div>
</div>
</template>

// Style section
<style>
    *{
        box-sizing: border-box;
        font-family: 'Poppins', sans-serif;
    }

    .navbar {
        justify-content: space-between;
        display: flex;
        align-items: center;
        }

    nav {
        display: flex;
        align-items: center;
        }

        .image {
        width: 140px;
        }

        ul {
  list-style-type: none;
  display: flex;
}

ul li {
    width: 150px;
  padding: 0 25px;
}

ul li a {
  font-size: 16px;
  color: #fff;
  text-decoration: none;
  padding: 8px 0;
  display: block;
}

ul li a:hover {
  color: #000;
  background-color: #fff;
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
}

.button:hover {
  background-image: linear-gradient(45deg, #c430d7, #df4881);
}

.content {
  margin-top: 10%;
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
