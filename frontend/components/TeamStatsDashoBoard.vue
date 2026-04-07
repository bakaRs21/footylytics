<script setup>
import { Icon } from '@iconify/vue';
import { computed, watch } from 'vue';

const stats = defineModel({
    type: Object ?? null,
    required: true,
    default: {},
})
const showStats = ref(false);
const dashboard = ref(null);

const newStats = computed(() =>  {
    if (!stats.value) return {};
    return Object.fromEntries(Object.entries(stats.value).filter(([_, v]) => v != null))
});

const lineups = computed(() => {
    if (!newStats.value) return null;
    if (!newStats.value.lineups) return null;
    try {
        const formatted = newStats.value.lineups.replace(/'/g, '"');
        return JSON.parse(formatted);
    } catch (e) {
        return null;
    }
});

const formArray = computed(() => {
    if (!newStats.value) return null;
    if (!newStats.value.form) return null;
    return newStats.value.form.split('');
});
const activeIndex = ref(null);
const toggleLineUp = (index) => {
    activeIndex.value = activeIndex.value === index ? null : index;
}

watch(() => stats.value, (newVal) => {
    if (newVal) {
        showStats.value = true;
        scrollToDashboard();
    } else {
        showStats.value = false;
    }
})
watch(() => showStats.value, async (newVal) => {
    if (newVal) {
        await scrollToDashboard();
    }
})
async function scrollToDashboard() {
    if (showStats.value) {
        await nextTick();
        const offset = 200
        const top = dashboard.value.getBoundingClientRect().top + window.scrollY - offset
        window.scrollTo({ top, behavior: 'smooth' })
    }
}
function clearStats() {
    stats.value = null;
}
</script>

<template>
<div class="tsd-wrapper">
    <div @click="showStats = !showStats" class="title-with-arrows tooltip" data-tooltip="Show metric options to be selected" >
        <Icon icon="mdi:chevron-down" />
        <h2 class="stats-h2" id="stats"> Team Statistics </h2>
        <Icon icon="mdi:chevron-down" />
    </div>
    <div v-if="showStats" class="dashboard-wrapper">
        <div class="dashboard-grid" ref="dashboard">
            <div class="card lineups-card">
                <h3 class="card-title">Formations</h3>
                <div v-if="lineups" class="lineups-content">
                    <div v-for="(lineup, index) in lineups" :key="index" class="lineup-wrapper">
                        <div class="lineup-item" @click="toggleLineUp(index)">
                            <span class="formation">{{ lineup.formation }}</span>
                            <span class="played-count">{{ lineup.played }} matches</span>
                            <span class="lineup-arrow"  :class="{ 'arrow-rotated': activeIndex === index }">
                                <Icon icon="mdi:chevron-down" />
                            </span>
                        </div>
                        <div v-if="activeIndex === index" class="lineup-details">
                            <LineUps :data="lineup" />
                        </div>
                    </div>
                </div>
                <div v-else class="no-data">
                    <p>No lineup data available</p>
                </div>
            </div>
            <div class="card matches-card">
                <h3 class="card-title">Matches Overview</h3>
                <div class="matches-content">
                    <div class="stat-large">
                        <span class="stat-value">{{ newStats.total_matches_played }}</span>
                        <span class="stat-label">Total Matches</span>
                    </div>
                    <div class="result-breakdown">
                        <div class="result-item">
                            <span class="result-icon win">W</span>
                            <span class="result-value">{{ newStats.total_wins }}</span>
                            <span class="result-label">Wins</span>
                        </div>
                        <div class="result-item">
                            <span class="result-icon draw">D</span>
                            <span class="result-value">{{ newStats.total_draws }}</span>
                            <span class="result-label">Draws</span>
                        </div>
                        <div class="result-item">
                            <span class="result-icon lose">L</span>
                            <span class="result-value">{{ newStats.total_losses }}</span>
                            <span class="result-label">Losses</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card goals-card">
                <h3 class="card-title">Goals & Performance</h3>
                <div class="goals-content">
                    <div class="goal-stat">
                        <Icon icon="mdi:target" class="goal-icon" />
                        <div class="goal-details">
                            <span class="goal-value">{{ newStats.total_goals_scored }}</span>
                            <span class="goal-label">Goals Scored</span>
                        </div>
                    </div>
                    <div class="goal-stat">
                        <Icon icon="mdi:target" class="goal-icon" />
                        <div class="goal-details">
                            <span class="goal-value">{{ newStats.total_goals_conceded }}</span>
                            <span class="goal-label">Goals Conceded</span>
                        </div>
                    </div>
                    <div class="goal-stat">
                        <Icon icon="mdi:shield" class="goal-icon" />
                        <div class="goal-details">
                            <span class="goal-value">{{ newStats.total_clean_sheets }}</span>
                            <span class="goal-label">Clean Sheets</span>
                        </div>
                    </div>
                    <div class="goal-stat">
                        <Icon icon="mdi:close" class="goal-icon" />
                        <div class="goal-details">
                            <span class="goal-value">{{ newStats.total_failed_to_score }}</span>
                            <span class="goal-label">Failed to Score</span>
                        </div>
                    </div>
                    <div class="penalties-section">
                        <h4 class="subsection-title">Penalties</h4>
                        <div class="penalty-stats">
                            <div class="penalty-item">
                                <span class="penalty-value success">{{ newStats.total_penalties_scored }}</span>
                                <span class="penalty-label">Scored</span>
                            </div>
                            <div class="penalty-item">
                                <span class="penalty-value missed">{{ newStats.total_penalties_missed }}</span>
                                <span class="penalty-label">Missed</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card streaks-card">
                <h3 class="card-title">Streaks</h3>
                <div class="streaks-content">
                    <div class="streak-item">
                        <span class="streak-icon win">
                            <Icon icon="openmoji:chart-increasing" />
                        </span>
                        <div class="streak-details">
                            <span class="streak-value">{{ newStats.biggest_win_streak }}</span>
                            <span class="streak-label">Biggest Win Streak</span>
                        </div>
                    </div>
                    <div class="streak-item">
                        <span class="streak-icon draw">
                            <Icon icon="mdi:minus" />
                        </span>
                        <div class="streak-details">
                            <span class="streak-value">{{ newStats.biggest_draw_streak }}</span>
                            <span class="streak-label">Biggest Draw Streak</span>
                        </div>
                    </div>
                    <div class="streak-item">
                        <span class="streak-icon lose">
                            <Icon icon="openmoji:chart-decreasing" />
                        </span>
                        <div class="streak-details">
                            <span class="streak-value">{{ newStats.biggest_lose_streak }}</span>
                            <span class="streak-label">Biggest Loss Streak</span>
                        </div>
                    </div>
                </div>
                <div v-if="formArray" class="form-section">
                    <h4 class="subsection-title">Team Form</h4>
                    <div class="form-display">
                        <div v-for="(result, index) in formArray" :key="index" :class="['form-badge', result.toLowerCase()]">
                            {{ result }}
                        </div>
                    </div>
                    <p class="form-note">Latest match played on the right</p>
                </div>
            </div>
        </div>
        <button class="eraseStatsButton" @click="clearStats">Clear Stats</button>
    </div>
</div>
</template>

<style scoped>
.tsd-wrapper {
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.281);
}
.dashboard-wrapper {
    width: 100%;
    margin-top: 10px;
}
.dashboard-title {
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.75rem;
}
.title-with-arrows {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1rem;
    max-width: 1400px;
    margin: 0 auto;
}

.tooltip { position: relative; cursor: help; }
.tooltip::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: -30px;
    left: 50%;
    transform: translateX(-50%);
    background: #0c0c0c;
    color: white;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 0.85rem;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
}
.tooltip:hover::after { opacity: 1; }
.arrow { margin: 0 0.5rem; cursor: pointer; }

.card {
    background: #16162e59;
    border: 1px solid rgba(61, 214, 140, 0.12);
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 10px rgba(0,0,0,0.4);
}
.card-title {
    font-size: 1rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #3a3a3a;
}
.no-data {
    text-align: center;
    padding: 1rem;
    color: #666;
    font-size: 0.85rem;
}

.stat-label, .result-label, .goal-label, .streak-label, .penalty-label {
    font-size: 0.8rem;
    color: #a0a0a0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.streaks-card { grid-column: span 3; }
.lineups-content { display: flex; flex-direction: column; gap: 0.5rem; }
.lineup-wrapper  { margin-bottom: 0.25rem; }
.lineup-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0.75rem;
    background: rgba(34, 32, 139, 0.199);
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
}
.lineup-item:hover { background: #284e2754; }
.formation { font-size: 1rem; font-weight: 600; color: #4ade80; }
.played-count { font-size: 0.8rem; color: #a0a0a0; }
.lineup-arrow { display: flex; align-items: center; transition: transform 0.3s ease; }
.arrow-rotated { transform: rotate(180deg); }
.lineup-details {
    padding: 0.5rem;
    background: #3a3a3a;
    border-radius: 6px;
    animation: slideDown 0.3s ease-out;
}
@keyframes slideDown {
    from { opacity: 0; max-height: 0; }
    to   { opacity: 1; max-height: 500px; }
}

.matches-content { display: flex; flex-direction: column; gap: 0.75rem; }
.stat-large {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.75rem;
    background: rgba(53, 50, 223, 0.199);
    border-radius: 6px;
}
.stat-value { font-size: 2rem; font-weight: 700; color: #4ade80; }
.result-breakdown {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
}
.result-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.6rem;
    background: rgba(34, 32, 139, 0.199);
    border-radius: 6px;
}
.result-icon {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 0.35rem;
}
.result-icon.win  { background: #22c55e; color: #fff; }
.result-icon.draw { background: #eab308; color: #000; }
.result-icon.lose { background: #ef4444; color: #fff; }
.result-value { font-size: 1.2rem; font-weight: 600; color: #fff; }

.goals-content { display: flex; flex-direction: column; gap: 0.5rem; }
.goal-stat {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 0.5rem;
    background: rgba(53, 50, 223, 0.199);
    border-radius: 6px;
}
.goal-icon   { font-size: 1.5rem; }
.goal-details { display: flex; flex-direction: column; }
.goal-value  { font-size: 1.2rem; font-weight: 600; }

.penalties-section {
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #3a3a3a;
}
.subsection-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #a0a0a0;
    margin: 0.5rem 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.penalty-stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
}
.penalty-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.4rem;
    background: rgba(34, 32, 139, 0.199);
    border-radius: 6px;
}
.penalty-value          { font-size: 1.2rem; font-weight: 600; margin-bottom: 0.2rem; }
.penalty-value.success  { color: #22c55e; }
.penalty-value.missed   { color: #ef4444; }

.streaks-content {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}
.streak-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0.9rem;
    background: rgba(34, 32, 139, 0.199);
    border-radius: 6px;
}
.streak-icon    { font-size: 1.5rem; }
.streak-details { display: flex; flex-direction: column; }
.streak-value   { font-size: 1.2rem; font-weight: 600; color: #fff; }

.form-section {
    padding-top: 0.75rem;
    border-top: 1px solid #3a3a3a;
}
.form-display {
    display: flex;
    gap: 0.3rem;
    flex-wrap: wrap;
    margin-bottom: 0.35rem;
}
.form-badge {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.75rem;
    cursor: default;
    transition: transform 0.2s;
}
.form-badge:hover { transform: scale(1.15); }
.form-badge.w { background: #22c55e; }
.form-badge.d { background: #eab308; }
.form-badge.l { background: #ef4444; }
.form-note {
    font-size: 0.7rem;
    color: #666;
    font-style: italic;
}

@media (max-width: 840px) {
    .dashboard-wrapper { padding: 0.75rem; }
    .dashboard-grid { grid-template-columns: 1fr; }
    .result-breakdown { grid-template-columns: 1fr; }
    .streaks-card { grid-column: span 1; }
}
</style>