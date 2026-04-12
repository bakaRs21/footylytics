<script setup>
import { Icon } from '@iconify/vue';

const page = "player";

const config = useRuntimeConfig()
const { pending: isLoading, data: players, error } = await useFetch(`${config.public.apiBase}players/with-seasons-teams`, {
  lazy: true,
})
</script>
<template>
    <div class="page-heading"> 
    <h1 class="h1-design">{{ $t('pages.players.title') }}</h1>
  </div>
  <div v-if="isLoading">
    <h2 class="pending-design">{{ $t('common.loading') }}</h2>
    <Icon icon="mdi:loading" />
  </div>
  <div v-else-if="error">
    {{ $t('common.error') }}: {{ error.message }}
  </div>
  <div v-else>
    <SearchableCards :enable-links="true" :items="players" :page="page" :placeholder="$t('pages.players.searchPlaceholder')"/>
  </div>
</template>