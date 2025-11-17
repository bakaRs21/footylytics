<script setup lang="ts">

</script>

<template>
  <footer class="footer">
    <div class="footer-layout">
      <div class="div-1">
        <p>Advanced football analytics platform for fans and analysts. Dive deep into stats, compare teams, and explore global football data.</p>
      </div>
        <div>
          <h3>Features</h3>
          <ul class="padding-fix">
            <li class="footer-link"><NuxtLink to="/seasons">Seasons Comparison</NuxtLink></li>
            <li class="footer-link"><NuxtLink to="/teams">Team Analysis</NuxtLink></li>
            <li class="footer-link"><NuxtLink to="/players">Player Stats</NuxtLink></li>
          </ul>
        </div>
        <div>
          <h3>Resources</h3>
          <ul class="padding-fix">
            <li ><NuxtLink to="/documentation">Documentation</NuxtLink></li>
            <li ><NuxtLink to="/manual">El Manuel</NuxtLink></li>
            <li ><NuxtLink to="/about">About</NuxtLink></li>
          </ul>
        </div>
    <div class="div-2">
      <p>&copy; 2025 FootyLytics. All rights reserved.</p>
    </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: auto;
  padding: 8px 4px; 
  background-color: rgba(22, 29, 39, 0.7);  
  color: #e5e7eb;  
  text-align: center;
  border-top: 1px solid #374151;
}
.footer-layout {
  max-width: 80rem;
  margin-left: auto;
  margin-right: auto;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-column-gap: 0px;
  grid-row-gap: 0px;
}
.div-1 { grid-area: 1 / 1 / 2 / 3; }
.div-2 { grid-area: 3 / 1 / 4 / 3; }

  

@media (min-width: 640px) {
  .sm\:px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
}
@media (min-width: 1024px) {
  .lg\:px-8 { padding-left: 2rem; padding-right: 2rem; }
}

footer ul.padding-fix li, footer ul.padding-fix li a, footer ul.padding-fix li .nuxt-link {
  list-style: none;
  margin: 0 0.5rem;
  font-size: 1rem;
  transition: color 0.2s;
  color: #d1d5db;
  text-decoration: none;
}
footer ul.padding-fix li a:hover, footer ul.padding-fix li .nuxt-link:hover {
  color: #ffc7c7;
}
/* icons */

.footer-icons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 1rem;
}
.footer-icon {
  width: 2rem;
  height: 2rem;
  color: #9ca3af;
  transition: color 0.2s;
}
.footer-icon:hover {
  color: #fff;
}

h3 {
  font-weight: 800;
  font-size: 30px;
  color: rgb(118, 76, 172);
  letter-spacing: 2px;
  margin: 0;
}
.padding-fix {
  padding-left: 0;
  padding-right: 0;
}
</style>