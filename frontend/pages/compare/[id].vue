<script setup>
  import { ref, watch } from 'vue';
const config = useRuntimeConfig()
const route = useRoute();
const router = useRouter();
const id = ref(route.params.id || "");
const apiRoute = `${config.public.apiBase}compare/${id.value}`;
const firstName = ref(route.query.first || "");
const firstId = ref("");
const secondName = ref(route.query.second || "");
const secondId = ref("");
const firstSeason = ref(route.query.firstSeason || "");
const secondSeason = ref(route.query.secondSeason || "");
const firstSeasons = ref("");
const firstSeasonsError = ref("");
const secondSeasons = ref("");
const secondSeasonsError = ref("");
const trimmedId = id.value.replace("s", '').toLowerCase();
const pageId = `${trimmedId}_id`;
const statsForFirst = ref(null);
const statsForFirstError = ref(null);
const statsForSecond = ref(null);
const statsForSecondError = ref(null);


const { data: list, error: listError } = await useFetch(apiRoute);

watch(() => firstName.value, (newVal) => {
  if (newVal && typeof newVal === 'object') {
    selectFirst(newVal)
  }
});
watch(() => secondName.value, (newVal) => {
  if (newVal &&typeof newVal === 'object') {
    selectSecond(newVal)
  }
});
const selectFirst = async(item) => {
  firstName.value = item.name;
  firstId.value = item[pageId];
  router.push({ query: { ...route.query, first: firstId.value } });
  const { data: seasons, error: firstError } = await useFetch(`${apiRoute}?${trimmedId}=${firstId.value}`);
  firstSeasons.value = seasons.value;
  firstSeasonsError.value = firstError.value;
};

const selectSecond = async (item) => {
  secondName.value = item.name;
  secondId.value = item[pageId];
  router.push({ query: { ...route.query, second: secondId.value } });
  const { data: seasons, error: secondError } = await useFetch(`${apiRoute}?${trimmedId}=${secondId.value}`);
  secondSeasons.value = seasons.value;
  secondSeasonsError.value = secondError.value;
};
const selectFirstSeason = async (item) => {
  firstSeason.value = item;
  router.push({ query: { ...route.query, firstSeason: item } });
  fetchStats({ season: item, first: true });
}
const selectSecondSeason = async (item) => {
  secondSeason.value = item;
  router.push({ query: { ...route.query, secondSeason: item } });
  fetchStats({ season: item, first: false });
}
async function fetchStats(params) {
  if (id.value === "Seasons") {
    console.log("Fetching stats for season", params.season);
  } else if (firstId.value && secondId.value && params.season) {
    if (params.first) {
      const { data: stats1, error: stats1err } = await useFetch(`${config.public.apiBase}team-metrics/basic-stats?${pageId}=${firstId.value}&season_id=${params.season}`);
      statsForFirst.value = stats1.value;
      statsForFirstError.value = stats1err.value;
    } else {
      const { data: stats2, error: stats2err } = await useFetch(`${config.public.apiBase}team-metrics/basic-stats?${pageId}=${secondId.value}&season_id=${params.season}`);
      statsForSecond.value = stats2.value;
      statsForSecondError.value = stats2err.value;
    }
  }
}
</script>

<template>
  <div class="page-heading">
        <h1 class ="h1-design">Comparing {{ id }}</h1>
    </div>
    <div v-if="listError">
      Error fetching {{ id }} : {{ listError.message }}
    </div>
    <div v-else class="options">
        <div v-if="id == 'Seasons'" class="option-items">
          <select v-model="firstSeason">
            <option disabled value="">Select</option>
            <option v-for="value in list" :key="value" @click="() => selectFirstSeason(value.season_id)">{{ value.season }}</option>
          </select>
          <select v-model="secondSeason">
            <option disabled value="">Select</option>
            <option v-for="value in list" :key="value" @click="() => selectSecondSeason(value.season_id)">{{ value.season }}</option>
          </select>
        </div>
        <div v-else class="option-items">
          <div class="first-selects">
            <SearchableSelect v-model="firstName" :options="list" :page="trimmedId"/>
            <SearchableSelect v-model="secondName" :options="list" :page="trimmedId"/>
          </div>
          <div v-if="firstSeasonsError || secondSeasonsError">
            Error fetching seasons:
            <div v-if="firstSeasonsError">{{ firstSeasonsError.message }}</div>
            <div v-if="secondSeasonsError">{{ secondSeasonsError.message }}</div>
          </div>
          <div v-else-if="firstId && secondId" class="season-selects">
            <select v-model="firstSeason">
              <option disabled value="">Select</option>
              <option v-for="value in firstSeasons" :key="value" @click="selectFirstSeason(value)">{{ value }}</option>
            </select>
            <select v-model="secondSeason">
              <option disabled value="">Select</option>
              <option v-for="value in secondSeasons" :key="value" @click="selectSecondSeason(value)">{{ value }}</option>
             </select>
          </div>
        </div>
    </div>
    <div v-if="statsForFirst && statsForSecond" class="stats-display">
      <div class="first-stats">
        STATS for {{ firstName }}:
        {{ statsForFirst }}
      </div>
      <div class="stats-second">
        STATS for {{ secondName }}:
        {{ statsForSecond }}
      </div>
    </div>
</template>

<style scoped>
.options {
  display: flex;
  justify-content: center;
}
.option-items {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.first-selects, .season-selects {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 100px;
  width: 100%;
}
</style>