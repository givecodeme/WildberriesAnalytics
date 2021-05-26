<template>
  <b-form @submit.prevent="createToken">
    <b-form-input v-model="token" type="text" />
    <b-form-text>Input API token </b-form-text>
    <br />
    {{ token }}
    <b-btn type="subnit">Send</b-btn>
  </b-form>
</template>

<script>
import api from "@/services/api";
import axios from "axios";
export default {
  data: () => ({
    token: "",
  }),
  methods: {
    createToken() {
      axios.defaults.headers.common["Authorization"] = localStorage.getItem(
        "token"
      );

      axios.get("auth/users/me/", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      // .then((res) => (this.user = res.data));

      // axios.post(
      //   "tokens/",
      //   {
      //     apiKey: this.token,
      //   },
      //   {
      //     Headers: {
      //       Authorization: localStorage.getItem("token"),
      //     },
      //   }
      // );
    },
  },
};
</script>

<style>
</style>