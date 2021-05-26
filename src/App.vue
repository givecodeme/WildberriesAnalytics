<template>
  <div id="app">
    <b-container class="w-50">
      <img alt="Vue logo" src="./assets/logo.png" />

      <b-form-input
        class="shadow-success"
        v-model="search"
        placeholder="Search"
        @input="searchSubmit"
      />

      <b-button v-b-modal.modal-1 variant="primary" class="my-3"
        >Create ToDo</b-button
      >

      <b-modal id="modal-1" title="Create ToDo">
        <b-form @submit.prevent="createTodo">
          <b-form-input placeholder="Title" v-model="title" />
          <b-button type="submit">Create</b-button>
        </b-form>
      </b-modal>

      <h2 v-if="!todos.length">Not Found</h2>

      <div v-else>
        <card
          :todo="todo"
          v-for="(todo, index) in todos"
          :key="todo.id"
          @deleteTodo="deleteTodo(todo.id, index)"
        />

        <!-- page-class="page" -->
        <b-pagination
          v-if="pages > 1"
          pills
          last-number
          v-model="currentPage"
          :total-rows="pages"
          :per-page="1"
          align="center"
          @change="changePage"
        />
      </div>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import Card from "@/components/Card.vue";

// axios.defaults.baseURL = "http://127.0.0.1:8000/";

export default {
  name: "App",
  components: { Card },
  data: () => ({
    search: "",
    todos: [],
    title: "",
    currentPage: 1,
    pages: 10,
  }),
  methods: {
    searchSubmit() {
      axios
        .get("todos/", {
          params: {
            search: this.search,
          },
        })
        .then((res) => {
          this.currentPage = 1;
          this.todos = res.data.results;
          this.pages = res.data.pages;
        });
    },

    createTodo() {
      axios
        .post("todos/", {
          title: this.title,
        })
        .then((res) => {
          if (this.todos.length == 3) {
            this.todos.splice(-1, 1);
          }
          this.todos.unshift(res.data);
          this.$bvModal.hide("modal-1");
          this.title = "";
        });
    },
    deleteTodo(id, index) {
      axios.delete(`todos/${id}/`).then(() => {
        this.todos.splice(index, 1);
      });
    },
    changePage(newPage) {
      axios
        .get("todos/", {
          params: {
            page: newPage,
            search: this.search,
          },
        })
        .then((res) => {
          this.todos = res.data.results;
        });
    },
  },
  mounted() {
    axios.get("todos/").then((res) => {
      this.todos = res.data.results;
      this.pages = res.data.pages;
    });
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
