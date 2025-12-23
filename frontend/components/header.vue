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
                        <li><NuxtLink to="/compare">Compare</NuxtLink></li>
                        <li><NuxtLink to="/seasons/">Seasons</NuxtLink></li>
                        <li><NuxtLink to="/teams/">Teams</NuxtLink></li>
                        <li><NuxtLink to="/players/">Players</NuxtLink></li>
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
  padding-left: 10px;
  padding-right: 10px;
}
@media (max-width: 512px) {
  header nav ul.menu {
    gap: 0.5rem; 
  }
}
@media (min-width: 513px) and (max-width: 580px) {
  header nav ul.menu {
    gap: 1rem;
  }
}

@media (max-width: 580px) {
  header nav .menu-bar {
    flex-direction: column;
    align-items: flex-start;
    height: 5rem;
    gap: 10px;
  }
  header nav .navigation {
    padding-left: 0; 
    padding-right: 0;

  }
  header nav .logo-row {
    margin-top: 10px;
  }
}

@media (max-width: 809px) and (min-width: 581px) {
  header nav .menu-bar {
    justify-content: space-evenly;
    height: 4rem;
  }
}

@media (min-width: 810px) {
  header nav .navigation {
    padding-left: 26px;
    padding-right: 50px;
  }
  header nav .menu-bar {
    justify-content: space-between;
    height: 4rem;
  }
  header nav ul.menu {
    gap: 14px; 
  }
  
}
@media (min-width: 1024px) {
  header nav .navigation {
    padding-left: 32px;
    padding-right: 32px;
  }
  header nav .menu-bar {
    height: 4rem;
  }
}

header nav .menu-bar {
  display: flex;
  align-items: center;
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

.router-link-exact-active {
    color: rgb(245, 241, 13);
}
</style>