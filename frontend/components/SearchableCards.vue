<script setup>
import { ref, watch, computed } from 'vue';
import { Icon } from '@iconify/vue';
const config = useRuntimeConfig()
const filterOpen = ref(false)
const search = ref("");
const count = ref(0);

const props = defineProps({
    items: {
        type: Array,
        required: true
    },
    placeholder: {
        type: String,
        default: "Search..."
    },
    enableLinks: {
        type: Boolean,
        default: true
    },
    page: {
        type: String,
        required: true
    }
});

const availableSeasons = computed(() => {
    if (props.page === 'team' || props.page === 'player') {
        const allSeasons = props.items.flatMap(item => item.seasons)
        const uniqueSeasons = new Map(allSeasons.map(season => [season.season_id, season]))
        return Array.from(uniqueSeasons.values()).sort((a, b) => b.season_id - a.season_id).reverse()
    }
})
const availableTeams = computed(() => {
    if (props.page === 'player') {
        const allTeams = props.items.flatMap(player => player.teams)
        const uniqueTeams = new Map(allTeams.map(team => [team.team_id, team]))
        return Array.from(uniqueTeams.values())
    }
})


const selectedFilters = ref([])
const selectedSeasons = ref([])
const selectedTeams = ref([])
function filters(filterValue, type) {
    if (type === 'Seasons') {
        filtersToArray(selectedSeasons, filterValue)
    }
    if (type === 'Teams') {
        filtersToArray(selectedTeams, filterValue)
    }
}
function filtersToArray(array, filterValue) {
    if (array.value.includes(filterValue)) {
        array.value.splice(array.value.indexOf(filterValue), 1)
        selectedFilters.value.splice(selectedFilters.value.indexOf(filterValue), 1)
    } else {
        array.value.push(filterValue)
        selectedFilters.value.push(filterValue)
    }
}

const availableFilters = computed(() => {
    if (props.page === 'season') {
        return [{ title: 'No filters available', value: null }]
    }
    if (props.page === 'team') {
        return [{title: 'Seasons', value: availableSeasons.value.map(season => ({ name: season.season, value: season.season_id }))}];
    }
    if (props.page === 'player') {
        return [
            { title: 'Seasons', value: availableSeasons.value.map(season => ({ name: season.season, value: season.season_id })) },
            { title: "Teams", value: availableTeams.value.map(team => ({ name: team.name, value: team.team_id })) }
        ]
    }
})

const filteredItems = computed(() => {
    let items = props.items

    if (selectedSeasons.value.length > 0) {
        items = items.filter(item => 
            item.seasons?.some(season => selectedSeasons.value.includes(season.season_id))
        )
    }
    if (selectedTeams.value.length > 0) {
        items = items.filter(item => 
            item.teams?.some(team => selectedTeams.value.includes(team.team_id))
        )
    }

    if (!search.value.trim()) return items
    const searchLower = search.value.toLowerCase().trim()
    items = items.filter((item) => {
        if (props.page === 'season') { return (item.season ?? '').toLowerCase().includes(searchLower) } 
        else {
            return (item.name ?? '').toLowerCase().includes(searchLower)
        }
    })
    return items
});
watch(filteredItems, (newItems) => {
    count.value = newItems.length;
}, 
    { immediate: true }
);

const getItemId = (item) => {
  const key = `${props.page}_id`
  return item[key]
}
</script>
<template>
    <div class="panel">
        <div class="left">
            <pre>Count: {{ count }}</pre>
        </div>
        <button v-if="page !== 'season'" class="filter-toggle-btn" @click="filterOpen = !filterOpen">
            <Icon icon="mdi:filter-variant" />
            Filters
            <Icon icon="mdi:chevron-down" :class="{ 'chevron-open': filterOpen }" class="chevron" />
        </button>
        <div class="right">
            <input v-model="search" type="text" :placeholder="placeholder"/>
        </div>
    </div>
    <Transition name="filter-slide">
        <div v-if="filterOpen" class="filter-drawer">
            <div class="filter-group" v-for="filterGroup in availableFilters" :key="filterGroup.title">
                <span class="filter-label">{{ filterGroup.title }} :</span>
                <div class="filter-chips">
                    <button v-for="filter in filterGroup.value" :key="filter.value" 
                        class="filter-chip" :class="{ active: selectedFilters.includes(filter.value) }" 
                        @click="filters(filter.value, filterGroup.title)"
                    >
                        {{ filter.name }}
                    </button>
                </div>  
            </div>
            <div class="filter-group">
                <span class="filter-label">Actions :</span>
                <button class="filter-chip clear" @click="selectedFilters = []">Clear Filters</button>
            </div>
        </div>
    </Transition>
    <hr />
    <div class="cards">
        <NuxtLink v-if="enableLinks" v-for="item in filteredItems" :key="getItemId(item)"  :to="`/${page}s/${getItemId(item)}`">
            <card v-if="page !== 'season'">{{ item.name }}</card>
            <card v-else>{{ item.season }}</card>
        </NuxtLink>
        <card v-else v-for="itm in filteredItems" :key="getItemId(itm)">{{ itm.name }}</card>
        <p v-if="filteredItems.length == 0">No items match {{ search }}</p>
    </div>
</template>

<style scoped>
.panel {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}
.left {
    display: flex;
    flex-shrink: 0;
    margin-left: 30px;
}
.right {
    flex: 1;
    display: flex;
    justify-content: flex-end;
}
input {
    justify-content: flex-end;
    margin: 15px 0 15px 0;
    padding: 8px 15px 8px 15px;
    font-size: 13px;
    background-color: #303030c4;
    color: white;
    border: 1px solid #3d4249d2;
    border-radius: 10px;

}
input:focus {
    outline: none;
    border-color: #5a9bfca6;
}

.filter-toggle-btn {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    border-radius: 10px;
    border: 1px solid #3d4249d2;
    background: #303030c4;
    color: #a0a0a0;
    cursor: pointer;
    transition: all 0.2s;
}
.filter-toggle-btn:hover { border-color: #5a9bfca6; color: #fff; }

.chevron { transition: transform 0.3s; }
.chevron-open { transform: rotate(180deg); }

.filter-drawer {
    display: flex;
    position: absolute;
    z-index: 10;
    gap: 0.75rem;
    flex-wrap: wrap;
    max-width: 900px;
    padding: 0.6rem 1rem;
    background: #2a2a2a;
    border: 1px solid #3d4249d2;
    border-radius: 10px;
}
.filter-group {
    display: flex;
    flex-direction: column;
    text-align: left;
    gap: 7px;
}

.filter-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #a0a0a0;
}

.filter-chips { display: flex; gap: 0.35rem; flex-wrap: wrap; }

.filter-chip {
    padding: 4px 12px;
    font-size: 12px;
    border-radius: 20px;
    border: 1px solid #3d4249d2;
    background: #333;
    color: #a0a0a0;
    cursor: pointer;
    transition: all 0.2s;
}
.filter-chip:hover { border-color: #5a9bfca6; color: #fff; }
.filter-chip.active { background: #5a9bfc2e; border-color: #5a9bfca6; color: #fff; }

.filter-slide-enter-active, .filter-slide-leave-active { transition: all 0.25s ease; }
.filter-slide-enter-from, .filter-slide-leave-to { opacity: 0; transform: translateY(-6px); }

.clear { border-color: #a00; }
</style>