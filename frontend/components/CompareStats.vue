<script setup>
import { computed, ref, toRaw } from 'vue';

const props = defineProps({
    firstStats: { 
        type: Object, required: true 
    },
    secondStats: { 
        type: Object, required: true 
    },
    firstName: { 
        type: String, required: true 
    },
    secondName: { 
        type: String, required: true 
    },
    type: {
        type: String,
        default: 'team',
        validator: (value) => ['team', 'player', 'season'].includes(value)
    }
});

const cleanStats = (stats) => {
    if (!stats || typeof stats !== 'object') return {};

    const raw = toRaw(stats);
    return Object.fromEntries(Object.entries(raw).filter(([_, v]) => v != null));
}

const parseLineups = (lineupString) => {
    if (!lineupString) return null;
    try {
        return JSON.parse(lineupString.replace(/'/g, '"'));
    } catch (e) {
        console.error('Failed to parse lineups:', e);
        return null;
    }
};

const parseForm = (stats) => stats.form?.split('') || null;

const competitors = computed(() => {
    if (!props.firstStats || !props.secondStats) return [];

    const c1 = {
        id: 'first',
        name: props.firstName,
        rawStats: cleanStats(props.firstStats),
    };
    const c2 = {
        id: 'second',
        name: props.secondName,
        rawStats: cleanStats(props.secondStats),
    };

    c1.lineups = parseLineups(c1.rawStats.lineups);
    c1.form = parseForm(c1.rawStats);
    c1.opponentStats = c2.rawStats;

    c2.lineups = parseLineups(c2.rawStats.lineups);
    c2.form = parseForm(c2.rawStats);
    c2.opponentStats = c1.rawStats;

    return [c1, c2];
});

const activeLineupState = ref({ 0: null, 1: null });

const toggleLineup = (sideIndex, lineupIndex) => {
    const current = activeLineupState.value[sideIndex];
    activeLineupState.value = {
        ...activeLineupState.value,
        [sideIndex]: current === lineupIndex ? null : lineupIndex
    };
};
const isLineupActive = (sideIndex, lineupIndex) => 
    activeLineupState.value[sideIndex] === lineupIndex;

const metricGroups = computed(() => {
    if (props.type === 'player') {
        return {
            games: {
                title: 'Game Time',
                icon: '🎮',
                metrics: [
                    { key: 'total_matches_played', label: 'Appearances',   type: 'number' },
                    { key: 'games_lineups',         label: 'Starts',        type: 'number' },
                    { key: 'total_minutes_played',  label: 'Minutes',       type: 'number' },
                    { key: 'rating',                label: 'Avg Rating',    type: 'success' },
                ]
            },
            attacking: {
                title: 'Attacking',
                icon: '⚽',
                metrics: [
                    { key: 'total_goals',       label: 'Goals',         type: 'success' },
                    { key: 'total_assists',      label: 'Assists',       type: 'success' },
                    { key: 'total_shots',        label: 'Shots',         type: 'number' },
                    { key: 'shots_on_target',    label: 'On Target',     type: 'success' },
                    { key: 'dribbles_success',   label: 'Dribbles Won',  type: 'success' },
                    { key: 'dribbles_attempts',  label: 'Dribble Attempts', type: 'number' },
                ]
            },
            passing: {
                title: 'Passing',
                icon: '🎯',
                metrics: [
                    { key: 'total_passes',   label: 'Total Passes',  type: 'number' },
                    { key: 'key_passes',     label: 'Key Passes',    type: 'success' },
                    { key: 'pass_accuracy',  label: 'Accuracy %',    type: 'success' },
                ]
            },
            defensive: {
                title: 'Defensive',
                icon: '🛡️',
                metrics: [
                    { key: 'total_tackles',         label: 'Tackles',           type: 'number' },
                    { key: 'tackles_interceptions', label: 'Interceptions',     type: 'success' },
                    { key: 'tackles_blocks',        label: 'Blocks',            type: 'success' },
                    { key: 'total_duels',           label: 'Duels',             type: 'number' },
                    { key: 'duels_won',             label: 'Duels Won',         type: 'success' },
                ]
            },
            discipline: {
                title: 'Discipline',
                icon: '🟨',
                metrics: [
                    { key: 'fouls_committed',  label: 'Fouls Committed',  type: 'danger',  lowerIsBetter: true },
                    { key: 'fouls_drawn',      label: 'Fouls Drawn',      type: 'success' },
                    { key: 'yellow_cards',     label: 'Yellow Cards',     type: 'warning', lowerIsBetter: true },
                    { key: 'red_cards',        label: 'Red Cards',        type: 'danger',  lowerIsBetter: true },
                ]
            },
            goalkeeper: {
                title: 'Goalkeeper',
                icon: '🧤',
                metrics: [
                    { key: 'saves',           label: 'Saves',            type: 'success' },
                    { key: 'goals_conceded',  label: 'Goals Conceded',   type: 'danger',  lowerIsBetter: true },
                    { key: 'penalties_saved', label: 'Penalties Saved',  type: 'success' },
                ]
            }
        };
    }
    return {
        matches: {
            title: 'Matches Overview',
            icon: '⚽',
            metrics: [
                { key: 'total_matches_played', label: 'Matches Played', type: 'number' },
                { key: 'total_wins',           label: 'Wins',           type: 'win' },
                { key: 'total_draws',          label: 'Draws',          type: 'draw' },
                { key: 'total_losses',         label: 'Losses',         type: 'loss',    lowerIsBetter: true }
            ]
        },
        goals: {
            title: 'Goals & Performance',
            icon: '🥅',
            metrics: [
                { key: 'total_goals_scored',    label: 'Goals Scored',    type: 'success' },
                { key: 'total_goals_conceded',  label: 'Goals Conceded',  type: 'danger',  lowerIsBetter: true },
                { key: 'total_clean_sheets',    label: 'Clean Sheets',    type: 'success' },
                { key: 'total_failed_to_score', label: 'Failed to Score', type: 'danger',  lowerIsBetter: true }
            ]
        },
        streaks: {
            title: 'Streaks',
            icon: '📊',
            metrics: [
                { key: 'biggest_win_streak',   label: 'Win Streak',   type: 'win' },
                { key: 'biggest_draw_streak',  label: 'Draw Streak',  type: 'draw' },
                { key: 'biggest_lose_streak',  label: 'Loss Streak',  type: 'loss',    lowerIsBetter: true }
            ]
        }
    };
});

function isWinner(val, opponentVal, lowerIsBetter = false) {
    const num1 = parseFloat(val) || 0;
    const num2 = parseFloat(opponentVal) || 0;
    if (num1 === num2) return false;
    return lowerIsBetter ? num1 < num2 : num1 > num2;
}

const groupHasData = (group, competitors) => {
    return group.metrics.some(metric =>
        competitors.some(c => c.rawStats[metric.key] != null)
    );
};
</script>

<template>
<div v-if="competitors.length === 2" class="comparison-wrapper">
    <div class="comparison-header">
        <div class="header-item first">
            <h2 class="entity-name">{{ firstName }}</h2>
        </div>
        <div class="header-divider">
            <span class="vs-badge">VS</span>
        </div>
        <div class="header-item second">
            <h2 class="entity-name">{{ secondName }}</h2>
        </div>
    </div>

    <div class="metrics-container">
        <div v-for="(group, groupKey) in metricGroups" :key="groupKey" class="metric-group">
            <h3 class="group-title">
                <span class="group-icon">{{ group.icon }}</span>
                {{ group.title }}
            </h3>
            <div class="comparison-grid">
                <div v-for="metric in group.metrics" :key="metric.key"class="metric-row">
                    <div class="metric-value first"
                        :class="[ metric.type,
                            { 'winner': isWinner(competitors[0].rawStats[metric.key], competitors[1].rawStats[metric.key], metric.lowerIsBetter) }
                        ]">
                        <span class="value">{{ competitors[0].rawStats[metric.key] ?? '-' }}</span>
                    </div>
                    <div class="metric-label">{{ metric.label }}</div>
                    <div 
                        class="metric-value second"
                        :class="[
                            metric.type,
                            { 'winner': isWinner(competitors[1].rawStats[metric.key], competitors[0].rawStats[metric.key], metric.lowerIsBetter) }
                        ]">
                        <span class="value">{{ competitors[1].rawStats[metric.key] ?? '-' }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div v-if="type !== 'player' && competitors.some(c => c.lineups)" class="lineups-section">
        <h3 class="section-title">
            <span class="group-icon">📋</span>
            Formations
        </h3>
        <div class="lineups-comparison">
            <div v-for="(comp, cIndex) in competitors" :key="comp.id" class="lineups-column">
                <h4 class="column-header">{{ comp.name }}</h4>
                
                <div v-if="comp.lineups" class="lineups-list">
                    <div v-for="(lineup, lIndex) in comp.lineups" :key="`${comp.id}-${lIndex}`" class="lineup-wrapper">
                        <div class="lineup-item" @click="toggleLineup(cIndex, lIndex)">
                            <span class="formation">{{ lineup.formation }}</span>
                            <span class="played-count">{{ lineup.played }} matches</span>
                            <span class="lineup-arrow" :class="{ 'arrow-rotated': isLineupActive(cIndex, lIndex) }">
                                <SmallArrowDown />
                            </span>
                        </div>
                        <div v-if="isLineupActive(cIndex, lIndex)" class="lineup-details">
                            <LineUps :data="lineup" />
                        </div>
                    </div>
                </div>
                <div v-else class="no-data">No formations available</div>
            </div>
        </div>
    </div>

    <div v-if="competitors.some(c => c.form)" class="form-section">
        <h3 class="section-title">
            <span class="group-icon">📈</span>
            Recent Form
        </h3>
        <div class="form-comparison">
            <div v-for="comp in competitors" :key="comp.id" class="form-column">
                <h4 class="column-header">{{ comp.name }}</h4>
                <div v-if="comp.form" class="form-display">
                    <div v-for="(result, index) in comp.form" :key="`${comp.id}-form-${index}`" :class="['form-badge', result.toLowerCase()]">
                        {{ result }}
                    </div>
                </div>
                <div v-else class="no-data">No form data</div>
            </div>
        </div>
        <p class="form-note">Latest match on the right</p>
    </div>
    <div v-if="competitors.some(c => c.rawStats.total_penalties_scored !== undefined)" class="penalties-section">
        <h3 class="section-title">
            <span class="group-icon">⚠️</span>
            Penalties
        </h3>
        <div class="penalties-comparison">
            <div v-for="comp in competitors" :key="comp.id" class="penalty-group">
                <h4 class="column-header">{{ comp.name }}</h4>
                <div class="penalty-stats">
                    <div class="penalty-item success">
                        <span class="penalty-value">{{ comp.rawStats.total_penalties_scored ?? 0 }}</span>
                        <span class="penalty-label">Scored</span>
                    </div>
                    <div class="penalty-item missed">
                        <span class="penalty-value">{{ comp.rawStats.total_penalties_missed ?? 0 }}</span>
                        <span class="penalty-label">Missed</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<div v-else class="loading-state">
        <p>Loading comparison...</p>
</div>
</template>

<style scoped>
.comparison-wrapper {
    width: 100%;
    padding: 1rem;
    background: #1a1a1a9c;
    min-height: 100vh;
    margin-top: 10px;
    border-top: solid 6px #1f1d2552;
}

.comparison-header {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 1rem;
    align-items: center;
    margin-bottom: 1.5rem;
    padding: 0.75rem;
    background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.header-item {
    text-align: center;
    padding: 0.75rem;
    border-radius: 8px;
    transition: transform 0.3s ease;
}

.header-item.first {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.header-item.second {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.header-item:hover {
    transform: scale(1.03);
}

.entity-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.header-divider {
    display: flex;
    align-items: center;
    justify-content: center;
}

.vs-badge {
    background: #4ade80;
    color: #000;
    padding: 0.4rem 0.9rem;
    border-radius: 50px;
    font-size: 1rem;
    font-weight: 900;
    box-shadow: 0 2px 8px rgba(74, 222, 128, 0.4);
    letter-spacing: 2px;
}

.metrics-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 1200px;
    margin: 0 auto 1.5rem;
}

.metric-group {
    background: #2a2a2a;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.group-title {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #3a3a3a;
}

.group-icon {
    font-size: 1.1rem;
}

.comparison-grid {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

.metric-row {
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    gap: 0.5rem;
    align-items: center;
    padding: 0.35rem 0.5rem;
    background: #333333;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.metric-row:hover {
    background: #3a3a3a;
    transform: translateY(-1px);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.metric-value {
    padding: 0.4rem 0.5rem;
    border-radius: 6px;
    text-align: center;
    background: #2a2a2a;
    transition: all 0.3s ease;
    position: relative;
}

.metric-value.winner {
    box-shadow: 0 0 12px rgba(34, 197, 94, 0.5);
}

.value {
    font-size: 1.2rem;
    font-weight: 700;
    color: #ffffff;
}

.metric-label {
    text-align: center;
    font-size: 0.8rem;
    font-weight: 600;
    color: #a0a0a0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-value.win .value    { color: #22c55e; }
.metric-value.draw .value   { color: #eab308; }
.metric-value.loss .value   { color: #ef4444; }
.metric-value.success .value { color: #4ade80; }
.metric-value.danger .value  { color: #f87171; }
.metric-value.warning .value { color: #fbbf24; }


.lineups-section,
.form-section,
.penalties-section {
    background: #2a2a2a;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #3a3a3a;
}

.lineups-comparison,
.form-comparison,
.penalties-comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.lineups-column,
.form-column,
.penalty-group {
    background: #333333;
    padding: 0.75rem;
    border-radius: 8px;
}

.column-header {
    font-size: 0.9rem;
    font-weight: 600;
    color: #4ade80;
    margin-bottom: 0.5rem;
    text-align: center;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #3a3a3a;
}

.lineups-list {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

.lineup-wrapper {
    margin-bottom: 0.25rem;
}

.lineup-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0.6rem;
    background: #3a3a3a;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
}

.lineup-item:hover {
    background: #404040;
    transform: translateX(3px);
}

.formation {
    font-size: 0.95rem;
    font-weight: 600;
    color: #4ade80;
}

.played-count {
    font-size: 0.8rem;
    color: #a0a0a0;
}

.lineup-arrow {
    display: flex;
    align-items: center;
    transition: transform 0.3s ease;
}

.arrow-rotated {
    transform: rotate(180deg);
}

.lineup-details {
    margin-top: 0.25rem;
    padding: 0.75rem;
    background: #2a2a2a;
    border-radius: 6px;
    animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
    from { opacity: 0; max-height: 0; }
    to   { opacity: 1; max-height: 500px; }
}

.form-display {
    display: flex;
    gap: 0.3rem;
    flex-wrap: wrap;
    justify-content: center;
}

.form-badge {
    width: 26px;
    height: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    font-weight: 700;
    font-size: 0.8rem;
    color: #fff;
    transition: transform 0.2s;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.form-badge:hover { transform: scale(1.2); }

.form-badge.w { background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); }
.form-badge.d { background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%); }
.form-badge.l { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }

.form-note {
    font-size: 0.75rem;
    color: #666;
    font-style: italic;
    text-align: center;
    margin-top: 0.5rem;
}

/* Penalties */
.penalty-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
}

.penalty-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.6rem;
    border-radius: 6px;
    background: #2a2a2a;
}

.penalty-item.success { border: 2px solid #22c55e; }
.penalty-item.missed  { border: 2px solid #ef4444; }

.penalty-value {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}

.penalty-item.success .penalty-value { color: #22c55e; }
.penalty-item.missed  .penalty-value { color: #ef4444; }

.penalty-label {
    font-size: 0.75rem;
    color: #a0a0a0;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Utility */
.no-data {
    text-align: center;
    padding: 1rem;
    color: #666;
    font-style: italic;
    font-size: 0.85rem;
}

@media (max-width: 968px) {
    .comparison-header {
        grid-template-columns: 1fr;
        gap: 0.5rem;
    }

    .header-divider { order: 2; }
    .header-item.first  { order: 1; }
    .header-item.second { order: 3; }

    .metric-row {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .lineups-comparison,
    .form-comparison,
    .penalties-comparison {
        grid-template-columns: 1fr;
    }

    .entity-name { font-size: 1.1rem; }
    .value       { font-size: 1.1rem; }
}

@media (max-width: 640px) {
    .comparison-wrapper { padding: 0.5rem; }

    .metric-group,
    .lineups-section,
    .form-section,
    .penalties-section {
        padding: 0.75rem;
    }

    .vs-badge {
        font-size: 0.9rem;
        padding: 0.35rem 0.75rem;
    }
}
</style>