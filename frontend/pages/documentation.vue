<script setup>
import card from '~/components/card.vue';
import { ref } from 'vue';
import searchableSelect from '~/components/searchableSelect.vue';
import RightArrow from '~/components/Icons/Right_Arrow.vue';
import LeftArrow from '~/components/Icons/Left_Arrow.vue';
import SlidingPanel from '~/components/Sliding_panel.vue';

const season = ref("");
const seasons = ["2006", "2007", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"];

const items = ["item 148390284789023740238947890", "item 2", "item 3", "item 4", "item 5", "item 6"];

const item = "one item";

</script>

<template>
  <searchable-select v-model="season" :options="seasons" placeholder="Select season"/>
  <p>Selected season: {{ season }}</p>
  
    
    <div class="cards">
      <div v-for="value in items" :key="value">
        <card class="card">{{ value }}</card>
      </div>
    </div>
    
    <RightArrow />
    <LeftArrow />

    <SlidingPanel :items="items" />
</template>

<style scoped>
</style>