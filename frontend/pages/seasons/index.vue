<script setup>
import { Icon } from '@iconify/vue';

const { t } = useI18n()
const config = useRuntimeConfig()
const {status, data: seasons, error } = await useFetch(`${config.public.apiBase}compare/Seasons`, {
  lazy: true,
})
</script>
<template>
  <div class="page-heading">
    <h1 class="h1-design">{{ $t('pages.seasons.title') }}</h1>
  </div>
  <div>
    <div v-if="status === 'pending'">
      <h2 class="pending-design">{{ $t('common.loading') }}</h2>
      <Icon icon="mdi:loading" />
    </div>
    <div v-else-if="error">
      {{ $t('common.error') }}: {{ error.message }}
    </div>
    <div v-else>
      <SearchableCards :enable-links="true" :items="seasons" :page="'season'" :placeholder="$t('pages.seasons.searchPlaceholder')" />
    </div>
  </div>
</template>



<style scoped>
</style>