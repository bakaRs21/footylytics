<script setup>
import { computed, ref, toRaw, onMounted } from 'vue';
import {Icon} from '@iconify/vue';

const { t } = useI18n()
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
                title: t('components.compareStats.gameTime'),
                icon: 'openmoji:stopwatch',
                metrics: [
                    { key: 'total_matches_played', label: t('components.compareStats.appearances'),   type: 'number' },
                    { key: 'games_lineups',         label: t('components.compareStats.starts'),        type: 'number' },
                    { key: 'total_minutes_played',  label: t('components.compareStats.minutes'),       type: 'number' },
                    { key: 'rating',                label: t('components.compareStats.avgRating'),    type: 'success' },
                ]
            },
            attacking: {
                title: t('components.compareStats.attacking'),
                icon: 'openmoji:soccer-ball',
                metrics: [
                    { key: 'total_goals',       label: t('components.compareStats.goals'),         type: 'success' },
                    { key: 'total_assists',      label: t('components.compareStats.assists'),       type: 'success' },
                    { key: 'total_shots',        label: t('components.compareStats.totalShots'),         type: 'number' },
                    { key: 'shots_on_target',    label: t('components.compareStats.shotsOnTarget'),     type: 'success' },
                    { key: 'dribbles_success',   label: t('components.compareStats.dribblesSuccessful'),  type: 'success' },
                    { key: 'dribbles_attempts',  label: t('components.compareStats.dribbleAttempts'), type: 'number' },
                ]
            },
            passing: {
                title: t('components.compareStats.passing'),
                icon: 'openmoji:bullseye',
                metrics: [
                    { key: 'total_passes',   label: t('components.compareStats.totalPasses'),  type: 'number' },
                    { key: 'key_passes',     label: t('components.compareStats.keyPasses'),    type: 'success' },
                    { key: 'pass_accuracy',  label: t('components.compareStats.shotAccuracy'),    type: 'success' },
                ]
            },
            defensive: {
                title: t('components.compareStats.defensive'),
                icon: 'openmoji:shield',
                metrics: [
                    { key: 'total_tackles',         label: t('components.compareStats.totalTackles'),           type: 'number' },
                    { key: 'tackles_interceptions', label: t('components.compareStats.interceptions'),     type: 'success' },
                    { key: 'tackles_blocks',        label: t('components.compareStats.blocks'),            type: 'success' },
                    { key: 'total_duels',           label: t('components.compareStats.duels'),             type: 'number' },
                    { key: 'duels_won',             label: t('components.compareStats.duelsWon'),         type: 'success' },
                ]
            },
            discipline: {
                title: t('components.compareStats.discipline'),
                icon: 'openmoji:warning',
                metrics: [
                    { key: 'fouls_committed',  label: t('components.compareStats.foulsCommitted'),  type: 'danger',  lowerIsBetter: true },
                    { key: 'fouls_drawn',      label: t('components.compareStats.foulsDrawn'),      type: 'success' },
                    { key: 'yellow_cards',     label: t('components.compareStats.yellowCards'),     type: 'warning', lowerIsBetter: true },
                    { key: 'red_cards',        label: t('components.compareStats.redCards'),        type: 'danger',  lowerIsBetter: true },
                ]
            },
            goalkeeper: {
                title: t('components.playerStatsDashboard.goalkeeperStats'),
                icon: 'openmoji:gloves',
                metrics: [
                    { key: 'saves',           label: t('components.playerStatsDashboard.saves'),            type: 'success' },
                    { key: 'goals_conceded',  label: t('components.playerStatsDashboard.goalsConceded'),   type: 'danger',  lowerIsBetter: true },
                    { key: 'penalties_saved', label: t('components.playerStatsDashboard.penaltiesSaved'),  type: 'success' },
                ]
            }
        };
    }
    return {
        matches: {
            title: t('components.teamStatsDashboard.matchesOverview'),
            icon: 'openmoji:soccer-ball',
            metrics: [
                { key: 'total_matches_played', label: t('components.teamStatsDashboard.totalMatches'), type: 'number' },
                { key: 'total_wins',           label: t('components.teamStatsDashboard.wins'),           type: 'win' },
                { key: 'total_draws',          label: t('components.teamStatsDashboard.draws'),          type: 'draw' },
                { key: 'total_losses',         label: t('components.teamStatsDashboard.losses'),         type: 'loss',    lowerIsBetter: true }
            ]
        },
        goals: {
            title: t('components.teamStatsDashboard.goalsAndPerformance'),
            icon: 'openmoji:goal-net',
            metrics: [
                { key: 'total_goals_scored',    label: t('components.teamStatsDashboard.goalsScored'),    type: 'success' },
                { key: 'total_goals_conceded',  label: t('components.teamStatsDashboard.goalsConceded'),  type: 'danger',  lowerIsBetter: true },
                { key: 'total_clean_sheets',    label: t('components.teamStatsDashboard.cleanSheets'),    type: 'success' },
                { key: 'total_failed_to_score', label: t('components.teamStatsDashboard.failedToScore'), type: 'danger',  lowerIsBetter: true }
            ]
        },
        streaks: {
            title: t('components.teamStatsDashboard.streaks'),
            icon: 'openmoji:chart-increasing',
            metrics: [
                { key: 'biggest_win_streak',   label: t('components.teamStatsDashboard.biggestWinStreak'),   type: 'win' },
                { key: 'biggest_draw_streak',  label: t('components.teamStatsDashboard.biggestDrawStreak'),  type: 'draw' },
                { key: 'biggest_lose_streak',  label: t('components.teamStatsDashboard.biggestLoseStreak'),  type: 'loss',    lowerIsBetter: true }
            ]
        },
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
    const el = document.getElementById('stats')
    if (!el) return
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
})
</script>

<template>
<div v-if="competitors.length === 2" class="comparison-wrapper" id="stats">
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
     <div v-if="overallWinner" class="winner-banner" :class="overallWinner.winner">
        <div class="winner-label">
            <span v-if="overallWinner.winner === 'tie'" class="winner-title">
                <span><Icon icon="openmoji:handshake" class="icon-md"/></span>
                <span>{{ $t('components.compareStats.tie') }}</span>
            </span>
            <span v-else class="winner-title">
                <span><Icon icon="openmoji:crown" class="icon-lg" /> </span>
                <span>{{ $t('components.compareStats.overallWinner') }}: </span>
                <strong>{{ overallWinner.winner === 'first' ? overallWinner.firstName : overallWinner.secondName }}</strong>
            </span>
            <span class="winner-subtitle">
                {{ overallWinner.firstWins }}W vs {{ overallWinner.secondWins }}W
                {{ $t('common.outOf') }} {{ overallWinner.total }} {{ $t('common.metrics') }}
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
            <h3 class="section-title">
                <span class="section-icon">
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
        <div v-if="type !== 'player' && competitors.some(c => c.lineups)" class="metric-group">
        <h3 class="section-title">
            <span class="section-icon">
                <Icon icon="openmoji:edit" class="icon-lg"/>
            </span>
            {{ $t('components.teamStatsDashboard.formations') }}
        </h3>
        <div class="lineups-comparison">
            <div v-for="(comp, cIndex) in competitors" :key="comp.id" class="lineups-column">
                <h4 class="column-header">{{ comp.name }}</h4>
                <div v-if="comp.lineups" class="lineups-list">
                    <div v-for="(lineup, lIndex) in comp.lineups" :key="`${comp.id}-${lIndex}`" class="lineup-wrapper">
                        <div class="lineup-item" @click="toggleLineup(cIndex, lIndex)">
                            <span class="formation">{{ lineup.formation }}</span>
                            <span class="played-count">{{ $t('statistics.labels.matches') }}: {{ lineup.played }}</span>
                            <span class="lineup-arrow" :class="{ 'arrow-rotated': isLineupActive(cIndex, lIndex) }">
                                <Icon icon="mdi:chevron-downkdkf" />
                            </span>
                        </div>
                        <div v-if="isLineupActive(cIndex, lIndex)" class="lineup-details">
                            <LineUps :data="lineup" />
                        </div>
                    </div>
                </div>
                <div v-else class="no-data">{{ $t('common.noFormations') }}</div>
            </div>
        </div>
    </div>
    <div v-if="competitors.some(c => c.form)" class="metric-group">
        <h3 class="section-title">
            <span class="section-icon">
                <Icon icon="openmoji:chart-increasing" class="icon-lg"/>
            </span>
            {{ $t('components.compareStats.recentForm') }}
        </h3>
        <div class="form-comparison">
            <div v-for="comp in competitors" :key="comp.id" class="form-column">
                <h4 class="column-header">{{ comp.name }}</h4>
                <div v-if="comp.form" class="form-display">
                    <div v-for="(result, index) in comp.form" :key="`${comp.id}-form-${index}`" :class="['form-badge', result.toLowerCase()]">
                        {{ result }}
                    </div>
                </div>
                <div v-else class="no-data">{{ $t('components.compareStats.noForm') }}</div>
            </div>
        </div>
        <p class="form-note">{{ $t('components.compareStats.formNote') }}</p>
    </div>
    <div v-if="competitors.some(c => c.rawStats.total_penalties_scored !== undefined)" class="metric-group">
        <h3 class="section-title">
            <span class="section-icon">
                <Icon icon="openmoji:goal-net" class="icon-lg"/>
            </span>
            {{ $t('components.compareStats.penalties') }}
        </h3>
        <div class="comparison-grid">
            <div class="metric-row">
                <div class="metric-value first success"
                    :class="{ 'winner': isWinner(competitors[0].rawStats.total_penalties_scored, competitors[1].rawStats.total_penalties_scored, false) }">
                    <span class="value">{{ competitors[0].rawStats.total_penalties_scored ?? 0 }}</span>
                </div>
                <div class="metric-label">{{ $t('components.compareStats.penaltiesScored') }}</div>
                <div class="metric-value second success"
                    :class="{ 'winner': isWinner(competitors[1].rawStats.total_penalties_scored, competitors[0].rawStats.total_penalties_scored, false) }">
                    <span class="value">{{ competitors[1].rawStats.total_penalties_scored ?? 0 }}</span>
                </div>
            </div>
            <div class="metric-row">
                <div class="metric-value first danger"
                    :class="{ 'winner': isWinner(competitors[0].rawStats.total_penalties_missed, competitors[1].rawStats.total_penalties_missed, true) }">
                    <span class="value">{{ competitors[0].rawStats.total_penalties_missed ?? 0 }}</span>
                </div>
                <div class="metric-label">{{ $t('components.compareStats.penaltiesMissed') }}</div>
                <div class="metric-value second danger"
                    :class="{ 'winner': isWinner(competitors[1].rawStats.total_penalties_missed, competitors[0].rawStats.total_penalties_missed, true) }">
                    <span class="value">{{ competitors[1].rawStats.total_penalties_missed ?? 0 }}</span>
                </div>
            </div>
        </div>
    </div>
    </div>
</div>
<div v-else class="loading-state">
        <p>{{ $t('common.loading') }}</p>
</div>
</template>