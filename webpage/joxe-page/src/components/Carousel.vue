<script>
export default {
  data() {
    return {
      currentIndex: 0,
      items: [],
    };
  },
  mounted() {
    this.items = this.$el.querySelectorAll('.carousel-item');
    this.showItem(this.currentIndex);
    setInterval(this.next, 10000); 
  },
  methods: {
    showItem(index) {
      this.items.forEach((item, i) => {
        if (i === index) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });
    },
    next() {
      this.currentIndex = (this.currentIndex + 1) % this.items.length;
      this.showItem(this.currentIndex);
    },
    prev() {
      this.currentIndex = (this.currentIndex - 1 + this.items.length) % this.items.length;
      this.showItem(this.currentIndex);
    },
  },
};
</script>

<style>
  .carousel {
    height: 600px;
    overflow: hidden;
    text-align: center;
    margin-left: 20px;
    margin-right: 20px;
  }

  .carousel-content {
  display: flex;
  align-items: center;
  }

  .carousel-content img {
    flex: 1;
    max-width: 50%; /* Adjust this value as needed */
  }

  .carousel-text {
    flex: 1;
    padding-left: 20px; /* Adjust this value as needed */
  }
  
  .carousel-item {
    min-width: 100%;
    overflow: hidden;
    position: relative;
    animation: slideInOut 10s infinite;
  }

  .carousel-item img {
    max-width: 500px;
  }

  .carousel h1 {
    font-size: 20px;
    font-family: 'Public Pixel', sans-serif;
  }

  @keyframes slideInOut {
    0% {
      transform: translateX(100%);
    }
    20% {
      transform: translateX(0);
    }
    80% {
      transform: translateX(0);
    }
    100% {
      transform: translateX(-100%);
    }
  }
</style>

<template>
  <main>
    <div class="carousel">
      <div class="carousel-item">
        <div class="carousel-content">
        <img src="../../img/JOXEC-noBG.png" alt="logo ">
        <div class="carousel-text">
          <h1>Welcome!</h1>
          <p>JOXE is a brand new game, online and offline. On this site you'll find
          more about the board game and the upcoming additional missions to unlock the online game for free!
          </p>
        </div>
      </div>
      </div>
        <div class="carousel-item">
          <div class="carousel-content">
          <img src="../../img/windmillv2.png" alt="windmill asset">
          <div class="carousel-text">
          <h1>Assets</h1>
          <p>A lot of assets like windmills are available to build.</p>
        </div>
      </div>
        </div>
        <div class="carousel-item">
          <div class="carousel-content">
          <img src="../../img/gameplay.png" alt="gameplay">
          <div class="carousel-text">
          <h1>Shop</h1>
          <p>Build houses and more to get a higher score and make the people in your city happier.</p>
        </div>
      </div>
      </div>
</div>
  </main>
</template>
