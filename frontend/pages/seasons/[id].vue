<script setup>
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()
const selectedSeason = ref(route.params.id || "")

const { data: teams, error: teamsError } = await useFetch(`${config.public.apiBase}Teams/${selectedSeason.value}`)
</script>
<template>
    {{ selectedSeason }}
    Teams in this season:
    {{ teams }}
</template>
