<script setup>
import card from '~/components/card.vue';
import { ref, onMounted } from 'vue';
import searchableSelect from '~/components/searchableSelect.vue';
import Sliding_panel from '~/components/Sliding_panel.vue';
import ColorThief from 'colorthief';

const season = ref("");
const seasons = ["2006", "2007", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"];

const items1 = ["item 148390284789023740238947890", "item 2", "item 3", "item 4", "item 5", "item 6"];

const items = ["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"];
const items2 = ["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"];

const info = { "team_id": 39, "name": "Wolves", "logo": "https://media.api-sports.io/football/teams/39.png" } 

const secondary = ref("")
onMounted(() => {
  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.src = info.logo;
  img.onload = () => {
    const colorThief = new ColorThief();
    const palette = colorThief.getPalette(img, 3)
    secondary.value = `rgb(${palette[1].join(',')})`

    console.log(palette, secondary)
  }
})

</script>

<template>
  <searchable-select v-model="season" :options="seasons" placeholder="Select season"/>
  <p>Selected season: {{ season }}</p>
  
    
  <div class="cards">
    <card v-for="value in items" :key="value" class="card">{{ value }}</card>
  </div>
    
  <Sliding_panel :items="items1" />
  <div class="team" :style="{backgroundColor: secondary}">
    {{ info.name }}
    <img :src="info.logo" :alt="info.name" />
    {{ secondary }}
  </div>
</template>

<style scoped>
.team {
  border: 5px solid black;
}
</style>