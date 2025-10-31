<script setup lang="ts">

</script>

<template>
  <footer class="bg-gray-900 border-t border-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 mt-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <p class="text-gray-400">Advanced football analytics platform for fans and analysts. Dive deep into stats, compare teams, and explore global football data.</p>
        </div>
        <div>
          <h3 class="text-white font-bold text-lg mb-4">Features</h3>
          <ul class="space-y-1">
            <li><NuxtLink to="/teams" class="text-gray-400 hover:text-primary-500 transition duration-150">Team Analysis</NuxtLink></li>
            <li><NuxtLink to="/players" class="text-gray-400 hover:text-primary-500 transition duration-150">Player Stats</NuxtLink></li>
            <li><NuxtLink to="/seasons" class="text-gray-400 hover:text-primary-500 transition duration-150">Seasons Comparison</NuxtLink></li>
          </ul>
        </div>
        <div>
          <h3 class="text-white font-bold text-lg mb-4">Resources</h3>
          <ul class="space-y-2">
            <li><NuxtLink to="/documentation" class="text-gray-400 hover:text-primary-500 transition duration-150">Documentation</NuxtLink></li>
            <li><NuxtLink to="/manual" class="text-gray-400 hover:text-primary-500 transition duration-150">El Manuel</NuxtLink></li>
          </ul>
        </div>
      </div>
      <div class="mt-12 pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center">
        <p class="text-gray-400">&copy; 2025 FootyLytics. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>

</style>