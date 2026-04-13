<template>
  <div class="main-wrapper">
    <Header>
    </Header>
    <main class="content container">
      <slot />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Header from '~/components/header.vue'
import Footer from '~/components/footer.vue'
</script>
