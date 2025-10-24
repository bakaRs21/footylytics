<template>
    <div>
        <header>
            <nav class="fixed w-full z-50 backdrop-blur-sm bg-gray-800/70 border-b border-gray-700">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex items-center justify-between h-16">
                        <div class="flex items-center">
                            <NuxtLink to="/">
                                <div class="ml-2">
                                    <span class="text-white text-lg font-bold tracking-wide">Go Home</span>
                                </div>
                            </NuxtLink>
                        </div> 
                        <ul class="flex items-center space-x-4">
                            <li><NuxtLink to="/seasons/" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition duration-150">Seasons</NuxtLink></li>
                            <li><NuxtLink to="/teams/" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition duration-150">Teams</NuxtLink></li>
                            <li><NuxtLink to="/about" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition duration-150">About</NuxtLink></li>
                            <li><NuxtLink to="/manual" class="bg-red-600 hover:bg-red-900 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150">ElManuel</NuxtLink></li>
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
        <div class= "pt-24 px-4 sm:px-6 lg:px-8 pb-8 max-w-7xl mx-auto text-center">
            <slot />
        </div>
    </div>
</template>
<style scoped>
@import "tailwindcss";
@tailwind utilities;

    .router-link-exact-active {
        color: rgb(245, 241, 13);
    }

    @layer components {
        .container-main {
            @apply pt-24 px-4 sm:px-6 lg:px-8 pb-8 max-w-7xl mx-auto text-center;
        }
        .h1-position {
            @apply text-center mb-16 text-4xl md:text-6xl font-bold text-white mb-6 leading-tight;
        }
        .h1-design {
            @apply bg-clip-text bg-gradient-to-r;
        }
    }
</style>