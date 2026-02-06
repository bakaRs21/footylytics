<script setup>
  import { ref, watch } from 'vue';
const config = useRuntimeConfig()
const route = useRoute();
const router = useRouter();
const id = ref(route.params.id || "");
const apiRoute = `${config.public.apiBase}compare/${id.value}`;
const first = ref(route.query.first || "");
const second = ref(route.query.second || "");
const firstSeason = ref(route.query.firstSeason || "");
const secondSeason = ref(route.query.secondSeason || "");
const firstSeasons = ref("");
const firstSeasonsError = ref("");
const secondSeasons = ref("");
const secondSeasonsError = ref("");

const trimmedId = id.value.replace("s", '').toLowerCase();

const { data: list, error: listError } = await useFetch(apiRoute);

watch(() => first.value, (newVal) => {
  if (newVal) {
    selectFirst(newVal)
  }
});
watch(() => second.value, (newVal) => {
  if (newVal) {
    selectSecond(newVal)
  }
});
watch(() => firstSeason.value, (newVal) => {
  if (newVal) {
    selectFirstSeason(newVal)
  }
});
watch(() => secondSeason.value, (newVal) => {
  if (newVal) {
    selectSecondSeason(newVal)
  }
});
const selectFirst = async(item) => {
  first.value = item;
  router.push({ query: { ...route.query, first: item } });
  const { data: seasons, error: firstError } = await useFetch(`${apiRoute}?${trimmedId}=${first.value}`);
  console.log(`${apiRoute}?${trimmedId}=${first.value}`);
  firstSeasons.value = seasons.value;
  firstSeasonsError.value = firstError.value;
};

const selectSecond = async (item) => {
  second.value = item;
  router.push({ query: { ...route.query, second: item } });
  const { data: seasons, error: secondError } = await useFetch(`${apiRoute}?${trimmedId}=${second.value}`);
  secondSeasons.value = seasons.value;
  secondSeasonsError.value = secondError.value;
};
const selectFirstSeason = async (item) => {
  firstSeason.value = item;
  router.push({ query: { ...route.query, firstSeason: item } });

}
const selectSecondSeason = async (item) => {
  secondSeason.value = item;
  router.push({ query: { ...route.query, secondSeason: item } });
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
            <SearchableSelect v-model="first" :options="list" :page="trimmedId"/>
            <SearchableSelect v-model="second" :options="list" :page="trimmedId"/>
          </div>
          <div v-if="firstSeasonsError || secondSeasonsError">
            Error fetching seasons:
            <div v-if="firstSeasonsError">{{ firstSeasonsError.message }}</div>
            <div v-if="secondSeasonsError">{{ secondSeasonsError.message }}</div>
          </div>
          <div v-else-if="first && second" class="season-selects">
            <SearchableSelect v-model="firstSeason" :options="firstSeasons" placeholder="Select season "/>
            <SearchableSelect v-model="secondSeason" :options="secondSeasons" placeholder="Select season "/>
          </div>
        </div>
    </div>
</template>

<style scoped>
</style>