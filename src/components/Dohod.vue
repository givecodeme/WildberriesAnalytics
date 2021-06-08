<template>
  <div class="">
    {{ res | format }} р.

    <br />
    {{ sebes }}
  </div>
</template>

<script>
export default {
  props: ["sales", "tax", "sebes"],
  filters: {
    format: (val) => `${val}`.replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 "),
  },
  data() {
    return {};
  },
  computed: {
    res() {
      return (this.sales - this.tax - this.sales * 0.06 - this.sebes).toFixed(
        0
      );
    },
  },
};
</script>

<style>
</style>