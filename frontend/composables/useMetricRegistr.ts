export type MetricKind = 'bar' | 'donut' | 'pie' | 'minuteBuckets' | 'table'

export interface DisplaySpec {
  kind: MetricKind
  valueKey?: string
  labelKey?: string
  unit?: string
  decimals?: number
  higherIsBetter?: boolean
}

// Player
const REGISTRY: Record<string, DisplaySpec> = {
  goals_per_match:          { kind: 'bar', valueKey: 'average_goals_per_match',   labelKey: 'player_name', unit: 'goals', decimals: 3 },
  assists_per_match:        { kind: 'bar', valueKey: 'average_assists_per_match',  labelKey: 'player_name', unit: 'assists', decimals: 3 },
  shots_per_match:          { kind: 'bar', valueKey: 'average_shots_per_match',    labelKey: 'player_name', unit: 'shots', decimals: 3 },
  minutes_per_match:        { kind: 'bar', valueKey: 'average_minutes_per_match',  labelKey: 'player_name', unit: 'min', decimals: 1 },
  penalty_success_rate:     { kind: 'bar', valueKey: 'penalty_succes_rate',        labelKey: 'player_name', unit: '%', decimals: 1 },
  shots_accuracy:           { kind: 'bar', valueKey: 'accuracy_pct',               labelKey: 'player_name', unit: '%', decimals: 2 },
  basic_player_stats:       { kind: 'table' },

  // Team
  goals__scored_per_match:              { kind: 'bar', valueKey: 'avg_goals_scored_per_match',   labelKey: 'team_name', unit: 'goals', decimals: 3 },
  goals_conceded_per_match:             { kind: 'bar', valueKey: 'avg_goals_conceded_per_match',  labelKey: 'team_name', unit: 'goals', decimals: 3 },
  goal_difference_per_match:            { kind: 'bar', valueKey: 'goal_diff_per_match',            labelKey: 'team_name', decimals: 3 },
  attack_defense_balance:               { kind: 'bar', valueKey: 'attack_defense_balance',         labelKey: 'team_name' },
  points_per_match:                     { kind: 'bar', valueKey: 'points_per_match',               labelKey: 'team_name', decimals: 3 },
  win_rate:                             { kind: 'bar', valueKey: 'win_rate_pct',                   labelKey: 'team_name', unit: '%', decimals: 2 },
  points_per_goal_scored:               { kind: 'bar', valueKey: 'points_per_goal_scored',         labelKey: 'team_name', decimals: 3 },
  season_consistency_index:             { kind: 'bar', valueKey: 'season_consistency_index',       labelKey: 'team_name', decimals: 3 },
  goals_scored_percentage_by_minutes:   { kind: 'minuteBuckets' },
  goals_conceded_percentage_by_minutes: { kind: 'minuteBuckets' },
  basic_team_stats:                     { kind: 'table' },
}

export function useMetricRegistry() {
  function resolve(metricKey: string, apiDisplay?: DisplaySpec): DisplaySpec {
    return apiDisplay ?? REGISTRY[metricKey] ?? { kind: 'bar' }
  }

  function toBarSeries(rows: any[], spec: DisplaySpec, seriesLabel: string) {
    return {
      series: [{ name: seriesLabel, data: rows.map(r => r[spec.valueKey!] ?? 0) }],
      categories: rows.map(r => r[spec.labelKey!] ?? '?'),
    }
  }

  function toDonutSeries(rows: any[], spec: DisplaySpec, seriesLabel: string) {
    return {
      series: rows.map(r => r[spec.valueKey!] ?? 0),
      labels: rows.map(r => r[spec.labelKey!] ?? '?'),
    }
  }

  const MINUTE_BUCKETS = [
    'minutes_0_15', 'minutes_16_30', 'minutes_31_45', 'minutes_46_60',
    'minutes_61_75', 'minutes_76_90', 'minutes_91_105', 'minutes_106_120',
    ]

    const BUCKET_LABELS = [
    '0–15', '16–30', '31–45', '46–60',
    '61–75', '76–90', '91–105', '106–120',
    ]

    function toMinuteBucketSeries(rows: any[]) {
    const series = rows.map(r => ({
        name: `Team ${r.team_id} / Season ${r.season_id}`,
        data: MINUTE_BUCKETS.map(b => r[b]?.percentage ?? 0),
    }))

    return {
        series,
        categories: BUCKET_LABELS,
    }
    }
}