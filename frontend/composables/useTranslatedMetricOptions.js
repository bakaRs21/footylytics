export function useTranslatedMetricOptions() {
  const { t, te } = useI18n()

  function translateOptions(options) {
    return (options ?? []).map(option => ({
      ...option,
      label: te(`components.metricDashboard.metricOptions.${option.key}`) ? t(`components.metricDashboard.metricOptions.${option.key}`) : option.label
    }))
  }

  return { translateOptions }
}