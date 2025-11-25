<script setup>
const config = useRuntimeConfig()
const route = useRoute()
const query = useRoute().query
const id = route.params.id
console.log(id)
//const { status, data, error } = await useFetch(`${config.public.apiBase}api/${$route.params.id}`)
</script>

<template>
    <div class="page-heading">
        <h1 class ="h1-design">Comparing {{ id }}</h1>
    {{ query }}
    </div>
</template>