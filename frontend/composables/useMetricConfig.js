//      PLAYER METRICS
export const PLAYER_METRIC_CONFIGS = {
  goals_per_match: {
    label: 'Goals per Match',
    endpoint: '/player-metrics/goals-per-match',
    allowedCharts: ['Bar Chart', 'Line Chart'],
    sharedGraph: 'player_per_match',
    toChartData(rows, _chartType) {
      return {
        series: [{ name: 'Avg Goals/Match', data: rows.map(r => r.average_goals_per_match) }],
        categories: rows.map(r => r.player_name),
      }
    },
  },
  assists_per_match: {
    label: 'Assists per Match',
    endpoint: '/player-metrics/assists-per-match',
    allowedCharts: ['Bar Chart', 'Line Chart'],
    sharedGraph: 'player_per_match',
    toChartData(rows, _chartType) {
      return {
        series: [{ name: 'Avg Assists/Match', data: rows.map(r => r.average_assists_per_match) }],
        categories: rows.map(r => r.player_name),
      }
    },
  },
  shots_per_match: {
    label: 'Shots per Match',
    endpoint: '/player-metrics/shots-per-match',
    allowedCharts: ['Bar Chart', 'Line Chart'],
    sharedGraph: 'player_per_match',
    toChartData(rows, _chartType) {
      return {
        series: [{ name: 'Avg Shots/Match', data: rows.map(r => r.average_shots_per_match) }],
        categories: rows.map(r => r.player_name),
      }
    },
  },
  minutes_per_match: {
    label: 'Minutes per Match',
    endpoint: '/player-metrics/minutes-per-match',
    allowedCharts: ['Bar Chart', 'Line Chart'],
    sharedGraph: null,
    toChartData(rows, _chartType) {
      return {
        series: [{ name: 'Avg Minutes/Match', data: rows.map(r => r.average_minutes_per_match) }],
        categories: rows.map(r => r.player_name),
      }
    }
  },
  penalty_success_rate: {
    label: 'Penalty Success Rate',
    endpoint: '/player-metrics/penalty-success-rate',
    allowedCharts: ['Bar Chart', 'Donut Chart', 'Pie Chart'],
    sharedGraph: 'player_accuracy',
    toChartData(rows, chartType) {
      if (chartType === 'Donut Chart' || chartType === 'Pie Chart') {
        return {
          series: rows.map(r => r.penalty_succes_rate),
          labels: rows.map(r => r.player_name),
        }
      }
      return {
        series: [{ name: 'Penalty Success %', data: rows.map(r => r.penalty_succes_rate) }],
        categories: rows.map(r => r.player_name),
      }
    },
  },
  shots_accuracy: {
    label: 'Shot Accuracy',
    endpoint: '/player-metrics/shots-accuracy',
    allowedCharts: ['Bar Chart', 'Donut Chart', 'Pie Chart'],
    sharedGraph: 'player_accuracy',
    toChartData(rows, chartType) {
      if (chartType === 'Donut Chart' || chartType === 'Pie Chart') {
        return {
          series: rows.map(r => r.accuracy_pct),
          labels: rows.map(r => r.player_name),
        }
      }
      return {
        series: [{ name: 'Shot Accuracy %', data: rows.map(r => r.accuracy_pct) }],
        categories: rows.map(r => r.player_name),
      }
    },
  },
}

//      TEAM METRICS

export const TEAM_METRIC_CONFIGS = {
  goals_scored_per_match: {
    label: 'Goals Scored/Match',
    endpoint: '/team-metrics/goals-scored-per-match',
    metricValue: 'goals_scored_per_match',
    allowedCharts: ['Bar Chart', 'Line Chart', "Pie Chart"],
    sharedGraph: {
      bar: {name : 'team_per_match_bar', type: 'bar'},
      pie: {name: 'team_per_match_pie', type: 'pie'}
    },  
    toChartData(rows, chartType) {
      if (chartType === 'Pie Chart') {
        return {
          series: rows.map(r => r.avg_goals_scored_per_match),
          categories: rows.map(r => r.team_name)
        }
      }
      return {
        series: [{ name: 'Avg Goals Scored', data: rows.map(r => r.avg_goals_scored_per_match) }],
        categories: rows.map(r => r.team_name),
      }
    },
  },
  goals_conceded_per_match: {
    label: 'Goals Conceded/Match',
    endpoint: '/team-metrics/goals-conceded-per-match',
    metricValue: 'goals_conceded_per_match',
    allowedCharts: ['Bar Chart', 'Line Chart', 'Pie Chart'],
    sharedGraph: {
      bar: {name : 'team_per_match_bar', type: 'bar'},
      pie: {name: 'team_per_match_pie', type: 'pie'}
    },
    toChartData(rows, chartType) {
      if (chartType === 'Pie Chart') {
        return {
          series: rows.map(r => r.avg_goals_conceded_per_match),
          categories: rows.map(r => r.team_name)
        }
      }
      return {
        series: [{ name: 'Avg Goals Conceded', data: rows.map(r => r.avg_goals_conceded_per_match) }],
        categories: rows.map(r => r.team_name),
      }
    },
  },
  win_rate: {
    label: 'Win Rate (%)',
    endpoint: '/team-metrics/win-rate',
    metricValue: 'win_rate_pct',
    allowedCharts: ['Bar Chart', 'Donut Chart', 'Pie Chart'],
    sharedGraph: null,
    toChartData(rows, chartType) {
      if (chartType === 'Donut Chart' || chartType === 'Pie Chart') {
        return {
          series: rows.map(r => r.win_rate_pct),
          labels: rows.map(r => r.team_name),
        }
      }
      return {
        series: [{ name: 'Win Rate %', data: rows.map(r => r.win_rate_pct) }],
        categories: rows.map(r => r.team_name),
      }
    },
  },
  points_per_match: {
    label: 'Points per Match',
    endpoint: '/team-metrics/points-per-match',
    metricValue: 'points_per_match',
    allowedCharts: ['Bar Chart', 'Line Chart', 'Pie Chart'],
    sharedGraph: {
      bar: {name : 'team_per_match_bar', type: 'bar'},
      pie: {name: 'team_per_match_pie', type: 'pie'}
    },
    toChartData(rows, chartType) {
      if (chartType === 'Pie Chart') {
        return {
          series: rows.map(r => r.points_per_match),
          categories: rows.map(r => r.team_name)
        }
      }
      return {
        series: [{ name: 'Points/Match', data: rows.map(r => r.points_per_match) }],
        categories: rows.map(r => r.team_name),
      }
    },
  },
  goal_difference_per_match: {
    label: 'Goal Difference/Match',
    endpoint: '/team-metrics/goal-difference-per-match',
    metricValue: 'goal_diff_per_match',
    allowedCharts: ['Bar Chart', 'Line Chart'],
    sharedGraph: {
      bar: {name : 'team_per_match_bar', type: 'bar'}
    },
    toChartData(rows, _chartType) {
      return {
        series: [{ name: 'Goal Diff/Match', data: rows.map(r => r.goal_diff_per_match) }],
        categories: rows.map(r => r.team_name),
      }
    },
  },
  attack_defense_balance: {
    label: 'Attack-Defense Balance (GF - GA)',
    endpoint: '/team-metrics/attack-defense-balance',
    metricValue: 'attack_defense_balance',
    allowedCharts: ['Bar Chart', 'Line Chart'],
    sharedGraph: null,
    toChartData(rows, _chartType) {
      return {
        series: [{ name: 'GF - GA', data: rows.map(r => r.attack_defense_balance) }],
        categories: rows.map(r => r.team_name),
      }
    },
  },
  points_per_goal_scored: {
    label: 'Points per Goal Scored',
    endpoint: '/team-metrics/points-per-goal-scored',
    metricValue: 'points_per_goal_scored',
    allowedCharts: ['Bar Chart', 'Line Chart', 'Pie Chart'],
    sharedGraph: {
      bar: { name: 'team_efficiency_bar', type: 'bar' },
      pie: { name: 'team_efficiency_pie', type: 'pie' },
    },
    toChartData(rows, chartType) {
      if (chartType === 'Pie Chart') {
        return {
          series: rows.map(r => r.points_per_goal_scored),
          categories: rows.map(r => r.team_name)
        }
      }
      return {
        series: [{ name: 'Points/Goal', data: rows.map(r => r.points_per_goal_scored ?? 0) }],
        categories: rows.map(r => r.team_name),
      }
    },
  },
  season_consistency_index: {
    label: 'Season Consistency Index',
    endpoint: '/team-metrics/season-consistency-index',
    metricValue: 'season_consistency_index',
    allowedCharts: ['Bar Chart', 'Line Chart', 'Pie Chart'],
    sharedGraph: {
      bar: { name: 'team_efficiency_bar', type: 'bar' },
      pie: { name: 'team_efficiency_pie', type: 'pie' },
    },
    toChartData(rows, chartType) {
      if (chartType === 'Pie Chart') {
        return {
          series: rows.map(r => r.season_consistency_index),
          categories: rows.map(r => r.team_name)
        }
      }
      return {
        series: [{ name: 'Consistency Index', data: rows.map(r => r.season_consistency_index ?? 0) }],
        categories: rows.map(r => `Team ${r.team_id} S${r.season_id}`),
      }
    },
  },
  goals_scored_pct_by_minutes: {
    label: 'Goals Scored % by Minute Interval',
    endpoint: '/team-metrics/goals-scored-percentage-by-minutes',
    allowedCharts: ['Bar Chart'],
    sharedGraph: null,
    toChartData(rows, _chartType) {
      const intervals = ['0–15', '16–30', '31–45', '46–60', '61–75', '76–90', '91–105', '106–120']
      const keys = [
        'minutes_0_15', 'minutes_16_30', 'minutes_31_45', 'minutes_46_60',
        'minutes_61_75', 'minutes_76_90', 'minutes_91_105', 'minutes_106_120',
      ]
      const series = rows.map(r => ({
        name: `Team ${r.team_id} S${r.season_id}`,
        data: keys.map(k => r[k]?.percentage ?? 0),
      }))
      return { series, categories: intervals }
    },
  },
  goals_conceded_pct_by_minutes: {
    label: 'Goals Conceded % by Minute Interval',
    endpoint: '/team-metrics/goals-conceded-percentage-by-minutes',
    allowedCharts: ['Bar Chart'],
    sharedGraph: null,
    toChartData(rows, _chartType) {
      const intervals = ['0–15', '16–30', '31–45', '46–60', '61–75', '76–90', '91–105', '106–120']
      const keys = [
        'minutes_0_15', 'minutes_16_30', 'minutes_31_45', 'minutes_46_60',
        'minutes_61_75', 'minutes_76_90', 'minutes_91_105', 'minutes_106_120',
      ]
      const series = rows.map(r => ({
        name: `Team ${r.team_id} S${r.season_id}`,
        data: keys.map(k => r[k]?.percentage ?? 0),
      }))
      return { series, categories: intervals }
    },
  },
}