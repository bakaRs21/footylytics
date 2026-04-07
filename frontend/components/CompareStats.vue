<script setup>
import { computed, ref, toRaw, onMounted } from 'vue';
import {Icon} from '@iconify/vue';
const comparing = ref(null);

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
                icon: 'openmoji:stopwatch',
                metrics: [
                    { key: 'total_matches_played', label: 'Appearances',   type: 'number' },
                    { key: 'games_lineups',         label: 'Starts',        type: 'number' },
                    { key: 'total_minutes_played',  label: 'Minutes',       type: 'number' },
                    { key: 'rating',                label: 'Avg Rating',    type: 'success' },
                ]
            },
            attacking: {
                title: 'Attacking',
                icon: 'openmoji:soccer-ball',
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
                icon: 'openmoji:bullseye',
                metrics: [
                    { key: 'total_passes',   label: 'Total Passes',  type: 'number' },
                    { key: 'key_passes',     label: 'Key Passes',    type: 'success' },
                    { key: 'pass_accuracy',  label: 'Accuracy %',    type: 'success' },
                ]
            },
            defensive: {
                title: 'Defensive',
                icon: 'openmoji:shield',
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
                icon: 'openmoji:warning',
                metrics: [
                    { key: 'fouls_committed',  label: 'Fouls Committed',  type: 'danger',  lowerIsBetter: true },
                    { key: 'fouls_drawn',      label: 'Fouls Drawn',      type: 'success' },
                    { key: 'yellow_cards',     label: 'Yellow Cards',     type: 'warning', lowerIsBetter: true },
                    { key: 'red_cards',        label: 'Red Cards',        type: 'danger',  lowerIsBetter: true },
                ]
            },
            goalkeeper: {
                title: 'Goalkeeper',
                icon: 'openmoji:gloves',
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
            icon: 'openmoji:soccer-ball',
            metrics: [
                { key: 'total_matches_played', label: 'Matches Played', type: 'number' },
                { key: 'total_wins',           label: 'Wins',           type: 'win' },
                { key: 'total_draws',          label: 'Draws',          type: 'draw' },
                { key: 'total_losses',         label: 'Losses',         type: 'loss',    lowerIsBetter: true }
            ]
        },
        goals: {
            title: 'Goals & Performance',
            icon: 'openmoji:goal-net',
            metrics: [
                { key: 'total_goals_scored',    label: 'Goals Scored',    type: 'success' },
                { key: 'total_goals_conceded',  label: 'Goals Conceded',  type: 'danger',  lowerIsBetter: true },
                { key: 'total_clean_sheets',    label: 'Clean Sheets',    type: 'success' },
                { key: 'total_failed_to_score', label: 'Failed to Score', type: 'danger',  lowerIsBetter: true }
            ]
        },
        streaks: {
            title: 'Streaks',
            icon: 'openmoji:chart-increasing',
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
const overallWinner = computed(() => {
    if (competitors.value.length !== 2) return null;

    const [c1, c2] = competitors.value;
    let firstWins = 0;
    let secondWins = 0;

    Object.values(metricGroups.value).forEach(group => {
        group.metrics.forEach(metric => {
            const v1 = c1.rawStats[metric.key];
            const v2 = c2.rawStats[metric.key];
            if (v1 == null || v2 == null) return;
            if (isWinner(v1, v2, metric.lowerIsBetter)) firstWins++;
            else if (isWinner(v2, v1, metric.lowerIsBetter)) secondWins++;
        });
    });

    const total = firstWins + secondWins;
    return {
        firstWins,
        secondWins,
        total,
        winner: firstWins > secondWins ? 'first'
              : secondWins > firstWins ? 'second'
              : 'tie',
        firstName: props.firstName,
        secondName: props.secondName,
        firstPct:  total > 0 ? Math.round((firstWins  / total) * 100) : 50,
        secondPct: total > 0 ? Math.round((secondWins / total) * 100) : 50,
    };
});

onMounted(() => {
    if (comparing.value) {
        const offset = 80;
        const top = comparing.value.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
    }
})
</script>

<template>
<div v-if="competitors.length === 2" class="comparison-wrapper" >
    <div class="comparison-header" ref="comparing">
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
     <div v-if="overallWinner" class="winner-banner" :class="overallWinner.winner">
        <div class="winner-label">
            <span v-if="overallWinner.winner === 'tie'" class="winner-title">
                <span><Icon icon="openmoji:handshake" class="icon-md"/></span>
                <span>It's a Tie!</span>
            </span>
            <span v-else class="winner-title">
                <span><Icon icon="openmoji:crown" class="icon-lg" /> </span>
                <span>Overall Winner: </span>
                <strong>{{ overallWinner.winner === 'first' ? overallWinner.firstName : overallWinner.secondName }}</strong>
            </span>
            <span class="winner-subtitle">
                {{ overallWinner.firstWins }}W vs {{ overallWinner.secondWins }}W
                out of {{ overallWinner.total }} metrics
            </span>
        </div>
        <div class="winner-bar-track">
            <div
                class="winner-bar-fill first-fill"
                :style="{ width: overallWinner.firstPct + '%' }"
            >
                <span v-if="overallWinner.firstPct > 15" class="bar-label">
                    {{ overallWinner.firstName }} {{ overallWinner.firstPct }}%
                </span>
            </div>
            <div
                class="winner-bar-fill second-fill"
                :style="{ width: overallWinner.secondPct + '%' }"
            >
                <span v-if="overallWinner.secondPct > 15" class="bar-label">
                    {{ overallWinner.secondName }} {{ overallWinner.secondPct }}%
                </span>
            </div>
        </div>
    </div>
    <div class="metrics-container">
        <div v-for="(group, groupKey) in metricGroups" :key="groupKey" class="metric-group">
            <h3 class="group-title">
                <span class="group-icon">
                    <Icon :icon="group.icon" class="icon-lg"/>
                </span>
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
            <span class="group-icon">
                <Icon icon="openmoji:edit" class="icon-lg"/>
            </span>
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
                                <Icon icon="mdi:chevron-downkdkf" />
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
            <span class="group-icon">
                <Icon icon="openmoji:chart-increasing" class="icon-lg"/>
            </span>
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
            <span class="group-icon">
                <Icon icon="openmoji:goal-net" class="icon-lg"/>
            </span>
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