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


const {status: listPending, data: list, error: listError } = await useFetch(apiRoute)
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
      <svg xmlns="http://www.w3.org/2000/svg" width="38" height="48" viewBox="0 0 24 24"><rect width="10" height="10" x="1" y="1" fill="currentColor" rx="1"><animate id="SVG7WybndBt" fill="freeze" attributeName="x" begin="0;SVGo3aOUHlJ.end" dur="0.2s" values="1;13"/><animate id="SVGVoKldbWM" fill="freeze" attributeName="y" begin="SVGFpk9ncYc.end" dur="0.2s" values="1;13"/><animate id="SVGKsXgPbui" fill="freeze" attributeName="x" begin="SVGaI8owdNK.end" dur="0.2s" values="13;1"/><animate id="SVG7JzAfdGT" fill="freeze" attributeName="y" begin="SVG28A4To9L.end" dur="0.2s" values="13;1"/></rect><rect width="10" height="10" x="1" y="13" fill="currentColor" rx="1"><animate id="SVGUiS2jeZq" fill="freeze" attributeName="y" begin="SVG7WybndBt.end" dur="0.2s" values="13;1"/><animate id="SVGU0vu2GEM" fill="freeze" attributeName="x" begin="SVGVoKldbWM.end" dur="0.2s" values="1;13"/><animate id="SVGOIboFeLf" fill="freeze" attributeName="y" begin="SVGKsXgPbui.end" dur="0.2s" values="1;13"/><animate id="SVG14lAaeuv" fill="freeze" attributeName="x" begin="SVG7JzAfdGT.end" dur="0.2s" values="13;1"/></rect><rect width="10" height="10" x="13" y="13" fill="currentColor" rx="1"><animate id="SVGFpk9ncYc" fill="freeze" attributeName="x" begin="SVGUiS2jeZq.end" dur="0.2s" values="13;1"/><animate id="SVGaI8owdNK" fill="freeze" attributeName="y" begin="SVGU0vu2GEM.end" dur="0.2s" values="13;1"/><animate id="SVG28A4To9L" fill="freeze" attributeName="x" begin="SVGOIboFeLf.end" dur="0.2s" values="1;13"/><animate id="SVGo3aOUHlJ" fill="freeze" attributeName="y" begin="SVG14lAaeuv.end" dur="0.2s" values="1;13"/></rect></svg>
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