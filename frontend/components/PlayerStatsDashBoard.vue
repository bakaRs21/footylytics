<script setup>
import { computed } from 'vue';

const props = defineProps({
    stats: {
        type: Object,
        required: true,
    },
})

const newStats = computed(() => 
    Object.fromEntries(Object.entries(props.stats).filter(([_, v]) => v != null))
);
const showMetricOptions = ref(false);
const metric_options = () => {
    showMetricOptions.value = !showMetricOptions.value;
}
</script>

<template>
<div class="dashboard-wrapper">
    <h2 class="dashboard-title">Player Statistics</h2>
    <div class="dashboard-grid">
        <div class="card">
            <h3 class="card-title">Games</h3>
            <div 
            v-if="newStats.total_matches_played > 0 || newStats.total_minutes_played > 0 || newStats.rating !== null" 
            class="card-content">
                <div class="game-stat">
                    <span class="stat-value">{{ newStats.total_matches_played }}</span>
                    <span class="stat-label">Total Matches Played</span>
                </div>
                <div class="game-stat">
                    <span class="stat-value">{{ newStats.total_minutes_played }}</span>
                    <span class="stat-label">Total Minutes Played</span>
                </div>
                <div class="game-stat">
                    <span class="stat-value">{{ newStats.rating }}</span>
                    <span class="stat-label">Player Rating</span>
                </div>
            </div>
            <div v-else class="no-data">
                No game data available for this season.
            </div>
        </div>
        <div class="card">
            <h3 class="card-title">Goals & Assists</h3>
            <div 
            v-if="newStats.total_goals > 0 || newStats.total_assists > 0 || newStats.total_shots > 0 || newStats.shots_on_target > 0" 
            class="card-content">
                <div class="card-stat">
                    <Ball class="goal-icon" />
                    <div class="goal-details">
                        <span class="stat-value">{{ newStats.total_goals }}</span>
                        <span class="stat-label">Total Goals</span>
                    </div>
                </div>
                <div class="card-stat">
                    <XMark class="goal-icon" />
                    <div class="goal-details">
                        <span class="stat-value">{{ newStats.total_assists }}</span>
                        <span class="stat-label">Total Assists</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Goal class="goal-icon" />
                    <div class="goal-details">
                        <span class="stat-value">{{ newStats.total_shots }}</span>
                        <span class="stat-label">Total Shots</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Goal class="goal-icon" />
                    <div class="goal-details">
                        <span class="stat-value">{{ newStats.shots_on_target }}</span>
                        <span class="stat-label">Shots on Target</span>
                    </div>
                </div>
            </div>
            <div v-else class="no-data">
                No goal/shot data available for this season.
            </div>
        </div>
        <div class="card">
            <h3 class="card-title">Defensive Stats</h3>
            <div v-if="newStats.total_tackles > 0 || newStats.tackles_blocks > 0 || newStats.tackles_interceptions > 0" class="card-content">
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.total_tackles }}</span>
                    <span class="stat-label">Total Tackles</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.tackles_blocks }}</span>
                    <span class="stat-label">Blocks</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.tackles_interceptions }}</span>
                    <span class="stat-label">Tackles & Interceptions</span>
                </div>
            </div>
            <div v-else class="no-data">
                No defensive data available for this season.
            </div>
        </div>
        <div class="card">
            <h3 class="card-title">Passing Stats</h3>
            <div v-if="newStats.total_passes > 0 || newStats.key_passes > 0" class="card-content">
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.total_passes }}</span>
                    <span class="stat-label">Total Passes</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.key_passes }}</span>
                    <span class="stat-label">Key Passes</span>
                </div>
            </div>
            <div v-else class="no-data">
                No passing data available for this season.
            </div>
        </div>
        <div class="card">
            <h3 class="card-title">Duels & Dribbles</h3>
            <div v-if="newStats.total_duels > 0 || newStats.duels_won > 0 || newStats.dribbles_success > 0 || newStats.dribbles_attempts > 0" class="card-content">
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
            <div v-else class="no-data">
                No duels/dribbles data available for this season.
            </div>
        </div>
        <div class="card">
            <h3 class="card-title">Discipline</h3>
            <div v-if="newStats.red_cards > 0 || newStats.yellow_cards > 0 || newStats.fouls_committed > 0 || newStats.fouls_drawn > 0" class="card-content">
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.red_cards }}</span>
                    <span class="stat-label">Red Cards</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.yellow_cards }}</span>
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
            <div v-else class="no-data">
                No discipline data available for this season.
            </div>
        </div>
        <div class="card">
            <h3 class="card-title">Penalties</h3>
            <div v-if="newStats.penalties_scored > 0 || newStats.penalties_missed > 0 || newStats.penalties_won > 0" class="card-content">
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.penalties_scored }}</span>
                    <span class="stat-label">Penalties Scored</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.penalties_missed }}</span>
                    <span class="stat-label">Penalties Missed</span>
                </div>
                <div class="card-stat">
                    <span class="stat-value">{{ newStats.penalties_won }}</span>
                    <span class="stat-label">Penalties Won</span>
                </div>
            </div>
            <div v-else class="no-data">
                No penalty data available for this season.
            </div>
        </div>
        <div class="card">
            <h3 class="card-title">Goalkeeper Stats</h3>
            <div v-if="newStats.goals_conceded > 0 || newStats.saves > 0 || newStats.penalties_saved > 0" class="card-content">
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
            <div v-else class="no-data">
                No goalkeeper data available for the player in selected season.
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
.dashboard-wrapper {
    width: 100%;
    padding: 1rem;
    background: #1a1a1a9c;
    min-height: 100vh;
    margin-top: 10px;
    border-top: solid 6px #1f1d2552;
}
.dashboard-title {
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.75rem;
}
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    max-width: 1400px;
    margin: 0 auto;
}

.card {
    background: #2a2a2a;
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
.card-content { display: flex; flex-direction: column; gap: 0.5rem; }
.no-data {
    text-align: center;
    padding: 1rem;
    color: #666;
    font-size: 0.85rem;
}

.stat-value { font-size: 1.4rem; font-weight: 600; color: #4ade80; }
.stat-label {
    font-size: 0.78rem;
    color: #a0a0a0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.game-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.6rem;
    background: #333;
    border-radius: 6px;
}

.card-stat {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    padding: 0.5rem;
    background: #333;
    border-radius: 6px;
}
.goal-icon    { font-size: 1.4rem; }
.goal-details { display: flex; flex-direction: column; }

@media (max-width: 840px) {
    .dashboard-wrapper { padding: 0.75rem; }
    .dashboard-grid { grid-template-columns: 1fr; }
}
</style>