<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand :to="{ name: 'list' }">WildberriesAnalytics</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item :to="{ name: 'token' }">Token</b-nav-item>
        <b-nav-item :to="{ name: 'calculator' }">Calculator</b-nav-item>
        <!-- <b-nav-item href="#" disabled>Disabled</b-nav-item> -->
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
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  methods: mapActions(["logout"]),
  computed: mapGetters(["isLoggedIn"]),
};
</script>

<style>
</style>