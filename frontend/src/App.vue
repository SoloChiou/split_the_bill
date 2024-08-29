<template>
  <div id="app">
    <div class="logo">
      <img
        src="./assets/img/photo_ID.png"
        :style="{ width: '80px', display: 'block', margin: '0 auto' }"
      />
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif, "微軟正黑體";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
  /* border: 1px solid #000; */
}

h1 {
  font-size: 24px;
  color: #333;
}

.router-link {
  text-decoration: none;
  color: #71acdc;
  font-weight: bold;
}
</style>
