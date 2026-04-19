<script setup>
import { ref, computed } from 'vue';
import { Icon } from '@iconify/vue';

const { t } = useI18n()

const props = defineProps({
    teams: {
        type: Object,
        required: true,
    }
})

const sortOptions = [
    { key: 'points',           label: t('components.seasonRankingTable.points'),           icon: 'material-symbols:trophy-outline',        dir: 'desc' },
    { key: 'wins',             label: t('components.seasonRankingTable.wins'),             icon: 'material-symbols:check-circle-outline',  dir: 'desc' },
    { key: 'goal_difference',  label: t('components.seasonRankingTable.goalDifference'),  icon: 'material-symbols:sports-score',          dir: 'desc' },
    { key: 'goals_for',        label: t('components.seasonRankingTable.goalsFor'),        icon: 'material-symbols:sports-soccer',         dir: 'desc' },
    { key: 'goals_against',    label: t('components.seasonRankingTable.goalsAgainst'),    icon: 'material-symbols:cancel-outline',        dir: 'asc'  },
    { key: 'matches',          label: t('components.seasonRankingTable.matchesPlayed'),   icon: 'material-symbols:event-note-outline',    dir: 'desc' },
    { key: 'draws',            label: t('components.seasonRankingTable.draws'),           icon: 'material-symbols:pause-circle-outline', dir: 'desc' },
    { key: 'losses',           label: t('components.seasonRankingTable.losses'),          icon: 'material-symbols:x-circle-outline',  dir: 'asc'  },
    { key: 'win_rate_pct',     label: t('components.seasonRankingTable.winRate'),        icon: 'material-symbols:percent',               dir: 'desc' },
    { key: 'points_per_match', label: t('components.seasonRankingTable.pointsPerMatch'), icon: 'material-symbols:calculate-outline',     dir: 'desc' },
]

const activeSort = ref(sortOptions[0])
const sortDir    = ref('desc')

function applySort(option) {
    if (activeSort.value.key === option.key) {
        sortDir.value = sortDir.value === 'desc' ? 'asc' : 'desc'
    } else {
        activeSort.value = option
        sortDir.value = option.dir
    }
}

const sortedTeams = computed(() => {
    return [...props.teams.ranking].sort((a, b) => {
        const va = a[activeSort.value.key]
        const vb = b[activeSort.value.key]
        return sortDir.value === 'desc' ? vb - va : va - vb
    })
})

function goalDiffLabel(goalDiff) {
    if (goalDiff > 0) return '+' + goalDiff
    return String(goalDiff)
}
function goalDiffClass(goalDiff) {
    if (goalDiff > 0) return 'green'
    if (goalDiff < 0) return 'red'
    return 'muted'
}
function formClass(wins, draws, losses) {
    const total = wins + draws + losses || 1
    const rate  = wins / total
    if (rate >= 0.6) return 'form-great'
    if (rate >= 0.4) return 'form-good'
    if (rate >= 0.2) return 'form-poor'
    return 'form-bad'
}
</script>

<template>
<div class="ranking-wrapper">
    <div class="ranking-header">
        <div class="ranking-title">
            <Icon icon="material-symbols:format-list-numbered" class="header-icon" />
            <span>{{ $t('components.seasonRankingTable.rank') }}</span>
        </div>
        <div class="team-count-pill">
            <Icon icon="material-symbols:groups-outline" />
            {{ props.teams.ranking.length }} {{ $t('components.searchableCards.teams') }}
        </div>
    </div>
    <div class="sort-bar">
        <span class="sort-label">
            <Icon icon="material-symbols:sort" />
            {{ $t('common.select') }}
        </span>
        <div class="sort-options">
            <button
                v-for="option in sortOptions"
                :key="option.key"
                class="sort-btn"
                :class="{ active: activeSort.key === option.key }"
                @click="applySort(option)"
            >
                <Icon :icon="option.icon" class="sort-btn-icon" :class="option.label"/>
                {{ option.label }}
                <Icon
                    v-if="activeSort.key === option.key"
                    :icon="sortDir === 'desc' ? 'material-symbols:arrow-downward' : 'material-symbols:arrow-upward'"
                    class="sort-dir-icon"
                />
            </button>
        </div>
    </div>
    <div class="table-scroll">
        <table class="ranking-table">
            <thead>
                <tr>
                    <th class="col-rank">#</th>
                    <th class="col-team">{{ $t('components.seasonRankingTable.team') }}</th>
                    <th class="col-num" :title="$t('components.seasonRankingTable.matchesPlayed')">MP</th>
                    <th class="col-num" :title="$t('components.seasonRankingTable.wins')">W</th>
                    <th class="col-num" :title="$t('components.seasonRankingTable.draws')">D</th>
                    <th class="col-num" :title="$t('components.seasonRankingTable.losses')">L</th>
                    <th class="col-num" :title="$t('components.seasonRankingTable.goalsFor')">GF</th>
                    <th class="col-num" :title="$t('components.seasonRankingTable.goalsAgainst')">GA</th>
                    <th class="col-num" :title="$t('components.seasonRankingTable.goalDifference')">GD</th>
                    <th class="col-num col-pts" :title="$t('components.seasonRankingTable.points')">Pts</th>
                    <th class="col-num" :title="$t('components.seasonRankingTable.pointsPerMatch')">P/M</th>
                    <th class="col-num" :title="$t('components.seasonRankingTable.winRate')">W%</th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="(team, index) in sortedTeams"
                    :key="team.team_id"
                    class="team-row"
                    :class="[
                        index === 0 ? 'rank-1' : '',
                        index === 1 ? 'rank-2' : '',
                        index === 2 ? 'rank-3' : '',
                    ]"
                >
                    <td class="col-rank">
                        <span class="rank-badge">
                            <Icon v-if="index === 0" icon="material-symbols:trophy" class="rank-trophy gold" />
                            <Icon v-else-if="index === 1" icon="material-symbols:trophy" class="rank-trophy silver" />
                            <Icon v-else-if="index === 2" icon="material-symbols:trophy" class="rank-trophy bronze" />
                            <span v-else class="rank-num">{{ index + 1 }}</span>
                        </span>
                    </td>
                    <td class="col-team">
                        <div class="team-cell">
                            <span class="team-name">{{ team.team_name }}</span>
                            <div class="form-bar" :class="formClass(team.wins, team.draws, team.losses)">
                                <div class="form-fill" :style="{ width: team.win_rate_pct + '%' }"></div>
                            </div>
                        </div>
                    </td>
                    <td class="col-num">{{ team.matches }}</td>
                    <td class="col-num text-green">{{ team.wins }}</td>
                    <td class="col-num text-muted">{{ team.draws }}</td>
                    <td class="col-num text-red">{{ team.losses }}</td>
                    <td class="col-num">{{ team.goals_for }}</td>
                    <td class="col-num">{{ team.goals_against }}</td>
                    <td class="col-num" :class="`text-${goalDiffClass(team.goal_difference)}`">{{ goalDiffLabel(team.goal_difference) }}</td>
                    <td class="col-num col-pts">
                        <span class="pts-badge">{{ team.points }}</span>
                    </td>
                    <td class="col-num text-muted">{{ team.points_per_match.toFixed(2) }}</td>
                    <td class="col-num">
                        <span class="wr-text" :class="team.win_rate_pct >= 50 ? 'text-green' : team.win_rate_pct >= 30 ? 'text-yellow' : 'text-red'">
                            {{ team.win_rate_pct }}%
                        </span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<style scoped>
.ranking-wrapper {
    width: 100%;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.ranking-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.75rem;
    padding: 0 0.25rem;
}

.ranking-title {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 1.3rem;
    font-weight: 700;
    color: #e2e8f0;
}

.header-icon {
    font-size: 1.4rem;
    color: rgba(61, 214, 140, 0.9);
}

.team-count-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 0.3rem 0.75rem;
    background: rgba(61, 214, 140, 0.08);
    border: 1px solid rgba(61, 214, 140, 0.2);
    border-radius: 9999px;
    color: rgba(61, 214, 140, 0.85);
}

.sort-bar {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.sort-label {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
    padding-top: 0.45rem;
    white-space: nowrap;
}

.sort-options {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
}

.sort-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.35rem 0.7rem;
    font-size: 0.78rem;
    font-weight: 500;
    color: #94a3b8;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 9999px;
    cursor: pointer;
    transition: background 0.2s, border-color 0.2s, color 0.2s;
    white-space: nowrap;
}

.sort-btn:hover {
    background: rgba(61, 214, 140, 0.07);
    border-color: rgba(61, 214, 140, 0.25);
    color: #e2e8f0;
}

.sort-btn.active {
    background: rgba(61, 214, 140, 0.12);
    border-color: rgba(61, 214, 140, 0.4);
    color: rgba(61, 214, 140, 0.95);
}

.sort-btn-icon  { font-size: 0.9rem; }
.sort-dir-icon  { font-size: 0.85rem; margin-left: 0.1rem; }

.table-scroll {
    overflow-x: auto;
    border-radius: 10px;
    border: 1px solid rgba(61, 214, 140, 0.35);
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
}

.ranking-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
}

.ranking-table thead tr {
    background: rgba(61, 214, 140, 0.06);
    border-bottom: 1px solid rgba(61, 214, 140, 0.18);
}

.ranking-table th {
    padding: 0.7rem 0.85rem;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #64748b;
    text-align: center;
    white-space: nowrap;
}

.ranking-table th.col-team { text-align: left; }

.team-row {
    background: #16162e40;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    transition: background 0.18s;
}

.team-row:last-child { border-bottom: none; }

.team-row:hover { background: rgba(61, 214, 140, 0.05); }

.team-row.rank-1 { background: rgba(255, 197, 48,  0.05); }
.team-row.rank-2 { background: rgba(180, 190, 200, 0.04); }
.team-row.rank-3 { background: rgba(180, 120, 60,  0.04); }
.team-row.rank-1:hover { background: rgba(255, 197, 48,  0.09); }
.team-row.rank-2:hover { background: rgba(180, 190, 200, 0.08); }
.team-row.rank-3:hover { background: rgba(180, 120, 60,  0.08); }

.ranking-table td {
    padding: 0.65rem 0.85rem;
    text-align: center;
    color: #e2e8f0;
    white-space: nowrap;
    font-variant-numeric: tabular-nums;
}

.col-rank { width: 52px; }
.col-team { text-align: left; min-width: 160px; }
.col-num  { min-width: 48px; }

.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
}

.rank-num { font-size: 0.85rem; font-weight: 600; color: #64748b; }
.rank-trophy        { font-size: 1.1rem; }
.rank-trophy.gold   { color: #fbbf24; }
.rank-trophy.silver { color: #94a3b8; }
.rank-trophy.bronze { color: #c07842; }

.team-cell {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}

.team-name {
    font-weight: 600;
    color: #e2e8f0;
    font-size: 0.9rem;
}

.form-bar {
    height: 3px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 9999px;
    overflow: hidden;
    max-width: 120px;
}

.form-fill { height: 100%; border-radius: 9999px; transition: width 0.5s ease; }
.form-great .form-fill { background: rgba(34,  197, 94,  0.85); }
.form-good  .form-fill { background: rgba(234, 179, 8,   0.85); }
.form-poor  .form-fill { background: rgba(251, 146, 60,  0.85); }
.form-bad   .form-fill { background: rgba(239, 68,  68,  0.8);  }

.col-pts { font-weight: 700; }

.pts-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 32px;
    padding: 0.15rem 0.45rem;
    background: rgba(61, 214, 140, 0.1);
    border: 1px solid rgba(61, 214, 140, 0.25);
    border-radius: 6px;
    color: rgba(61, 214, 140, 0.95);
    font-size: 0.88rem;
    font-weight: 700;
}

.wr-text { font-weight: 600; font-size: 0.82rem; }

.Draws {
    rotate: 270deg;
}

@media (max-width: 840px) {
    .ranking-wrapper { padding: 0.75rem; }
    .ranking-table th,
    .ranking-table td { padding: 0.55rem 0.6rem; }
}
</style>