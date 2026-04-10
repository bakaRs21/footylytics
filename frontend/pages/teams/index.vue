<script setup>
import { Icon } from '@iconify/vue';

const { t } = useI18n()
const config = useRuntimeConfig()
const { pending: isLoading, data: teams, error } = await useFetch(`${config.public.apiBase}teams/with-seasons`, {
  lazy: true,
})
</script>

<template>
  <div class="page-heading"> 
    <h1 class="h1-design">{{ $t('pages.teams.title') }}</h1>
  </div>
  <div v-if="isLoading">
    <h2 class="pending-design">{{ $t('common.loading') }}</h2>
    <Icon icon="mdi:loading" />
  </div>
  <div v-else-if="error">
    {{ $t('common.error') }}: {{ error.message }}
  </div>
  <div v-else>
    <SearchableCards :enable-links="true" :items="teams" :page="'team'" :placeholder="$t('pages.teams.searchPlaceholder')"/>
  </div>
</template>

<style scoped>
</style>