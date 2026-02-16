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

const lineups = computed(() => {
    if (!newStats.value.lineups) return null;
    try {
        const formatted = newStats.value.lineups.replace(/'/g, '"');
        return JSON.parse(formatted);
    } catch (e) {
        console.error('Failed to parse lineups:', e);
        return null;
    }
});

const formArray = computed(() => {
    if (!newStats.value.form) return null;
    return newStats.value.form.split('');
});
const activeIndex = ref(null);
const toggleLineUp = (index) => {
    activeIndex.value = activeIndex.value === index ? null : index;
}

const showMetricOptions = ref(false);
const metric_options = () => {
    showMetricOptions.value = !showMetricOptions.value;
}
</script>

<template>
<div class="dashboard-wrapper">
    <h2 class="dashboard-title">Team Statistics</h2>
    <div class="dashboard-grid">
        <div class="card lineups-card">
            <h3 class="card-title">Formations</h3>
            <div v-if="lineups" class="lineups-content">
                <div v-for="(lineup, index) in lineups" :key="index" class="lineup-wrapper">
                    <div class="lineup-item" @click="toggleLineUp(index)">
                        <span class="formation">{{ lineup.formation }}</span>
                        <span class="played-count">{{ lineup.played }} matches</span>
                        <span class="lineup-arrow"  :class="{ 'arrow-rotated': activeIndex === index }">
                            <SmallArrowDown />
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
                    <Ball class="goal-icon" />
                    <div class="goal-details">
                        <span class="goal-value">{{ newStats.total_goals_scored }}</span>
                        <span class="goal-label">Goals Scored</span>
                    </div>
                </div>
                <div class="goal-stat">
                    <Goal class="goal-icon" />
                    <div class="goal-details">
                        <span class="goal-value">{{ newStats.total_goals_conceded }}</span>
                        <span class="goal-label">Goals Conceded</span>
                    </div>
                </div>
                <div class="goal-stat">
                    <Shield class="goal-icon" />
                    <div class="goal-details">
                        <span class="goal-value">{{ newStats.total_clean_sheets }}</span>
                        <span class="goal-label">Clean Sheets</span>
                    </div>
                </div>
                <div class="goal-stat">
                    <XMark class="goal-icon" />
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
                    <span class="streak-icon win">📈</span>
                    <div class="streak-details">
                        <span class="streak-value">{{ newStats.biggest_win_streak }}</span>
                        <span class="streak-label">Biggest Win Streak</span>
                    </div>
                </div>
                <div class="streak-item">
                    <span class="streak-icon draw">➖</span>
                    <div class="streak-details">
                        <span class="streak-value">{{ newStats.biggest_draw_streak }}</span>
                        <span class="streak-label">Biggest Draw Streak</span>
                    </div>
                </div>
                <div class="streak-item">
                    <span class="streak-icon lose">📉</span>
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
    <div class="metrics">
        <div>
            <h2 class="dashboard-title title-with-arrows tooltip" data-tooltip="Show metric options to be selected" >
                <ArrowDown class="arrow" @click="metric_options()" /> 
                Metrics 
                <ArrowDown class="arrow" @click="metric_options()"/>
            </h2>
        </div>
        <div v-if="showMetricOptions" class="metric-options">
            <p>Metric options will be available in a future update!</p>
        </div>
    </div>
</div>
</template>

<style scoped>
.dashboard-wrapper {
    width: 100%;
    padding: 2rem;
    background: #1a1a1a9c;
    min-height: 100vh;
    margin-top: 20px;
    border-top: solid 12px #1f1d2552;
}


.dashboard-title {
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
}
.title-with-arrows {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}


.tooltip {
    position: relative;
    cursor: help;
}
.tooltip::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: -35px;
  left: 50%;
  transform: translateX(-50%);
  
  background: #0c0c0c;
  color: white;
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 16px;
  white-space: nowrap;

  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
}
.tooltip:hover::after {
  opacity: 1;
}


.arrow {
    margin-left: 0.5rem;
    margin-right: 0.5rem;
    cursor: pointer;
}


.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    max-width: 1400px;
    margin: 0 auto;
}



.card {
    background: #2a2a2a;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.4);
}
.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid #3a3a3a;
}



.lineups-card {
    grid-column: span 1;
}
.lineups-content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.lineup-wrapper { 
    margin-bottom: 0.5rem;
}
.lineup-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: #333333;
    border-radius: 8px;
    transition: background 0.2s;
    cursor: pointer;
}
.lineup-item:hover {
    background: #3d3d3d;
}
.formation {
    font-size: 1.1rem;
    font-weight: 600;
    color: #4ade80;
}
.played-count {
    font-size: 0.9rem;
    color: #a0a0a0;
}
.lineup-arrow {
    display: flex;
    align-items: center;
    transition: transform 0.3s ease;
    cursor: pointer;
}
.arrow-rotated {
    transform: rotate(180deg);
}
.lineup-details {
    padding: 0.75rem;
    background: #3a3a3a;
    border-radius: 8px;
    animation: slideDown 0.3s ease-out;
}
.no-data {
    text-align: center;
    padding: 2rem;
    color: #666;
}

@keyframes slideDown {
    from {
        opacity: 0;
        max-height: 0;
        padding-top: 0;
        padding-bottom: 0;
    }
    to {
        opacity: 1;
        max-height: 500px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
}



.matches-card {
    grid-column: span 1;
}
.matches-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}
.stat-large {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    background: #333333;
    border-radius: 8px;
}
.stat-value {
    font-size: 3rem;
    font-weight: 700;
    color: #4ade80;
}
.stat-label {
    font-size: 0.9rem;
    color: #a0a0a0;
    text-transform: uppercase;
    letter-spacing: 1px;
}



.result-breakdown {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
}
.result-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    background: #333333;
    border-radius: 8px;
}
.result-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}
.result-icon.win {
    background: #22c55e;
    color: #fff;
}
.result-icon.draw {
    background: #eab308;
    color: #000;
}
.result-icon.lose {
    background: #ef4444;
    color: #fff;
}
.result-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 0.25rem;
}
.result-label {
    font-size: 0.85rem;
    color: #a0a0a0;
}




.goals-card {
    grid-column: span 1;
}
.goals-content {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
}
.goal-stat {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.9rem;
    padding: 0.75rem;
    background: #333333;
    border-radius: 8px;
}
.goal-icon {
    font-size: 2rem;
}
.goal-details {
    display: flex;
    flex-direction: column;
}
.goal-value {
    font-size: 1.5rem;
    font-weight: 600;
}
.goal-label {
    font-size: 0.85rem;
    color: #a0a0a0;
}



.penalties-section {
    margin-top: 0.2rem;
    border-top: 1px solid #3a3a3a;
}



.subsection-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #a0a0a0;
    margin-bottom: 0.75rem;
    margin-top: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}



.penalty-stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
}
.penalty-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.55rem;
    background: #3a3a3a;
    border-radius: 8px;
}
.penalty-value {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
}
.penalty-value.success {
    color: #22c55e;
}
.penalty-value.missed {
    color: #ef4444;
}
.penalty-label {
    font-size: 0.85rem;
    color: #a0a0a0;
}




.streaks-card {
    grid-column: span 3;
}
.streaks-content {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.streak-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.9rem;
    background: #333333;
    border-radius: 8px;
}
.streak-icon {
    font-size: 2rem;
}
.streak-details {
    display: flex;
    flex-direction: column;
}
.streak-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: #ffffff;
}
.streak-label {
    font-size: 0.85rem;
    color: #a0a0a0;
}



.form-section {
    padding-top: 1rem;
    border-top: 1px solid #3a3a3a;
}
.form-display {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 0.5rem;
}
.form-badge {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.9rem;
    cursor: default;
    transition: transform 0.2s;
}

.form-badge:hover {
    transform: scale(1.15);
}

.form-badge.w {
    background: #22c55e;
}

.form-badge.d {
    background: #eab308;
}

.form-badge.l {
    background: #ef4444;
}

.form-note {
    font-size: 0.75rem;
    color: #666;
    font-style: italic;
}



@media (max-width: 840px) {
    .dashboard-wrapper {
        padding: 1rem;
    }
    
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
    
    .result-breakdown {
        grid-template-columns: 1fr;
    }
}
</style>
