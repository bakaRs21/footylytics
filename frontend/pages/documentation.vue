<script setup>
import card from '~/components/card.vue';
import { ref, onMounted, watch, computed } from 'vue';
import searchableSelect from '~/components/searchableSelect.vue';
import Sliding_panel from '~/components/Sliding_panel.vue';
import BarChart from '~/components/Charts/BarChart.vue';
import DonutChart from '~/components/Charts/DonutChart.vue';
import LineChart from '~/components/Charts/LineChart.vue';
import PieChart from '~/components/Charts/PieChart.vue';

const season = ref("");
const seasons = ["2006", "2007", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"];

const items1 = ["item 148390284789023740238947890", "item 2", "item 3", "item 4", "item 5", "item 6"];

const items = ["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"];
const items2 = ["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"];

const info = { "team_id": 39, "name": "Wolves", "logo": "https://media.api-sports.io/football/teams/39.png" } 

const title = ref("Wolves 2022/2023 Season Record")
const selectedChart = ref("")
const charts = ["Donut Chart", "Pie Chart", "Bar Chart", "Line Chart"]
const rawData = {
  "goals_for_minute_91_105_total": 5,
  "biggest_goals_for_away": "4",
  "cards_red_61_75_total": 1,
  "goals_for_minute_91_105_percentage": 8.93,
  "biggest_goals_against_home": "6",
  "cards_red_61_75_percentage": 50,
  "goals_for_minute_106_120_total": null,
  "biggest_goals_against_away": "5",
  "cards_red_76_90_total": null,
  "goals_for_minute_106_120_percentage": null,
  "clean_sheet_home": 5,
  "cards_red_76_90_percentage": null,
  "goals_against_total_home": 32,
  "clean_sheet_away": 3,
  "cards_red_91_105_total": 1,
  "goals_against_total_away": 37,
  "failed_to_score_home": 3,
  "cards_red_91_105_percentage": 50,
  "season_id": 2024,
  "goals_against_average_home": 1.7,
  "failed_to_score_away": 4,
  "cards_red_106_120_total": null,
  "team_id": 39,
  "goals_against_average_away": 1.9,
  "penalty_scored_total": 0,
  "cards_red_106_120_percentage": null,
  "form": "LLDLLLLLDDWWLLLLWWDLLLLWLWLDWWWWWWLLLD",
  "goals_against_minute_0_15_percentage": 14.93,
  "penalty_missed_total": 0,
  "fixtures_played_home": 19,
  "goals_against_minute_16_30_total": 10,
  "lineups": "[{'formation': '3-4-2-1', 'played': 28}, {'formation': '4-2-3-1', 'played': 4}, {'formation': '4-1-4-1', 'played': 3}, {'formation': '4-4-1-1', 'played': 2}, {'formation': '3-5-2', 'played': 1}]",
  "fixtures_played_away": 19,
  "goals_against_minute_16_30_percentage": 14.93,
  "cards_yellow_0_15_total": 5,
  "fixtures_wins_home": 6,
  "goals_against_minute_31_45_total": 11,
  "cards_yellow_0_15_percentage": 6.33,
  "fixtures_wins_away": 6,
  "goals_against_minute_31_45_percentage": 16.42,
  "cards_yellow_16_30_total": 14,
  "fixtures_draws_home": 3,
  "goals_against_minute_46_60_total": 12,
  "cards_yellow_16_30_percentage": 17.72,
  "fixtures_draws_away": 3,
  "goals_against_minute_46_60_percentage": 17.91,
  "cards_yellow_31_45_total": 14,
  "fixtures_loses_home": 10,
  "goals_against_minute_61_75_total": 11,
  "cards_yellow_31_45_percentage": 17.72,
  "fixtures_loses_away": 10,
  "goals_against_minute_61_75_percentage": 16.42,
  "cards_yellow_46_60_total": 13,
  "goals_for_total_home": 27,
  "goals_against_minute_76_90_total": 9,
  "cards_yellow_46_60_percentage": 16.46,
  "goals_for_total_away": 27,
  "goals_against_minute_76_90_percentage": 13.43,
  "cards_yellow_61_75_total": 13,
  "goals_for_minute_0_15_total": 9,
  "goals_against_minute_91_105_total": 4,
  "cards_yellow_61_75_percentage": 16.46,
  "goals_for_minute_0_15_percentage": 16.07,
  "goals_against_minute_91_105_percentage": 5.97,
  "cards_yellow_76_90_total": 13,
  "goals_for_minute_16_30_total": 8,
  "goals_against_minute_106_120_total": null,
  "cards_yellow_76_90_percentage": 16.46,
  "goals_for_minute_16_30_percentage": 14.29,
  "goals_against_minute_106_120_percentage": null,
  "cards_yellow_91_105_total": 6,
  "goals_for_minute_31_45_total": 7,
  "biggest_streak_wins": "6",
  "cards_yellow_91_105_percentage": 7.59,
  "goals_for_minute_31_45_percentage": 12.5,
  "biggest_streak_draws": "2",
  "cards_red_0_15_total": null,
  "goals_for_minute_46_60_total": 9,
  "biggest_streak_loses": "5",
  "cards_red_0_15_percentage": null,
  "goals_for_minute_46_60_percentage": 16.07,
  "biggest_wins_home": "Mar-00",
  "cards_red_16_30_total": null,
  "goals_for_minute_61_75_total": 11,
  "biggest_wins_away": "4-Jan",
  "cards_red_16_30_percentage": null,
  "goals_for_minute_61_75_percentage": 19.64,
  "biggest_loses_home": "6-Feb",
  "cards_red_31_45_total": null,
  "goals_for_minute_76_90_total": 7,
  "biggest_loses_away": "Apr-00",
  "cards_red_31_45_percentage": null,
  "goals_for_minute_76_90_percentage": 12.5,
  "biggest_goals_for_home": "4",
  "cards_red_46_60_total": null,
  "goals_against_minute_0_15_total": 10,
  "cards_red_46_60_percentage": null
}

</script>

<template>
  <searchable-select v-model="season" :options="seasons" placeholder="Select season"/>
  <p>Selected season: {{ season }}</p>
  
    
  <div class="cards">
    <card v-for="value in items" :key="value" class="card">{{ value }}</card>
  </div>
    
  <Sliding_panel :items="items1" />

  <div class="dashboard">
    <div class="dashboard-row">
      <DashboardCard 
        :chartOptions="charts" 
        :dataForChart="rawData"
      />
      <DashboardCard 
        :chartOptions="charts" 
        :dataForChart="rawData"
      />
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  background-color: rgb(39, 39, 39);
  border-radius: 20px;
  box-shadow: 0 15px 20px rgba(29, 25, 59, 0.884);
  height: fit-content;
  padding: 35px;
  gap: 15px;
}
.dashboard-row {
  display: flex;
  flex: 1;
  gap: 20px;
}
</style>