<script setup>
import { ref, watch, computed } from 'vue';
import { Icon } from '@iconify/vue';

const { t } = useI18n()
const localePath = useLocalePath()
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
        default: undefined
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
    if (type === t('components.searchableCards.seasons')) {
        filtersToArray(selectedSeasons, filterValue)
    }
    if (type === t('components.searchableCards.teams')) {
        filtersToArray(selectedTeams, filterValue)
    }
}
function filtersToArray(array, filterValue) {
    console.log('filter added/removed:', filterValue)
    if (array.value.includes(filterValue)) {
        array.value.splice(array.value.indexOf(filterValue), 1)
        selectedFilters.value.splice(selectedFilters.value.indexOf(filterValue), 1)
    } else {
        array.value.push(filterValue)
        selectedFilters.value.push(filterValue)
    }
}
function clearFilters() {
    selectedFilters.value = []
    selectedSeasons.value = []
    selectedTeams.value = []
}

const availableFilters = computed(() => {
    if (props.page === 'season') {
        return [{ title: t('common.noFiltersAvailable'), value: null }]
    }
    if (props.page === 'team') {
        return [{title: t('components.searchableCards.seasons'), value: availableSeasons.value.map(season => ({ name: season.season, value: season.season_id }))}];
    }
    if (props.page === 'player') {
        return [
            { title: t('components.searchableCards.seasons'), value: availableSeasons.value.map(season => ({ name: season.season, value: season.season_id })) },
            { title: t('components.searchableCards.teams'), value: availableTeams.value.map(team => ({ name: team.name, value: team.team_id })) }
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

const placeholderText = computed(() => {
  return props.placeholder || t('components.searchableCards.searchPlaceholder')
})
</script>
<template>
    <div class="panel">
        <div class="left panel-left">
            <pre>{{ $t('common.search') }}: {{ count }}</pre>
        </div>
        <button v-if="page !== 'season'" class="filter-toggle-btn btn-filter" @click="filterOpen = !filterOpen">
            <Icon icon="mdi:filter-variant" />
            {{ $t('common.filters') }}
            <Icon icon="mdi:chevron-down" :class="{ 'chevron-open': filterOpen }" class="chevron" />
        </button>
        <div class="right panel-right">
            <input v-model="search" type="text" :placeholder="placeholderText" class="input-compact"/>
        </div>
    </div>
    <Transition name="filter-slide">
        <div v-if="filterOpen" class="filter-drawer panel-filter">
            <div class="filter-group" v-for="filterGroup in availableFilters" :key="filterGroup.title">
                <span class="filter-label label-filter">{{ filterGroup.title }} :</span>
                <div class="filter-chips">
                    <button v-for="filter in filterGroup.value" :key="filter.value" 
                        class="filter-chip btn-chip" :class="{ active: selectedFilters.includes(filter.value) }" 
                        @click="filters(filter.value, filterGroup.title)"
                    >
                        {{ filter.name }}
                    </button>
                </div>  
            </div>
            <div class="filter-group">
                <span class="filter-label label-filter">{{ $t('common.select') }} :</span>
                <button class="filter-chip btn-chip clear" @click="clearFilters">{{ $t('common.clearFilters') }}</button>
            </div>
        </div>
    </Transition>
    <hr />
    <div class="cards">
        <NuxtLink v-if="enableLinks" v-for="item in filteredItems" :key="getItemId(item)"  :to="localePath(`/${page}s/${getItemId(item)}`)">
            <card v-if="page !== 'season'">{{ item.name }}</card>
            <card v-else>{{ item.season }}</card>
        </NuxtLink>
        <card v-else v-for="itm in filteredItems" :key="getItemId(itm)">{{ itm.name }}</card>
        <p v-if="filteredItems.length == 0">{{ $t('common.noData') }}</p>
    </div>
</template>

<style scoped>
.left {
    margin-left: 30px;
}
input {
    justify-content: flex-end;
    margin: 15px 0 15px 0;
}

.chevron { transition: transform 0.3s; }
.chevron-open { transform: rotate(180deg); }

.clear { border-color: #a00; }
</style>