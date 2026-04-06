<script setup>
import { Icon } from '@iconify/vue';
import { computed, watch } from 'vue';

const stats = defineModel({
    type: Object,
    required: true,
    default: null,
})
const showStats = ref(false);
const dashboard = ref(null);

const newStats = computed(() => 
    Object.fromEntries(Object.entries(stats.value).filter(([_, v]) => v != null))
);

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
function eraseStats() {
    stats.value = null
}
</script>

<template>
<div @click="showStats = !showStats" class="title-with-arrows tooltip" data-tooltip="Stats will be displayed here" >
    <Icon icon="mdi:chevron-down"/>
    <h2 class="stats-h2">Player Statistics</h2> 
    <Icon icon="mdi:chevron-down"/>
</div>
<div v-if="showStats" class="dashboard-wrapper">
    <div class="dashboard-grid grid-dashboard" ref="dashboard">
        <div class="card-primary"  v-if="newStats.total_matches_played > 0 || newStats.total_minutes_played > 0 || newStats.rating !== null">
            <h3 class="card-title">Games</h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat stat-details">
                    <span class="stat-value text-green">{{ newStats.total_matches_played }}</span>
                    <span class="stat-label">Total Matches Played</span>
                </div>
                <div class="card-stat stat-details">
                    <span class="stat-value">{{ newStats.total_minutes_played }}</span>
                    <span class="stat-label">Total Minutes Played</span>
                </div>
                <div class="card-stat stat-details">
                    <span class="stat-value">{{ newStats.rating }}</span>
                    <span class="stat-label">Player Rating</span>
                </div>
            </div>
        </div>
        <div class="card-primary" v-if="newStats.total_goals > 0 || newStats.total_assists > 0 || newStats.total_shots > 0 || newStats.shots_on_target > 0" >
            <h3 class="card-title">Goals & Assists</h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <Ball class="goal-icon" />
                    <div class="stat-details">
                        <span class="stat-value">{{ newStats.total_goals }}</span>
                        <span class="stat-label">Total Goals</span>
                    </div>
                </div>
                <div class="card-stat">
                    <XMark class="goal-icon" />
                    <div class="stat-details">
                        <span class="stat-value">{{ newStats.total_assists }}</span>
                        <span class="stat-label">Total Assists</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Goal class="goal-icon" />
                    <div class="stat-details">
                        <span class="stat-value">{{ newStats.total_shots }}</span>
                        <span class="stat-label">Total Shots</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Goal class="goal-icon" />
                    <div class="stat-details">
                        <span class="stat-value">{{ newStats.shots_on_target }}</span>
                        <span class="stat-label">Shots on Target</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-primary" v-if="newStats.total_tackles > 0 || newStats.tackles_blocks > 0 || newStats.tackles_interceptions > 0">
            <h3 class="card-title">Defensive Stats</h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat stat-details">
                    <span class="stat-value">{{ newStats.total_tackles }}</span>
                    <span class="stat-label">Total Tackles</span>
                </div>
                <div class="card-stat stat-details">
                    <span class="stat-value">{{ newStats.tackles_blocks }}</span>
                    <span class="stat-label">Blocks</span>
                </div>
                <div class="card-stat stat-details">
                    <span class="stat-value">{{ newStats.tackles_interceptions }}</span>
                    <span class="stat-label">Tackles & Interceptions</span>
                </div>
            </div>
        </div>
        <div class="card-primary" v-if="newStats.total_passes > 0 || newStats.key_passes > 0">
            <h3 class="card-title">Passing Stats</h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat stat-details">
                    <span class="stat-value">{{ newStats.total_passes }}</span>
                    <span class="stat-label">Total Passes</span>
                </div>
                <div class="card-stat stat-details">
                    <span class="stat-value">{{ newStats.key_passes }}</span>
                    <span class="stat-label">Key Passes</span>
                </div>
            </div>
        </div>
        <div class="card-primary" v-if="newStats.total_duels > 0 || newStats.duels_won > 0 || newStats.dribbles_success > 0 || newStats.dribbles_attempts > 0">
            <h3 class="card-title">Duels & Dribbles</h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.total_duels }}</span>
                    <span class="stat-label">Total Duels</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.duels_won }}</span>
                    <span class="stat-label">Duels Won</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.dribbles_success }}</span>
                    <span class="stat-label">Dribbles Successful</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.dribbles_attempts }}</span>
                    <span class="stat-label">Dribbles Attempts</span>
                </div>
            </div>
        </div>
        <div class="card-primary" v-if="newStats.red_cards > 0 || newStats.yellow_cards > 0 || newStats.fouls_committed > 0 || newStats.fouls_drawn > 0">
            <h3 class="card-title">Discipline</h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <span class="stat-value red">{{ newStats.red_cards }}</span>
                    <span class="stat-label">Red Cards</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value yellow">{{ newStats.yellow_cards }}</span>
                    <span class="stat-label">Yellow Cards</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.fouls_committed }}</span>
                    <span class="stat-label">Fouls Committed</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.fouls_drawn }}</span>
                    <span class="stat-label">Fouls Drawn</span>
                </div>
            </div>
        </div>
        <div class="card-primary" v-if="newStats.penalties_scored > 0 || newStats.penalties_missed > 0 || newStats.penalties_won > 0">
            <h3 class="card-title">Penalties</h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <span class="stat-value green">{{ newStats.penalties_scored }}</span>
                    <span class="stat-label">Penalties Scored</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value red">{{ newStats.penalties_missed }}</span>
                    <span class="stat-label">Penalties Missed</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.penalties_won }}</span>
                    <span class="stat-label">Penalties Won</span>
                </div>
            </div>
        </div>
        <div class="card-primary" v-if="newStats.goals_conceded > 0 || newStats.saves > 0 || newStats.penalties_saved > 0">
            <h3 class="card-title">Goalkeeper Stats</h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.goals_conceded }}</span>
                    <span class="stat-label">Goals Conceded</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.saves }}</span>
                    <span class="stat-label">Saves</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.penalties_saved }}</span>
                    <span class="stat-label">Penalties Saved</span>
                </div>
            </div>
        </div>
    </div>
    <button class="eraseStatsButton" @click="eraseStats()">Clear Stats</button>
</div>
</template>

<style scoped>
.dashboard-wrapper {
    width: 100%;
    padding: 1rem;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    max-width: 1400px;
    margin: 0 auto;
}


.no-data {
    text-align: center;
    padding: 1rem;
    color: #666;
    font-size: 0.85rem;
}

.red { color: #ef4444; }
.green { color: #22c55e; }
.yellow { color: #eab308; }


.goal-icon    { font-size: 1.35rem; color: #94a3b8; flex-shrink: 0; }
.stat-details { display: flex; flex-direction: column; min-width: 0; }

@media (max-width: 840px) {
    .dashboard-wrapper { padding: 0.75rem; }
    .dashboard-grid { grid-template-columns: 1fr; }
}
</style>