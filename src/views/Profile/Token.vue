<template>
  <b-form @submit.prevent="createToken">
    <b-form-input @change="updateToken" v-model="token.apiKey" type="text" />
    <b-form-text>Input API token </b-form-text>
    <b-btn type="subnit">Добавить</b-btn>
  </b-form>
</template>

<script>
import api from "@/services/api";
import axios from "axios";
export default {
  data: () => ({
    token: {
      id: "",
      apiKey: "",
    },
  }),
  methods: {
    createToken() {
      axios.defaults.xsrfHeaderName = "X-CSRFToken";
      axios.defaults.xsrfCookieName = "csrftoken";

      // axios.defaults.headers.common["Authorization"] = localStorage.getItem(
      //   "token"
      // );

      // axios.get("auth/users/me/", {
      //   headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      // });
      // .then((res) => (this.user = res.data));
      if (!this.token.id) {
        axios.post(
          "tokens/",
          {
            apiKey: this.token.apiKey,
          },
          {
            headers: {
              Authorization: localStorage.getItem("token"),
            },
          }
        );
      }
    },
    updateToken() {
      axios.defaults.xsrfHeaderName = "X-CSRFToken";
      axios.defaults.xsrfCookieName = "csrftoken";

      axios.patch(`tokens/${this.token.id}/`, {
        apiKey: this.token.apiKey,
      });
    },
  },

  mounted() {
    axios
      .get("tokens/", {
        headers: {
          Authorization: localStorage.getItem("token"),
        },
      })
      .then((res) => {
        if (res.data.id) this.token = res.data;
      });
  },
};
</script>

<style>
</style>