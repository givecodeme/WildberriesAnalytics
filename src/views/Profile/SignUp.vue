<template>
  <div class="w-50 m-auto">
    <b-form @submit.prevent="register">
      <b-form-group id="input-group-2" label="Your Name:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.username"
          placeholder="Enter name"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-2"
        label="Your Password:"
        label-for="input-2"
      >
        <b-form-input
          type="password"
          id="input-2"
          v-model="form.password"
          placeholder="Enter password"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-4" v-slot="{ ariaDescribedby }">
        <b-form-checkbox-group
          v-model="form.checked"
          id="checkboxes-4"
          :aria-describedby="ariaDescribedby"
        >
        </b-form-checkbox-group>
      </b-form-group>

      <b-button type="submit" variant="primary">Register</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    form: {
      // email: "",
      username: "",
      password: "",
    },
  }),
  methods: {
    register() {
      axios.post("auth/users/", this.form);
    },
  },
};
</script>