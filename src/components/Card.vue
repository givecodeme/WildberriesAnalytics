<template>
  <b-card class="mb-3" border-variant="success" align="center">
    <b-card-text>
      <del v-if="todo.completed" class="text-danger">
        {{ todo.title }}
      </del>

      <span v-else>
        {{ todo.title }}
      </span>
    </b-card-text>

    <!-- <b-card-text 
      >{{ todo.title }}
      {{ todo.completed }}
    </b-card-text> -->

    <b-button variant="warning" @click="completeTodo()">Change</b-button>
    <b-icon variant="danger" icon="x-circle" @click="$emit('deleteTodo')" />
  </b-card>
</template>

<script>
import axios from "axios";

export default {
  props: {
    todo: Object,
  },
  methods: {
    completeTodo() {
      axios
        .put(`todos/${this.todo.id}/`, {
          title: this.todo.title,
          completed: !this.todo.completed,
        })
        .then((res) => {
          this.todo.completed = res.data.completed;
        });
    },
  },
};
</script>

<style>
</style>