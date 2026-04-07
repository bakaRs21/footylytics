<script setup>
import { computed, ref, toRaw, onMounted } from 'vue';
import { Icon } from '@iconify/vue';

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

const metricGroups = {
    overview: {
        title: 'Season Overview',
        icon: 'openmoji:soccer-ball',
        metrics: [
            { key: 'total_players',            label: 'Total Players',  type: 'number' },
            { key: 'total_player_appearances', label: 'Appearances',    type: 'number' },
        ]
    },
    attacking: {
        title: 'Attacking',
        icon: 'openmoji:goal-net',
        metrics: [
            { key: 'total_goals',           label: 'Goals',            type: 'success' },
            { key: 'total_assists',         label: 'Assists',          type: 'success' },
            { key: 'total_shots',           label: 'Total Shots',      type: 'number'  },
            { key: 'total_shots_on_target', label: 'Shots on Target',  type: 'success' },
            { key: 'shot_accuracy_pct',     label: 'Shot Accuracy %',  type: 'success' },
        ]
    },
    passing: {
        title: 'Passing',
        icon: 'openmoji:bullseye',
        metrics: [
            { key: 'total_passes',     label: 'Total Passes', type: 'number'  },
            { key: 'total_key_passes', label: 'Key Passes',   type: 'success' },
        ]
    },
    duels: {
        title: 'Duels & Dribbles',
        icon: 'openmoji:collision',
        metrics: [
            { key: 'total_duels',              label: 'Total Duels',         type: 'number'  },
            { key: 'total_duels_won',          label: 'Duels Won',           type: 'success' },
            { key: 'duel_win_rate_pct',        label: 'Duel Win Rate %',     type: 'success' },
            { key: 'total_dribbles_attempts',  label: 'Dribble Attempts',    type: 'number'  },
            { key: 'total_dribbles_success',   label: 'Dribbles Successful', type: 'success' },
            { key: 'dribble_success_rate_pct', label: 'Dribble Success %',   type: 'success' },
        ]
    },
    defensive: {
        title: 'Defensive',
        icon: 'openmoji:shield',
        metrics: [
            { key: 'total_tackles', label: 'Tackles', type: 'success' },
        ]
    },
    discipline: {
        title: 'Discipline',
        icon: 'openmoji:warning',
        metrics: [
            { key: 'total_yellow_cards',    label: 'Yellow Cards',    type: 'warning', lowerIsBetter: true },
            { key: 'total_red_cards',       label: 'Red Cards',       type: 'danger',  lowerIsBetter: true },
            { key: 'total_fouls_committed', label: 'Fouls Committed', type: 'danger',  lowerIsBetter: true },
            { key: 'total_fouls_drawn',     label: 'Fouls Drawn',     type: 'success' },
        ]
    },
    penalties: {
        title: 'Penalties',
        icon: 'openmoji:bullseye',
        metrics: [
            { key: 'total_penalties_scored', label: 'Penalties Scored', type: 'success' },
            { key: 'total_penalties_missed', label: 'Penalties Missed', type: 'danger',  lowerIsBetter: true },
        ]
    },
};

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