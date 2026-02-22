<script setup lang="ts">

</script>

<template>
  <footer class="footer">
    <div class="footer-layout">
      <div class="div-1">
        <p>Advanced football analytics platform for fans and analysts. Dive deep into stats, compare teams, and explore global football data.</p>
      </div>
      <div class="footer-links">
        <div>
          <h3 class="h3-footer">Features</h3>
          <ul class="padding-fix">
            <li class="footer-link"><NuxtLink to="/seasons">Seasons Comparison</NuxtLink></li>
            <li class="footer-link"><NuxtLink to="/teams">Team Analysis</NuxtLink></li>
            <li class="footer-link"><NuxtLink to="/players">Player Stats</NuxtLink></li>
          </ul>
        </div>
        <div>
          <h3 class="h3-footer">Resources</h3>
          <ul class="padding-fix">
            <li ><NuxtLink to="/documentation">Documentation</NuxtLink></li>
            <li ><NuxtLink to="/manual">El Manuel</NuxtLink></li>
          </ul>
        </div>
      </div>
    <div>
      <p>&copy; 2025 FootyLytics. All rights reserved.</p>
    </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  display: flex;
  margin-top: auto;
  padding: 0; 
  background-color: rgba(22, 29, 39, 0.7);  
  color: #e5e7eb;  
  text-align: center;
  border-top: 1px solid #374151;
}
.footer-layout {
  max-width: 80rem;
  margin-left: auto;
  margin-right: auto;
}
.footer-links {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}
@media (max-width: 280px) {
  .footer-links {
    flex-direction: column;
    gap: 0.1rem;
  }
}
ul {
  margin: 0;
}

footer ul.padding-fix li, footer ul.padding-fix li a, footer ul.padding-fix li .nuxt-link {
  list-style: none;
  margin: 0.2rem 0.3rem;
  font-size: 0.8rem;
  transition: color 0.2s;
  color: #d1d5db;
  text-decoration: none;
}
footer ul.padding-fix li a:hover, footer ul.padding-fix li .nuxt-link:hover {
  color: #ffc7c7;
}
p{
  font-size: 0.9rem;
  margin: 0.4rem;
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

.h3-footer {
  font-weight: 800;
  font-size: 25px;
  color: rgb(118, 76, 172);
  letter-spacing: 2px;
  margin: 0;
}

.padding-fix {
  padding-left: 0;
  padding-right: 0;
}
</style>