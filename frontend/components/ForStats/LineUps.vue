<script setup>
import { Icon } from '@iconify/vue'


const props = defineProps({
    data: {
        type: Object,
        required: true
    }
})
const FORMATION_RULES = {
    '3': {
        lines: [
            { count: 3, roles: ["Center Back", "Center Back", "Center Back"] }
        ]
    },
    '4': {
        lines: [
            { count: 4, roles: ["Left Back", "Center Back", "Center Back", "Right Back"] }
        ]
    },
    '5': {
        lines: [
            { count: 5, roles: ["Left Wing Back", "Left Center Back", "Center Back", "Right Center Back", "Right Wing Back"] }
        ]
    },

    '1-midfield': {
        lines: [
            { count: 1, roles: ["Defensive Midfielder"] }
        ]
    },
    '2-midfield': {
        lines: [
            { count: 2, roles: ["Defensive Midfielder", "Defensive Midfielder"] }
        ]
    },
    '3-midfield': {
        lines: [
            { count: 3, roles: ["Central Midfielder", "Central Midfielder", "Central Midfielder"] }
        ]
    },
    '4-midfield': {
        lines: [
            { count: 4, roles: ['Left Midfielder', 'Central Midfielder', 'Central Midfielder', 'Right Midfielder']}
        ]
    },
    '5-midfield': {
        lines: [
            { count: 5, roles: ['Left Wing', 'Defensive Mid', 'Central Mid', 'Defensive Mid', 'Right Wing']}
        ]
    },

    '1-attack': {
        lines: [
            { count: 1, roles: ['Striker'] }
        ]
    },
    '2-attack': {
        lines: [
            { count: 2, roles: ['Left Forward', 'Right Forward'] }
        ]
    },
    '3-attack': {
        lines: [
            { count: 3, roles: ['Left Wing', 'Striker', 'Right Wing'] }
        ]
    }
}

const parseFormation = computed(() => {
    const splitted = props.data.formation.split('-')
    const positions = [
        { line: 'Goalkeeper', roles: ['Goalkeeper'], count: 1 },
    ]

    const defenders = parseInt(splitted[0])
    positions.push({
        line: 'Defenders',
        roles: FORMATION_RULES[`${defenders}`].lines[0].roles,
        count: defenders
    })

    if (splitted.length === 3) {
        const midfielders = parseInt(splitted[1])
        positions.push({
            line: 'Midfielders',
            roles: FORMATION_RULES[`${midfielders}-midfield`].lines[0].roles,
            count: midfielders
        })
    } else if (splitted.length === 4) {
        const defensive_mids = parseInt(splitted[1])
        const offensive_mids = parseInt(splitted[2])

        positions.push({
            line: 'Defensive Midfielders',
            roles: FORMATION_RULES[`${defensive_mids}-midfield`].lines[0].roles,
            count: defensive_mids
        })
        positions.push({
            line: 'Offensive Midfielders',
            roles: FORMATION_RULES[`${offensive_mids}-midfield`].lines[0].roles,
            count: offensive_mids
        })
    }

    const attackers = parseInt(splitted[splitted.length - 1])
    positions.push({
        line: 'Attackers',
        roles: FORMATION_RULES[`${attackers}-attack`].lines[0].roles,
        count: attackers
    })
    return positions
})

</script>
<template>
<div class="formation-container">
    <div class="formation-wrapper">
        <div v-for="(line, index) in parseFormation" :key="index" class="formation-line">
            <div class="line-label">
                {{ line.line }}
            </div>
            <div class="players-row">
                <div v-for="player in line.count" :key="player" class="player-dot">
                    <div class="tooltip" :data-tooltip="line.roles[player - 1]">
                        <div class="player-icon">
                            <Icon icon="mdi:soccer" />
                        </div>
                    </div> 
                </div>
            </div>
        </div>
    </div>
    <div class="formation-legend">
      <h4>Position Breakdown</h4>
      <div v-for="(line, index) in parseFormation"  :key="index"  class="legend-item">
        <span class="legend-count">{{ line.count }}</span>
        <span class="legend-text">{{ line.line }}: {{ line.roles.join(', ') }}</span>
      </div>
    </div>
</div>
</template>
<style scoped>
.formation-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 1.5rem;
  background: #1a1a1a;
  border-radius: 12px;
}

.formation-wrapper {
  background: linear-gradient(180deg, #2d5016 0%, #1a3d0a 100%);
  border-radius: 8px;
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column-reverse;
  gap: 1.5rem;
  min-height: 400px;
  justify-content: space-evenly;
  border: 2px solid #4a4a4a;
}

.formation-line {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.line-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  background: rgba(0, 0, 0, 0.5);
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
}

.players-row {
  display: flex;
  justify-content: center;
  gap: 1rem;
  width: 100%;
}

.player-dot {
  width: 40px;
  height: 40px;
  background: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  border: 2px solid #333;
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
  
  background: rgba(0, 0, 0, 0.301);
  color: white;
  padding: 8px 10px;
  border-radius: 10px;
  font-size: 12px;
  white-space: nowrap;

  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
}
.tooltip:hover::after {
  opacity: 1;
}

.role-description {
  font-size: 0.75rem;
  color: #cccccc;
  text-align: center;
  max-width: 200px;
}

.formation-legend {
  background: #333333;
  padding: 1.5rem;
  border-radius: 8px;
}

.formation-legend h4 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  color: #ffffff;
}

.legend-item {
  display: flex;
  gap: 1rem;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: #2a2a2a;
  border-radius: 6px;
  align-items: center;
}

.legend-count {
  background: #4CAF50;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.legend-text {
  color: #e0e0e0;
  font-size: 0.75rem;
}
</style>