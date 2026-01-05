<script setup>
import card from '~/components/card.vue';
import { ref } from 'vue';
import searchableSelect from '~/components/searchableSelect.vue';
import RightArrow from '~/components/Icons/Right_Arrow.vue';
import LeftArrow from '~/components/Icons/Left_Arrow.vue';
import Sliding_panel from '~/components/Sliding_panel.vue';

const season = ref("");
const seasons = ["2006", "2007", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"];

const items1 = ["item 148390284789023740238947890", "item 2", "item 3", "item 4", "item 5", "item 6"];

const items = ["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"];
const items2 = ["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"];
</script>

<template>
  <searchable-select v-model="season" :options="seasons" placeholder="Select season"/>
  <p>Selected season: {{ season }}</p>
  
    
    <div class="cards">
        <card v-for="value in items" :key="value" class="card">{{ value }}</card>
    </div>
    
    <RightArrow />
    <LeftArrow />

    <Sliding_panel :items="items1" />

    <SearchableCards :enable-links="false" :items="items2" placeholder="Search items..."/>
</template>

<style scoped>
</style>