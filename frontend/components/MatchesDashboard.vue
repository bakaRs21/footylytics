<script setup lang="ts">
import { ref, computed } from 'vue'

interface Match {
  season_id: number
  fixture_id: number
  fixture_date: string
  fixture_venue_name: string
  fixture_venue_city: string
  league_name: string
  league_round: string
  fixture_status_short: string
  fixture_status_long: string
  fixture_status_elapsed: number | null
  home_team_id: number
  away_team_id: number
  teams_home_name: string
  teams_away_name: string
  teams_home_logo: string
  teams_away_logo: string
  teams_home_winner: boolean | null
  teams_away_winner: boolean | null
  goals_home: number | null
  goals_away: number | null
  score_halftime_home: number | null
  score_halftime_away: number | null
  score_fulltime_home: number | null
  score_fulltime_away: number | null
  score_extratime_home: number | null
  score_extratime_away: number | null
  score_penalty_home: number | null
  score_penalty_away: number | null
  referee_id: number | null
}

interface Referee {
  referee_id: number
  name: string
}

const props = defineProps<{
  matches: Match[]
  referees: Referee[]
  page: string
  title?: string
}>()

function getRefereeName(id: number | null): string {
  if (id === null) return '—'
  return props.referees.find(r => r.referee_id === id)?.name ?? `#${id}`
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC',
  })
}

function roundLabel(round: string): string {
  return round.replace('Regular Season - ', 'R')
}

function matchResult(match: Match, side: 'home' | 'away'): 'W' | 'D' | 'L' | null {
  if (match.goals_home === null || match.goals_away === null) return null
  if (match.goals_home === match.goals_away) return 'D'
  if (side === 'home') return match.goals_home > match.goals_away ? 'W' : 'L'
  return match.goals_away > match.goals_home ? 'W' : 'L'
}

function statusPillClass(status: string): string {
  if (status === 'FT') return 'pill-badge pill-green'
  if (['1H', 'HT', '2H', 'ET', 'P'].includes(status)) return 'pill-badge pill-teal'
  if (status === 'NS') return 'pill-badge pill-yellow'
  return 'pill-badge pill-blue'
}

type VenueFilter = 'all' | 'home' | 'away'
const venueFilter = ref<VenueFilter>('all')
const refereeFilter = ref<number | null>(null)

const focalTeamId = computed<number | null>(() => {
  if (!props.matches.length) return null
  const freq = new Map<number, number>()
  for (const m of props.matches) {
    freq.set(m.home_team_id, (freq.get(m.home_team_id) ?? 0) + 1)
    freq.set(m.away_team_id, (freq.get(m.away_team_id) ?? 0) + 1)
  }
  return [...freq.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? null
})

const allTeams = computed(() => {
  const map = new Map<number, string>()
  for (const m of props.matches) {
    map.set(m.home_team_id, m.teams_home_name)
    map.set(m.away_team_id, m.teams_away_name)
  }
  return [...map.entries()]
    .map(([id, name]) => ({ id, name }))
    .sort((a, b) => a.name.localeCompare(b.name))
})

const selectedTeamId = ref<number | null>(null)
const filterMode = ref<'venue' | 'team'>('venue')

const availableReferees = computed(() => {
  const refereeIds = new Set<number>()
  for (const m of props.matches) {
    if (m.referee_id !== null) {
      refereeIds.add(m.referee_id)
    }
  }
  return props.referees.filter(r => refereeIds.has(r.referee_id))
})

const filteredMatches = computed(() => {
    let matches = props.matches
    if (refereeFilter.value !== null) {
        matches = matches.filter(m => m.referee_id === refereeFilter.value)
    }
    if (props.page === 'team') {
        if (filterMode.value === 'venue') {
            if (venueFilter.value === 'all' || focalTeamId.value === null) return matches
            matches = matches.filter(
                m => venueFilter.value === 'home'
                ? m.home_team_id === focalTeamId.value
                : m.away_team_id === focalTeamId.value
            )
        }
    } else if (props.page === 'season') {
        if (selectedTeamId.value !== null) {
            matches = matches.filter(
                m => m.home_team_id === selectedTeamId.value || m.away_team_id === selectedTeamId.value
            )
        }
    }
    return matches
})

const teamStats = computed(() => {
    const teamId = props.page === 'team' ? focalTeamId.value : selectedTeamId.value
    if (teamId === null) return { wins: 0, losses: 0 }
    
    let wins = 0
    let losses = 0

    for (const match of filteredMatches.value) {
        if (match.goals_home === null || match.goals_away === null) continue

        const isHome = match.home_team_id === teamId
        const isAway = match.away_team_id === teamId

        if (isHome) {
            if (match.goals_home > match.goals_away) wins++
            else if (match.goals_home < match.goals_away) losses++
        } else if (isAway) {
            if (match.goals_away > match.goals_home) wins++
            else if (match.goals_away < match.goals_home) losses++
        }
    }

    return { wins, losses }
})
watch(() => props.matches, async (newVal) => {
    if (newVal.length > 0) {
        scrollToDashboard()
    }
})
async function scrollToDashboard() {
  await nextTick()
  const el = document.getElementById('matches')
  if (!el) return
  el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<template>
  <div v-if="matches" class="card-dashboard wrapper" id="matches">
    <div class="card-header">
        <div class="filter-group" v-if="page === 'team'">
          <span class="label-filter">Venue</span>
          <div class="filter-chips">
            <button
                v-for="opt in (['all', 'home', 'away'] as VenueFilter[])"
                :key="opt"
                class="btn-chip"
                :class="{ active: venueFilter === opt }"
                @click="venueFilter = opt, filterMode = 'venue'"
            >
              {{ opt.charAt(0).toUpperCase() + opt.slice(1) }}
            </button>
          </div>
        </div>
        <div class="filter-group" v-if="page === 'team' || page === 'season'">
            <span class="label-filter">Referees</span>
            <select v-model="refereeFilter" class="filter-select">
                <option :value="null">All Referees</option>
                <option v-for="ref in availableReferees" :key="ref.referee_id" :value="ref.referee_id">
                    {{ ref.name }}
                </option>
            </select>
        </div>
        <div class="filter-group" v-if="page === 'season'">
            <span class="label-filter">Team</span>
            <select v-model="selectedTeamId" class="filter-select">
                <option :value="null">All Teams</option>
                <option v-for="team in allTeams" :key="team.id" :value="team.id">
                {{ team.name }}
                </option>
            </select>
        </div>
      <span class="subtitle-text" style="margin-left: auto;">
        {{ filteredMatches.length }} matches
        <span v-if="(page === 'season' && selectedTeamId) || page === 'team'">
            <span style="color: lightgreen;">{{ teamStats.wins }}W</span>
            <span style="color: red;">{{ teamStats.losses }}L</span>
        </span>
      </span>
    </div>
    <div class="card-content" style="padding: 0; overflow-x: auto; align-items: flex-start;">
      <table class="matches-table">
        <thead>
          <tr>
            <th class="subtitle-text">Date</th>
            <th class="subtitle-text">Round</th>
            <th class="subtitle-text" style="text-align: right;">Home</th>
            <th class="subtitle-text" style="text-align: center;">Score</th>
            <th class="subtitle-text" style="text-align: left;">Away</th>
            <th class="subtitle-text" style="text-align: center;">Venue</th>
            <th class="subtitle-text" style="text-align: center;">Referee</th>
            <th class="subtitle-text" style="text-align: center;">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="match in filteredMatches" :key="match.fixture_id" class="match-row">
            <td>
              <div class="flex-col" style="gap: 2px;">
                <span class="text-light text-medium" style="font-size: 0.75rem; white-space: nowrap;">
                  {{ formatDate(match.fixture_date) }}
                </span>
                <span class="text-muted" style="font-size: 0.72rem; white-space: nowrap;">
                  {{ formatTime(match.fixture_date) }} UTC
                </span>
              </div>
            </td>
            <td>
              <span class="pill-badge pill-blue" style="font-size: 0.72rem;">
                {{ roundLabel(match.league_round) }}
              </span>
            </td>
            <td>
              <div class="flex-center" style="gap: 0.4rem; justify-content: flex-end;">
                <span class="text-light text-medium" style="font-size: 0.75rem; white-space: nowrap;">
                  {{ match.teams_home_name }}
                </span>
                <img
                  :src="match.teams_home_logo"
                  :alt="match.teams_home_name"
                  width="22"
                  height="22"
                  loading="lazy"
                  style="object-fit: contain; flex-shrink: 0;"
                />
              </div>
            </td>
            <td>
              <div class="flex-center" style="gap: 3px;">
                <span
                  class="stat-value-sm"
                  :class="{
                    'text-green': matchResult(match, 'home') === 'W',
                    'text-red':   matchResult(match, 'home') === 'L',
                  }"
                >{{ match.goals_home ?? '–' }}</span>
                <span class="text-muted" style="font-weight: 400;">:</span>
                <span
                  class="stat-value-sm"
                  :class="{
                    'text-green': matchResult(match, 'away') === 'W',
                    'text-red':   matchResult(match, 'away') === 'L',
                  }"
                >{{ match.goals_away ?? '–' }}</span>
              </div>
              <div class="text-muted" style="font-size: 0.7rem; text-align: center; margin-top: 1px; font-variant-numeric: tabular-nums;">
                HT {{ match.score_halftime_home }}:{{ match.score_halftime_away }}
              </div>
            </td>
            <td>
              <div class="flex-center" style="gap: 0.4rem; justify-content: flex-start;">
                <img
                  :src="match.teams_away_logo"
                  :alt="match.teams_away_name"
                  width="22"
                  height="22"
                  loading="lazy"
                  style="object-fit: contain; flex-shrink: 0;"
                />
                <span class="text-light text-medium" style="font-size: 0.75rem; white-space: nowrap;">
                  {{ match.teams_away_name }}
                </span>
              </div>
            </td>
            <td>
              <div class="flex-col" style="gap: 2px;">
                <span class="text-light-gray" style="font-size: 0.75rem; white-space: nowrap;">
                  {{ match.fixture_venue_name }}
                </span>
                <span class="text-muted" style="font-size: 0.7rem; white-space: nowrap;">
                  {{ match.fixture_venue_city }}
                </span>
              </div>
            </td>
            <td>
              <span class="text-gray" style="font-size: 0.75rem; white-space: nowrap;">
                {{ getRefereeName(match.referee_id) }}
              </span>
            </td>

            <td style="text-align: center;">
              <span :class="statusPillClass(match.fixture_status_short)" style="font-size: 0.72rem;">
                {{ match.fixture_status_short }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
    border-color: rgba(61, 214, 140, 0.35);
    box-shadow: none;
}

.filter-select {
    margin: 0; 
    width: auto;
    font-size: 12px;
    padding: 5px 12px;
}

.matches-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 700px;
}

.matches-table thead tr {
  background-color: #1a2332;
  border-bottom: 2px solid #2d3a4a;
}

.matches-table th {
  padding: 10px 12px;
  text-align: left;
  white-space: nowrap;
}

.matches-table tbody tr {
  border-bottom: 1px solid #1e2a3a;
  transition: background 0.15s ease;
}

.matches-table tbody tr:last-child {
  border-bottom: none;
}

.match-row:hover {
  background-color: #1a2332;
}

.matches-table td {
  padding: 9px 12px;
  vertical-align: middle;
}
</style>