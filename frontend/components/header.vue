<script setup>
import { ref } from 'vue'
import { Icon } from '@iconify/vue';

const route = useRoute()
const localePath = useLocalePath()
const menuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}
</script>
<template>
    <header>
        <nav>
            <div class="navigation">
                <div class="menu-bar">
                    <div class="logo-row">
                        <div class="hamburger" @click="toggleMenu" aria-label="Toggle menu">
                            <Icon icon="carbon:text-align-justify" class="icon-lg"/>
                        </div>
                        <NuxtLink :to="localePath('/')">
                            <div class="logo-text">
                                <img src="/assets/logo/Footylytics-4.svg" alt="Logo" class="logo" />
                            </div>
                        </NuxtLink>
                        <LanguageSwitcher />
                    </div> 
                    <ul class="menu" :class="{ 'menu-open': menuOpen }">
                        <li><NuxtLink :to="localePath('/compare')" @click="menuOpen = false" :class="{ 'nav-active': route.path.includes('/compare')}">{{ $t('navigation.compare') }}</NuxtLink></li>
                        <li><NuxtLink :to="localePath('/seasons')" @click="menuOpen = false" :class="{ 'nav-active': route.path.includes('/seasons')}">{{ $t('navigation.seasons') }}</NuxtLink></li>
                        <li><NuxtLink :to="localePath('/teams')" @click="menuOpen = false" :class="{ 'nav-active': route.path.includes('/teams')}">{{ $t('navigation.teams') }}</NuxtLink></li>
                        <li><NuxtLink :to="localePath('/players')" @click="menuOpen = false" :class="{ 'nav-active': route.path.includes('/players')}">{{ $t('navigation.players') }}</NuxtLink></li>
                        <li><NuxtLink :to="localePath('/manual')" class="manual" @click="menuOpen = false" :class="{ 'nav-active': route.path.includes('/manual')}">{{ $t('navigation.manual') }}</NuxtLink></li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
</template>
<style scoped>
header nav {
  position: fixed;
  width: 100%;
  z-index: 50;
  backdrop-filter: blur(6px);
  background: rgba(31, 41, 55, 0.7); 
  border-bottom: 1px solid #374151;
}

header nav .navigation {
  max-width: 80rem; 
  margin-left: auto;
  margin-right: auto;
}

.logo {
  width: 220px;
  height: 50px;
}


header nav .menu-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 5rem;
}

header nav .logo-row {
  display: flex;
  align-items: center;
  gap: 20px;
}

header nav ul.menu {
  display: flex;
  align-items: center;
  margin: 0;
  margin-right: 30px;
  padding: 0;
  list-style: none;
}

.hamburger {
  display: none;
  background: none;
  border: none;
  color: #d1d5db;
  cursor: pointer;
  padding: 0;
  align-items: center;
  justify-content: center;
}

.hamburger:hover {
  color: #ffc7c7;
}

@media (max-width: 1320px) {
  header nav .menu-bar {
    margin: 0 32px 0 32px;
  }
}
@media (max-width: 840px) {
  header nav .menu-bar {
    flex-direction: column;
    margin: 1rem 0;
    align-items: center;
    height: 5.5rem;
  }
  header nav {
    height: 8rem;
  }
}
@media (max-width: 480px) {
  .hamburger {
    display: flex;
  }

  header nav .menu-bar {
    flex-direction: column;
    height: auto;
    padding: 0;
    margin: 0;
  }

  header nav {
    height: auto;
    overflow-x: hidden;
  }

  header nav .logo-row {
    width: 100%;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    box-sizing: border-box;
  }

  .logo {
    width: 150px;
    height: auto;
  }

  header nav ul.menu {
    display: none;
    margin: 0;
    padding: 0;
    flex-direction: column;
    width: 100%;
    background: rgba(20, 28, 40, 0.95);
    position: static;
    border-bottom: 1px solid #374151;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
  }

  header nav ul.menu.menu-open {
    display: flex;
    max-height: 100vh;
  }

  header nav ul.menu li {
    width: 100%;
  }

  header nav ul.menu li a, header nav ul.menu li .nuxt-link {
    display: block;
    padding: 1rem;
    border-radius: 0;
  }
}

header nav ul.menu li a, header nav ul.menu li .nuxt-link {
  color: #e6e6e6;         
  padding: 0.75rem 0.75rem;
  font-size: 0.875rem;    
  font-weight: 500;       
  transition: color 150ms, background 150ms;
  text-decoration: none;
  background: none;
}

header nav ul.menu li a:hover, header nav ul.menu li .nuxt-link:hover {
  color: #ffc7c7;
}


header nav ul.menu li .manual {
  color: #fff;
}
</style>