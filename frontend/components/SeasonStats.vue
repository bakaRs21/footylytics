<script setup>
import { Icon } from '@iconify/vue';

const props = defineProps({
    data: {
        type: Object,
        required: true,
    }
})
</script>

<template>
<div class="season-stats-wrapper">
    <div class="season-header">
        <div class="season-title">
            <Icon icon="material-symbols:trophy-outline" class="header-icon" />
            <span>Season {{ props.data.season_id }} Overview</span>
        </div>
        <div class="season-meta">
            <span class="meta-pill">
                <Icon icon="material-symbols:person-outline" />
                {{ props.data.total_players.toLocaleString() }} Players
            </span>
            <span class="meta-pill">
                <Icon icon="material-symbols:event-note-outline" />
                {{ props.data.total_player_appearances.toLocaleString() }} Appearances
            </span>
        </div>
    </div>
    <div class="row">
        <div class="row-card">
            <Icon icon="material-symbols:sports-soccer" class="icon" />
            <span class="value">{{ props.data.total_goals.toLocaleString() }}</span>
            <span class="label">Goals</span>
        </div>
        <div class="row-card">
            <Icon icon="material-symbols:back-hand-outline" class="icon" />
            <span class="value">{{ props.data.total_assists.toLocaleString() }}</span>
            <span class="label">Assists</span>
        </div>
        <div class="row-card">
            <Icon icon="material-symbols:arrow-circle-right-outline" class="icon" />
            <span class="value">{{ props.data.total_shots.toLocaleString() }}</span>
            <span class="label">Total Shots</span>
        </div>
        <div class="row-card">
            <Icon icon="material-symbols:send-outline" class="icon" />
            <span class="value">{{ props.data.total_passes.toLocaleString() }}</span>
            <span class="label">Total Passes</span>
        </div>
    </div>
    <div class="detail-grid">
        <div class="card-primary">
            <h3 class="card-title">
                <Icon icon="material-symbols:sports-score" class="card-title-icon" />
                Shooting
            </h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <Icon icon="material-symbols:arrow-circle-right-outline" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_shots.toLocaleString() }}</span>
                        <span class="stat-label">Total Shots</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Icon icon="material-symbols:check-box-outline" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_shots_on_target.toLocaleString() }}</span>
                        <span class="stat-label">Shots on Target</span>
                    </div>
                </div>
                <div class="progress-wrap">
                    <div class="progress-header">
                        <span class="stat-label">Shot Accuracy</span>
                        <span class="stat-label">{{ props.data.shot_accuracy_pct }}%</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill" :style="{ width: props.data.shot_accuracy_pct + '%' }"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-primary">
            <h3 class="card-title">
                <Icon icon="material-symbols:multiple-stop" class="card-title-icon" />
                Passing
            </h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <Icon icon="material-symbols:send-outline" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_passes.toLocaleString() }}</span>
                        <span class="stat-label">Total Passes</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Icon icon="material-symbols:key-outline" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_key_passes.toLocaleString() }}</span>
                        <span class="stat-label">Key Passes</span>
                    </div>
                </div>
                <div class="progress-wrap">
                    <div class="progress-header">
                        <span class="stat-label">Key Pass Rate</span>
                        <span class="stat-label">{{ ((props.data.total_key_passes / props.data.total_passes) * 100).toFixed(2) }}%</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill" :style="{ width: ((props.data.total_key_passes / props.data.total_passes) * 100).toFixed(2) + '%' }"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-primary">
            <h3 class="card-title">
                <Icon icon="material-symbols:sync-alt" class="card-title-icon" />
                Duels & Dribbles
            </h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <Icon icon="material-symbols:groups-outline" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_duels.toLocaleString() }}</span>
                        <span class="stat-label">Total Duels</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Icon icon="material-symbols:trophy-outline" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_duels_won.toLocaleString() }}</span>
                        <span class="stat-label">Duels Won</span>
                    </div>
                </div>
                <div class="progress-wrap">
                    <div class="progress-header">
                        <span class="stat-label">Duel Win Rate</span>
                        <span class="stat-label">{{ props.data.duel_win_rate_pct }}%</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill" :style="{ width: props.data.duel_win_rate_pct + '%' }"></div>
                    </div>
                </div>
                <div class="card-stat">
                    <Icon icon="material-symbols:directions-run" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_dribbles_attempts.toLocaleString() }}</span>
                        <span class="stat-label">Dribble Attempts</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Icon icon="material-symbols:sprint" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_dribbles_success.toLocaleString() }}</span>
                        <span class="stat-label">Dribbles Successful</span>
                    </div>
                </div>
                <div class="progress-wrap">
                    <div class="progress-header">
                        <span class="stat-label">Dribble Success Rate</span>
                        <span class="stat-label">{{ props.data.dribble_success_rate_pct }}%</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill" :style="{ width: props.data.dribble_success_rate_pct + '%' }"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-primary">
            <h3 class="card-title">
                <Icon icon="material-symbols:gavel" class="card-title-icon" />
                Discipline
            </h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <Icon icon="material-symbols:rectangle-outline" class="stat-icon text-yellow" />
                    <div class="flex-col">
                        <span class="stat-value text-yellow">{{ props.data.total_yellow_cards.toLocaleString() }}</span>
                        <span class="stat-label">Yellow Cards</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Icon icon="material-symbols:rectangle-outline" class="stat-icon text-red" />
                    <div class="flex-col">
                        <span class="stat-value text-red">{{ props.data.total_red_cards }}</span>
                        <span class="stat-label">Red Cards</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Icon icon="material-symbols:back-hand-outline" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_fouls_committed.toLocaleString() }}</span>
                        <span class="stat-label">Fouls Committed</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Icon icon="material-symbols:front-hand-outline" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_fouls_drawn.toLocaleString() }}</span>
                        <span class="stat-label">Fouls Drawn</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-primary">
            <h3 class="card-title">
                <Icon icon="material-symbols:radio-button-checked-outline" class="card-title-icon" />
                Penalties
            </h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <Icon icon="material-symbols:check-circle-outline" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_penalties_scored }}</span>
                        <span class="stat-label">Penalties Scored</span>
                    </div>
                </div>
                <div class="card-stat">
                    <Icon icon="material-symbols:cancel-outline" class="stat-icon text-red" />
                    <div class="flex-col">
                        <span class="stat-value text-red">{{ props.data.total_penalties_missed }}</span>
                        <span class="stat-label">Penalties Missed</span>
                    </div>
                </div>
                <div class="progress-wrap">
                    <div class="progress-header">
                        <span class="stat-label">Conversion Rate</span>
                        <span class="stat-label">
                            {{ ((props.data.total_penalties_scored / (props.data.total_penalties_scored + props.data.total_penalties_missed)) * 100).toFixed(1) }}%
                        </span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill"
                            :style="{ width: ((props.data.total_penalties_scored / (props.data.total_penalties_scored + props.data.total_penalties_missed)) * 100).toFixed(1) + '%' }">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-primary">
            <h3 class="card-title">
                <Icon icon="material-symbols:shield-outline" class="card-title-icon" />
                Defense
            </h3>
            <div class="card-content flex-col-gap">
                <div class="card-stat">
                    <Icon icon="material-symbols:block" class="stat-icon" />
                    <div class="flex-col">
                        <span class="stat-value">{{ props.data.total_tackles.toLocaleString() }}</span>
                        <span class="stat-label">Total Tackles</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
.season-stats-wrapper {
    width: 100%;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}
.season-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.75rem;
    padding: 0 0.25rem;
}
.season-title {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 1.3rem;
    font-weight: 700;
    color: #e2e8f0;
}
.season-meta {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
}


.header-icon {
    font-size: 1.4rem;
    color: rgba(61, 214, 140, 0.9);
}

.row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 0.75rem;
}
.row-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.2rem;
    padding: 1rem 0.75rem;
    background: #16162e59;
    border: 1px solid rgba(61, 214, 140, 0.12);
    border-radius: 10px;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    text-align: center;
}
.row-card:hover {
    transform: translateY(-3px);
    border-color: rgba(61, 214, 140, 0.35);
    box-shadow: 0 14px 32px rgba(0, 0, 0, 0.2);
}

.icon {
    font-size: 1.5rem;
    color: #94a3b8;
    margin-bottom: 0.15rem;
}

.value {
    font-size: 1.6rem;
    font-weight: 800;
    color: #e2e8f0;
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
}

.label {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
}

.card-title {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.9rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid rgba(61, 214, 140, 0.2);
    color: #e2e8f0;
}
.card-title-icon {
    font-size: 1.1rem;
    color: rgba(61, 214, 140, 0.9);
    flex-shrink: 0;
}

.stat-icon {
    font-size: 1.35rem;
    color: #94a3b8;
    flex-shrink: 0;
}

.progress-wrap {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    padding: 0.4rem 0.25rem 0.2rem;
}
.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stat-icon.text-red { color: #ef4444; }
.stat-icon.text-yellow { color: #eab308; }

@media (max-width: 840px) {
    .season-stats-wrapper { padding: 0.75rem; }
    .detail-grid { grid-template-columns: 1fr; }
    .kpi-row { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 480px) {
    .season-header { flex-direction: column; align-items: flex-start; }
    .kpi-row { grid-template-columns: repeat(2, 1fr); }
}
</style>