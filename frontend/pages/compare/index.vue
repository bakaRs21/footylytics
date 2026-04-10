<script setup>
const { t } = useI18n()

const compareOptions = [
  { key: 'Seasons', label: t('pages.compare.compareSeasons') },
  { key: 'Teams', label: t('pages.compare.compareTeams') },
  { key: 'Players', label: t('pages.compare.comparePlayers') }
]
</script>

<template>
    <div class="page-heading">
        <h1 class="h1-design">{{ $t('pages.compare.title') }}</h1>
        <h3>{{ $t('pages.compare.subtitle') }}</h3>
    </div>
    <div class="card-margin">
        <div class="card-grid">
          <div v-for="option in compareOptions" :key="option.key">
              <NuxtLink :to="`/compare/${option.key}`">
                <card id="card">{{ option.label }}</card>
              </NuxtLink>
          </div>
        </div>
    </div>
</template>

<style scoped>
.card-margin {
  margin-top: 100px;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 120px;
}
@media (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>