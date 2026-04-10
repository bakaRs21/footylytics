<script setup>
import { computed, ref, toRaw, onMounted } from 'vue';
import { Icon } from '@iconify/vue';

const { t } = useI18n()
const comparing = ref(null);

const props = defineProps({
    firstStats:  { type: Object, required: true },
    secondStats: { type: Object, required: true },
    firstName:   { type: String, required: true },
    secondName:  { type: String, required: true },
});

const cleanStats = (stats) => {
    if (!stats || typeof stats !== 'object') return {};
    const raw = toRaw(stats);
    return Object.fromEntries(Object.entries(raw).filter(([_, v]) => v != null));
};

const competitors = computed(() => {
    if (!props.firstStats || !props.secondStats) return [];
    const c1 = { id: 'first',  name: props.firstName,  rawStats: cleanStats(props.firstStats)  };
    const c2 = { id: 'second', name: props.secondName, rawStats: cleanStats(props.secondStats) };
    c1.opponentStats = c2.rawStats;
    c2.opponentStats = c1.rawStats;
    return [c1, c2];
});

const metricGroups = computed(() => ({
    overview: {
        title: t('components.compareSeasons.seasonOverview'),
        icon: 'openmoji:soccer-ball',
        metrics: [
            { key: 'total_players',            label: t('components.compareSeasons.totalPlayers'),  type: 'number' },
            { key: 'total_player_appearances', label: t('components.compareSeasons.appearances'),    type: 'number' },
        ]
    },
    attacking: {
        title: t('components.compareSeasons.attacking'),
        icon: 'openmoji:goal-net',
        metrics: [
            { key: 'total_goals',           label: t('components.compareSeasons.goals'),            type: 'success' },
            { key: 'total_assists',         label: t('components.compareSeasons.assists'),          type: 'success' },
            { key: 'total_shots',           label: t('components.compareSeasons.totalShots'),      type: 'number'  },
            { key: 'total_shots_on_target', label: t('components.compareSeasons.shotsOnTarget'),  type: 'success' },
            { key: 'shot_accuracy_pct',     label: t('components.compareSeasons.shotAccuracy'),  type: 'success' },
        ]
    },
    passing: {
        title: t('components.compareSeasons.passing'),
        icon: 'openmoji:bullseye',
        metrics: [
            { key: 'total_passes',     label: t('components.compareSeasons.totalPasses'), type: 'number'  },
            { key: 'total_key_passes', label: t('components.compareSeasons.keyPasses'),   type: 'success' },
        ]
    },
    duels: {
        title: t('components.compareSeasons.duels'),
        icon: 'openmoji:collision',
        metrics: [
            { key: 'total_duels',              label: t('components.compareSeasons.totalDuels'),         type: 'number'  },
            { key: 'total_duels_won',          label: t('components.compareSeasons.duelsWon'),           type: 'success' },
            { key: 'duel_win_rate_pct',        label: t('components.compareSeasons.duelWinRate'),     type: 'success' },
            { key: 'total_dribbles_attempts',  label: t('components.compareSeasons.dribbleAttempts'),    type: 'number'  },
            { key: 'total_dribbles_success',   label: t('components.compareSeasons.dribblesSuccessful'), type: 'success' },
            { key: 'dribble_success_rate_pct', label: t('components.compareSeasons.dribbleSuccessRate'),   type: 'success' },
        ]
    },
    defensive: {
        title: t('components.compareSeasons.defensive'),
        icon: 'openmoji:shield',
        metrics: [
            { key: 'total_tackles', label: t('components.compareSeasons.totalTackles'), type: 'success' },
        ]
    },
    discipline: {
        title: t('components.compareSeasons.discipline'),
        icon: 'openmoji:warning',
        metrics: [
            { key: 'total_yellow_cards',    label: t('components.compareSeasons.yellowCards'),    type: 'warning', lowerIsBetter: true },
            { key: 'total_red_cards',       label: t('components.compareSeasons.redCards'),       type: 'danger',  lowerIsBetter: true },
            { key: 'total_fouls_committed', label: t('components.compareSeasons.foulsCommitted'), type: 'danger',  lowerIsBetter: true },
            { key: 'total_fouls_drawn',     label: t('components.compareSeasons.foulsDrawn'),     type: 'success' },
        ]
    },
    penalties: {
        title: t('components.compareSeasons.penalties'),
        icon: 'openmoji:bullseye',
        metrics: [
            { key: 'total_penalties_scored', label: t('components.compareSeasons.penaltiesScored'), type: 'success' },
            { key: 'total_penalties_missed', label: t('components.compareSeasons.penaltiesMissed'), type: 'danger',  lowerIsBetter: true },
        ]
    },
}));

function isWinner(val, opponentVal, lowerIsBetter = false) {
    const num1 = parseFloat(val) || 0;
    const num2 = parseFloat(opponentVal) || 0;
    if (num1 === num2) return false;
    return lowerIsBetter ? num1 < num2 : num1 > num2;
}

const overallWinner = computed(() => {
    if (competitors.value.length !== 2) return null;
    const [c1, c2] = competitors.value;
    let firstWins = 0;
    let secondWins = 0;

    Object.values(metricGroups).forEach(group => {
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
        firstWins, secondWins, total,
        winner:    firstWins > secondWins ? 'first' : secondWins > firstWins ? 'second' : 'tie',
        firstName:  props.firstName,
        secondName: props.secondName,
        firstPct:   total > 0 ? Math.round((firstWins  / total) * 100) : 50,
        secondPct:  total > 0 ? Math.round((secondWins / total) * 100) : 50,
    };
});

onMounted(() => {
    if (comparing.value) {
        const offset = 80;
        const top = comparing.value.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
    }
});
</script>

<template>
<div v-if="competitors.length === 2" class="comparison-wrapper">
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
                <Icon icon="openmoji:handshake" class="icon-md" />
                <span>It's a Tie!</span>
            </span>
            <span v-else class="winner-title">
                <Icon icon="openmoji:crown" class="icon-lg" />
                <span>Overall Winner: </span>
                <strong>{{ overallWinner.winner === 'first' ? overallWinner.firstName : overallWinner.secondName }}</strong>
            </span>
            <span class="winner-subtitle">
                {{ overallWinner.firstWins }}W vs {{ overallWinner.secondWins }}W
                out of {{ overallWinner.total }} metrics
            </span>
        </div>
        <div class="winner-bar-track">
            <div class="winner-bar-fill first-fill" :style="{ width: overallWinner.firstPct + '%' }">
                <span v-if="overallWinner.firstPct > 15" class="bar-label">
                    {{ overallWinner.firstName }} {{ overallWinner.firstPct }}%
                </span>
            </div>
            <div class="winner-bar-fill second-fill" :style="{ width: overallWinner.secondPct + '%' }">
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
                    <Icon :icon="group.icon" class="icon-lg" />
                </span>
                {{ group.title }}
            </h3>
            <div class="comparison-grid">
                <div v-for="metric in group.metrics" :key="metric.key" class="metric-row">
                    <div
                        class="metric-value first"
                        :class="[metric.type, { winner: isWinner(competitors[0].rawStats[metric.key], competitors[1].rawStats[metric.key], metric.lowerIsBetter) }]"
                    >
                        <span class="value">{{ competitors[0].rawStats[metric.key] ?? '-' }}</span>
                    </div>
                    <div class="metric-label">{{ metric.label }}</div>
                    <div
                        class="metric-value second"
                        :class="[metric.type, { winner: isWinner(competitors[1].rawStats[metric.key], competitors[0].rawStats[metric.key], metric.lowerIsBetter) }]"
                    >
                        <span class="value">{{ competitors[1].rawStats[metric.key] ?? '-' }}</span>
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