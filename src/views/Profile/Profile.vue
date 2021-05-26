<template>
  <div class="">
    <b-row>
      <b-col>
        <b-list-group>
          <b-list-group-item
            v-for="url in urls"
            :to="{ name: url.path_name }"
            :key="url.path_name"
            >{{ url.name }}</b-list-group-item
          >
        </b-list-group>
      </b-col>
      <b-col>
        <router-view />
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  data: () => ({
    urls: [
      { name: "Token", path_name: "token" },
      //  {   name:}
    ],
  }),
};
</script>

<style>
</style>