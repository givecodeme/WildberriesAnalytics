<template>
  <div id="">
    <div>
      <b-navbar toggleable="lg" type="dark" variant="dark">
        <b-navbar-brand :to="{ name: 'list' }">NavBar</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item href="#">Link</b-nav-item>
            <b-nav-item href="#" disabled>Disabled</b-nav-item>
          </b-navbar-nav>
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-item-dropdown right>
              <!-- Using 'button-content' slot -->
              <template #button-content>
                <em>User</em>
              </template>
              <b-dropdown-item v-if="isLoggedIn" :to="{ name: 'profile' }"
                >Profile</b-dropdown-item
              ><b-dropdown-item v-if="isLoggedIn" @click="logout()"
                >Log Out</b-dropdown-item
              >
              <b-dropdown-item
                v-if="!isLoggedIn"
                :to="{
                  name: 'signIn',
                }"
                >Sign In</b-dropdown-item
              >

              <b-dropdown-item
                v-if="!isLoggedIn"
                :to="{
                  name: 'signUp',
                }"
                >Register</b-dropdown-item
              >
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>

    <b-container fluid id="app">
      <router-view />
    </b-container>
  </div>
</template>

<script>
// import Card from "@/components/Card.vue";

import { mapGetters, mapActions } from "vuex";

export default {
  name: "App",
  // components: { Card },
  data: () => ({
    search: "",
    todos: [],
    title: "",
    currentPage: 1,
    pages: 10,
  }),
  methods: {
    ...mapActions(["logout"]),
  },
  computed: {
    ...mapGetters(["isLoggedIn"]),
  },
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
</style>
