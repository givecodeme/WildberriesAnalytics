<template>
  <div id="">
    <nav-bar />

    <b-container fluid id="app">
      <router-view />
    </b-container>
  </div>
</template>

<script>
// import Card from "@/components/Card.vue";

import NavBar from "./components/NavBar.vue";

export default {
  components: { NavBar },
  name: "App",
  data: () => ({}),
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.shadow-success:focus {
  box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
}

.page-item.active .page-link {
  background-color: #28a745;
  border-color: #28a745;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  /* display: none; <- Crashes Chrome on hover */
  -webkit-appearance: none;
  margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
}
</style>

