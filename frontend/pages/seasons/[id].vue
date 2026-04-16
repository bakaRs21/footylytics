<script setup>
  import { Icon } from '@iconify/vue';
  import { ref, onMounted } from 'vue';
import MatchesDashboard from '~/components/MatchesDashboard.vue';
  import SeasonRankingTable from '~/components/SeasonRankingTable.vue';
  import SeasonStats from '~/components/SeasonStats.vue';
  const { t } = useI18n()
const config = useRuntimeConfig()
const route = useRoute()
const selectedSeason = ref(` ${route.params.id} - ${Number(route.params.id) + 1} `)
const seasonParam = ref(route.params.id)
const onMountedMsg = ref("")
const stats = ref(null)
const statsStatus = ref("")
const statsError = ref("")
const rankings = ref(null)
const matches = ref([])
const referees = ref([])
const showMatches = ref(false)
const sections = [
  { label: t("pages.seasons.sections.seasonStats"), anchor: "stats" },
  { label: t("pages.seasons.sections.seasonRanking"), anchor: "metrics" },
  { label: t("pages.seasons.sections.matches"), anchor: "matches" },
]

watch(() => showMatches.value, async (newVal) => {
  if (newVal) {
    fetchMatches()
  }
})
function Inspection() {
  if (!seasonParam.value) {
     onMountedMsg.value = "Season not selected. Please select a season to view the stats."
  }
  onMountedMsg.value = ""
  fetchData()
}
async function fetchMatches() {
  try {
    const matchData = await $fetch(`${config.public.apiBase}seasons/${seasonParam.value}/matches`)
    const refereesData = await $fetch(`${config.public.apiBase}referees`)
    matches.value = matchData
    referees.value = refereesData
  } catch (error) {
    console.error("Error fetching matches or referees:", error)
  }
}
async function fetchData() {
  statsStatus.value = 'pending'
  statsError.value = ""
  try {
    const [first, second, third, fourth] = await Promise.all([
      $fetch(`${config.public.apiBase}season-metrics/stats?season_id=${seasonParam.value}`),
      $fetch(`${config.public.apiBase}season-metrics/team-ranking?season_id=${seasonParam.value}`)
    ])
    stats.value = first
    rankings.value = second
    statsStatus.value = ""
  } catch (error) {
    statsError.value = error.message
    statsStatus.value = "error"
  }
}

onMounted(() => {
  Inspection()
})
</script>
<template>
  <div v-if="onMountedMsg">
    {{ onMountedMsg }}
  </div>
  <div v-if="statsStatus === 'pending'">
    {{ $t('common.loading') }} <Icon icon="mdi:loading" />
  </div>
  <div v-if="statsError">
    Error: {{ statsError }}
  </div>
  <div v-if="stats">
    <h2 class="h1-design" id="stats">{{ selectedSeason }} {{ $t('statistics.labels.stats') }}</h2>
    <SeasonStats :data="stats" />
  </div>
  <div v-if="rankings">
    <h2 class="h1-design" id="metrics">{{ selectedSeason }} {{ $t('statistics.labels.ranking') }}</h2>
    <SeasonRankingTable :teams="rankings" />
  </div>
  <div class="matches">
      <div @click="showMatches = !showMatches" class="title-with-arrows" style="cursor: pointer;">
        <Icon icon="mdi:chevron-down" />
        <h2 id="matches">{{ $t('pages.seasons.sections.matches') }}</h2>
        <Icon icon="mdi:chevron-down" />
      </div>
      <div v-if="showMatches && matches.length > 0">
        <MatchesDashboard :matches="matches" :referees="referees" :page="'season'" />
      </div>
    </div>

  <PageContent :page-sections="sections" />
</template>