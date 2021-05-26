<template>
  <div class="w-50 m-auto">
    <b-form @submit.prevent="onSubmit">
      <!-- <b-form-group
        id="input-group-1"
        label="Email address:"
        label-for="input-1"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          placeholder="Enter email"
          required
        ></b-form-input>
      </b-form-group> -->

      <b-form-group id="input-group-2" label="Your Name:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.name"
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
      <b-button type="submit" variant="primary">Sign In</b-button>
    </b-form>
  </div>
</template>

<script>
// import axios from "axios";
import { mapActions } from "vuex";

export default {
  data: () => ({
    form: {
      // email: "",
      name: "",
      password: "",
    },
  }),
  methods: {
    ...mapActions(["LOGIN"]),

    onSubmit() {
      this.LOGIN(this.form);
    },

    // register() {
    //   // axios.post("auth/users/", this.form);
    //   axios
    //     .post("/token/", {
    //       username: this.form.name,
    //       password: this.form.password,
    //     })
    //     // commit('auth_success',)
    //     .then((response) =>
    //       localStorage.setItem("token", `Bearer ${response.data.access}`)
    //     );
    // },
  },
};
</script>