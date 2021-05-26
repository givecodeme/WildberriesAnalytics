<template>
  <div class="">
    <b-input class="w-25 m-auto" v-model="sebes" @change="updateSebes()" />
    {{ sebes }}
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: ["prod_id"],
  data: () => ({
    sebes: 0,
  }),

  methods: {
    updateSebes() {
      axios
        .post(`products/${prod_id}/`, {
          sebes: this.sebes,
        })
        .then(() => console.log("success"));
    },
  },
};
</script>

<style>
</style>