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
    setInterval(this.next, 3000); // Change slide every 3 seconds
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
    width: 100%;
    overflow: hidden;
    position: relative;
  }
  
  .carousel-inner {
    display: flex;
    transition: transform 0.5s ease;
  }
  
  .carousel-item {
    min-width: 100%;
    overflow: hidden;
  }
</style>

<template>
  <main>
    <div class="carousel">
  <div class="carousel-inner">
    <div class="carousel-item">
        <p>There are many assets in the game, like the windmill.</p>
      <img src="../../img/windmillv2.png" alt="windmill asset">
    </div>
    <div class="carousel-item">
        <p>text 2</p>
      <!-- <img src="image2.jpg" alt="Image 2"> -->
    </div>
    <div class="carousel-item">
        <p>text 3</p>
      <!-- <img src="image3.jpg" alt="Image 3"> -->
    </div>
  </div>
</div>
  </main>
</template>
