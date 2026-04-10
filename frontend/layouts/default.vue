<template>
  <div class="main-wrapper">
    <Header>
    </Header>
    <main class="content container">
      <NuxtPage />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Header from '~/components/header.vue'
import Footer from '~/components/footer.vue'
</script>
