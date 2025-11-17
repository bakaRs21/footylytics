<template>
    <header>
        <nav>
            <div class="navigation">
                <div class="menu-bar">
                    <div class="logo-row">
                        <NuxtLink to="/">
                            <div class="logo-text">
                                Go Home
                            </div>
                        </NuxtLink>
                    </div> 
                    <ul class="menu">
                        <li><NuxtLink to="/seasons/">Seasons</NuxtLink></li>
                        <li><NuxtLink to="/teams/">Teams</NuxtLink></li>
                        <li><NuxtLink to="/about">About</NuxtLink></li>
                        <li><NuxtLink to="/documentation" class="docs">Docs</NuxtLink></li>
                        <li><NuxtLink to="/manual" class="manual">ElManuel</NuxtLink></li>
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
  padding-left: 16px;
  padding-right: 16px;
}

@media (min-width: 640px) {
  header nav .navigation {
    padding-left: 24px;
    padding-right: 24px;
  }
}
@media (min-width: 1024px) {
  header nav .navigation {
    padding-left: 32px;
    padding-right: 32px;
  }
}

header nav .menu-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
}

header nav .logo-row {
  display: flex;
  align-items: center;
}
header nav .logo-row .logo-text {
  margin-left: 0.5rem; 
  color: #fff;
  font-size: 1.125rem;
  font-weight: 700;  
  letter-spacing: 0.05em; 
}

header nav ul.menu {
  display: flex;
  align-items: center;
  gap: 1rem; 
  margin: 0;
  padding: 0;
  list-style: none;
}

header nav ul.menu li a, header nav ul.menu li .nuxt-link {
  color: #d1d5db;         
  padding: 0.75rem 0.75rem;
  border-radius: 0.375rem; 
  font-size: 0.875rem;    
  font-weight: 500;       
  transition: color 150ms, background 150ms;
  text-decoration: none;
  background: none;
}

header nav ul.menu li a:hover, header nav ul.menu li .nuxt-link:hover {
  color: #ffc7c7;
}

header nav ul.menu li .docs,
header nav ul.menu li .manual {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

header nav ul.menu li .manual {
  background: #dc2626;
  color: #fff;
}
header nav ul.menu li .manual:hover {
  background: #7f1d1d;
}

@media (max-width: 600px) {
  header nav .container {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
  }
  header nav .menu-bar {
    flex-direction: column;
    height: auto;
  }
}

.router-link-exact-active {
    color: rgb(245, 241, 13);
}
</style>