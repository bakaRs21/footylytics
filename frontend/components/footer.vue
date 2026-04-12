<script setup>
const localePath = useLocalePath()
</script>

<template>
  <footer class="footer">
    <div class="footer-layout">
      <div class="div-1">
        <p>{{ $t('components.footer.description') }}</p>
      </div>
      <div class="footer-links">
        <div>
          <h3 class="h3-footer">{{ $t('components.footer.features') }}</h3>
          <ul class="padding-fix">
            <li class="footer-link"><NuxtLink :to="localePath('/seasons')">{{ $t('components.footer.seasonsComparison') }}</NuxtLink></li>
            <li class="footer-link"><NuxtLink :to="localePath('/teams')">{{ $t('components.footer.teamAnalysis') }}</NuxtLink></li>
            <li class="footer-link"><NuxtLink :to="localePath('/players')">{{ $t('components.footer.playerStats') }}</NuxtLink></li>
          </ul>
        </div>
        <div>
          <h3 class="h3-footer">{{ $t('components.footer.resources') }}</h3>
          <ul class="padding-fix">
            <li ><NuxtLink :to="localePath('/documentation')">{{ $t('components.footer.documentation') }}</NuxtLink></li>
            <li ><NuxtLink :to="localePath('/manual')">{{ $t('components.footer.manual') }}</NuxtLink></li>
          </ul>
        </div>
      </div>
    <div>
      <p>{{ $t('components.footer.copyright') }}</p>
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