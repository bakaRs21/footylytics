<script setup>
import card from '~/components/card.vue';

const config = useRuntimeConfig()
const { data: teams, error } = await useFetch(`${config.public.apiBase}compare/Teams`, {
  lazy: true,
})

</script>

<template>
  <div class="page-heading"> 
    <h1 class="h1-design">Teams Page</h1>
  </div>
  <div>
    <div v-if="error">
      Error: {{ error.message }}
    </div>
    <div v-else>
      <div v-for="team in teams" :key="team" class="card-margin">
        <div v-for="value in team" :key="index" class="card-grid">
            <NuxtLink :to="`/teams/${value}`">
              <card id="card">{{ value }}</card>
            </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-margin {
  margin-top: 80px;
}
.card-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(390px, 1fr));
}
#card {
  max-width: 327px;
}
</style>