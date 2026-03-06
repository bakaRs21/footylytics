import { ref, computed } from 'vue'
import { PLAYER_METRIC_CONFIGS, TEAM_METRIC_CONFIGS } from './useMetricConfig.js'

export function useMetrics() {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  const playerMetrics = ref([])
  const teamMetrics = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function loadMetricOptions() {
    loading.value = true
    error.value = null
    try {
      const [playerOpts, teamOpts] = await Promise.all([
        $fetch(`${apiBase}/player-metrics/options`),
        $fetch(`${apiBase}/team-metrics/options`),
      ])
      playerMetrics.value = playerOpts
      teamMetrics.value = teamOpts
    } catch (e) {
      error.value = e?.message ?? 'Failed to load metric options'
    } finally {
      loading.value = false
    }
  }

  const mergedPlayerMetrics = computed(() =>
    playerMetrics.value
      .map(opt => ({
        ...opt,
        ...PLAYER_METRIC_CONFIGS[opt.key],
      }))
      .filter(opt => opt.allowedCharts)
  )

  const mergedTeamMetrics = computed(() =>
    teamMetrics.value
      .map(opt => ({
        ...opt,
        ...TEAM_METRIC_CONFIGS[opt.key],
      }))
      .filter(opt => opt.allowedCharts)
  )

  return {
    loadMetricOptions,
    mergedPlayerMetrics,
    mergedTeamMetrics,
    loading,
    error,
  }
}