<script setup>
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()
const selectedSeason = ref(route.params.id || "")

const { status: teamStatus, data: teamsInSeason, error: teamInSeasonError } = await useFetch(`${config.public.apiBase}seasons/${selectedSeason.value}/teams`, {
  lazy: true,
})
</script>
<template>
    {{ teamInSeason }}
</template>