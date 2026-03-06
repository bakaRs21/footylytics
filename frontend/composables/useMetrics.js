import { ref, computed } from 'vue'
import { PLAYER_CHART_CONFIGS, TEAM_CHART_CONFIGS } from './useMetricConfig.js'

export function useMetrics() {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  const playerMetrics = ref([])   // raw from backend
  const teamMetrics = ref([])     // raw from backend
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

  // Merge backend options with frontend chart config
  // Result: { key, label, params, allowedCharts, toChartData }
  const mergedPlayerMetrics = computed(() =>
    playerMetrics.value
      .map(opt => ({
        ...opt,                                  // key, label, params from backend
        ...PLAYER_CHART_CONFIGS[opt.key],        // allowedCharts, toChartData from frontend
      }))
      .filter(opt => opt.allowedCharts)          // skip any not yet configured in frontend
  )

  const mergedTeamMetrics = computed(() =>
    teamMetrics.value
      .map(opt => ({
        ...opt,
        ...TEAM_CHART_CONFIGS[opt.key],
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