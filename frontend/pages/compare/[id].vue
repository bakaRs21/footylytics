<script setup>
const config = useRuntimeConfig()
const route = useRoute();
const router = useRouter();
const id = ref(route.params.id || "");
const apiRoute = `${config.public.apiBase}compare/${id.value}`;
const first = ref(route.query.first || "");
const second = ref(route.query.second || "");
const firstSeason = ref(route.query.firstSeason || "");
const secondSeason = ref(route.query.secondSeason || "");
//const firstData = ref("");
//const secondData = ref("");
const firstError = ref("");
const secondError = ref("");

const firstData = { "first":["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]};
const secondData = { "second":["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]};


const { data: list, error: listError } = await useFetch(apiRoute)
const selectFirst = async(item) => {
  first.value = item;
  router.push({ query: { ...route.query, first: item } });
};

const selectSecond = async (item) => {
  second.value = item;
  router.push({ query: { ...route.query, second: item } });
  console.log(second.value);
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
            <select v-model="firstSeason" v-for="value in firstData" :key="value">
              <option disabled value=""></option>
              <option v-for="index in value" :key="index"  @click="() => selectFirstSeason(index)">{{ index }}</option>
            </select>
            <select v-model="secondSeason" v-for="value in secondData" :key="value">
              <option disabled value=""></option>
              <option v-for="index in value" :key="index"  @click="() => selectSecondSeason(index)">{{ index }}</option>
            </select>
          </div>
        </div>
    </div>
</template>

<style scoped>


</style>