<script setup>

import { onMounted, ref } from 'vue';
import { api } from '../main';

const posts = ref([])

const fetchPosts = () => {
  api.get("http://localhost:8000/api/posts")
  .then(({data}) => {
    posts.value = data
  })
  .catch((err) => {
    alert(err.response?.data.detail ?? "Erreur sans réponse")
  })
}

onMounted(fetchPosts)

</script>

<template>
  <div class="main-container">
    <template v-if="posts.length">
      <section v-for="post in posts">
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
      </section>
    </template>
    <p v-else>Aucun posts disponible</p>
  </div>
</template>