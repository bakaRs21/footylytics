<script setup>
  import { ref } from 'vue';
  import searchableSelect from '~/components/searchableSelect.vue';
const config = useRuntimeConfig()
const route = useRoute();
const router = useRouter();
const id = ref(route.params.id || "");
const apiRoute = `${config.public.apiBase}compare/${id.value}`;
const first = ref(route.query.first || "");
const second = ref(route.query.second || "");
const firstSeason = ref(route.query.firstSeason || "");
const secondSeason = ref(route.query.secondSeason || "");
const firstData = ref("");
const firstDataError = ref("");
const secondData = ref("");
const secondDataError = ref("");


const {status: listPending, data: list, error: listError } = await useFetch(apiRoute, {
  lazy: true,
});
const selectFirst = async(item) => {
  first.value = item;
  router.push({ query: { ...route.query, first: item } });
  const { data: firstSeasons, error: firstError } = await useFetch(`${config.public.apiBase}compare/Players?player=${first.value}`);
  firstData.value = firstSeasons.value;
  firstDataError.value = firstError.value;
};

const selectSecond = async (item) => {
  second.value = item;
  router.push({ query: { ...route.query, second: item } });
  const { data: secondSeasons, error: secondError } = await useFetch(`${config.public.apiBase}compare/Players?player=${second.value}`);
  secondData.value = secondSeasons.value;
  secondDataError.value = secondError.value;
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
    <div v-if="listPending === 'pending'">
      <h2 class="pending-design">Loading data...</h2> 
      <loading-svg />
    </div>
    <div v-if="listError">
      Error fetching {{ id.value }} : {{ listError.message }}
    </div>
    <div v-else class="options">
        <div v-if="id == 'Seasons'" class="option-items">
          <select v-model="firstSeason" v-for="items in list" :key="value">
          <option disabled value="">Select</option>
          <option v-for="value in items" :key="value" @click="() => selectFirstSeason(value)">{{ value }}</option>
          </select>
          <select v-model="secondSeason" v-for="items in list" :key="value">
            <option disabled value="">Select</option>
            <option v-for="value in items" :key="value" @click="() => selectSecondSeason(value)">{{ value }}</option>
          </select>
        </div>
        <div v-else class="option-items">
          <select v-model="first" v-for="items in list" :key="value">
          <option disabled value="">First Choice</option>
          <option v-for="value in items" :key="value" @click="() => selectFirst(value)">{{ value }}</option>
          </select>
          <select v-model="second" v-for="items in list" :key="value">
            <option disabled value="">Second Choice</option>
            <option v-for="value in items" :key="value" @click="() => selectSecond(value)">{{ value }}</option>
          </select>
          <div v-if="first && second">
            <SearchableSelect v-if="firstData && secondData" v-model="firstSeason" :options="firstData" placeholder="Select season for {{ first }}"/>
            <SearchableSelect v-if="firstData && secondData" v-model="secondSeason" :options="secondData" placeholder="Select season for {{ second }}"/>
          </div>
        </div>
    </div>
</template>

<style scoped>


</style>