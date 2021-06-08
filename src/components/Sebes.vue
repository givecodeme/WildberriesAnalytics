<template>
  <div>
    <b-input class="w-25 m-auto" v-model="sebes" @change="updateSebes()" />
  </div>
</template>

<script>
import axios from "axios";
import { api } from "@/services/api";
export default {
  props: ["prod_id", "prop_sebes"],
  data() {
    return {
      sebes: +this.prop_sebes || 0,
    };
  },

  methods: {
    updateSebes() {
      // axios.defaults.headers.common["Authorization"] =
      //   localStorage.getItem("token");

      axios
        .patch(`products/${this.prod_id}/`, {
          sebes: Number(this.sebes),
        })
        .then(() => console.log("success"));
    },
  },
};
</script>

<style>
</style>