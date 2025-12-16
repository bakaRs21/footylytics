<script setup>
import card from '~/components/card.vue';
import { ref } from 'vue';
import searchableSelect from '~/components/searchableSelect.vue';

const season = ref("");
const seasons = ["2006", "2007", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"];

const items = ["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"];


</script>

<template>
  <searchable-select v-model="season" :options="seasons" placeholder="Select season"/>
  <p>Selected season: {{ season }}</p>
  

    <div class="card-margin">
        <div class="card-grid" v-for="value in items" :key="value">
            <card id="card">{{ value }}</card>
        </div>
    </div>
</template>

<style scoped>
.card-margin {
  margin-top: 80px;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}
</style>