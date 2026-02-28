<script setup>
  import { ref, onMounted, watch } from 'vue';
const config = useRuntimeConfig()
const route = useRoute();
const router = useRouter();
// route query constants
const first = route.query.first;
const second = route.query.second;
const firstSeason = route.query.firstSeason;
const secondSeason = route.query.secondSeason;
const id = ref(route.params.id || "");
 // api route for current page
const apiRoute = `${config.public.apiBase}compare/${id.value}`;
// Fetched Current Page Content
const { data: list, error: listError } = await useFetch(apiRoute);
// Helper Constants
const trimmedId = id.value.replace("s", '').toLowerCase();
const pageId = `${trimmedId}_id`;
const errorMsgId = id.value.toLowerCase();
const metricApiRoute = `${config.public.apiBase}${trimmedId}-metrics/`; // api metric route
// First Item Constants
const firstObject = ref(null)
const firstName = ref("");
const firstId = ref(route.query.first || "");
const firstSeasons = ref(null); // seasons for first item
const firstSeasonParam = ref(""); // parameter for fetching stats for first item
const firstSeasonsError = ref("");
// Second Item Constants
const secondObject = ref(null)
const secondName = ref("");
const secondId = ref(route.query.second || "");
const secondSeasons = ref(null); // seasons for second item
const secondSeasonParam = ref(""); // parameter for fetching stats for second item
const secondSeasonsError = ref("");
// Fetching
const compareErrorMsg = ref(""); // error message used before fetching stats
const isFetchingStats = ref(false);
const statsErrorMsg = ref("");
// Stats Constants
const statsForFirst = ref(null);
const statsForSecond = ref(null);


watch([first, second, firstSeason, secondSeason], () => {
  Inspection();
  if (!compareErrorMsg.value) {
    fetchData();
  }
})

function Inspection() {
  compareErrorMsg.value = "";
  if (id.value === "Seasons") {
    if (!route.query.firstSeason || !route.query.secondSeason) {
      compareErrorMsg.value = "Please select both seasons.";
      return;
    }
    if (route.query.firstSeason === route.query.secondSeason) {
      compareErrorMsg.value = "Cannot compare the same season. Please select different seasons.";
      return;
    }
  }
  if (!route.query.first || !route.query.second) {
    compareErrorMsg.value = `Please select both ${errorMsgId}.`;
    firstSeasons.value = "";
    secondSeasons.value = "";
    return;
  }
  if (route.query.first === route.query.second) {
    compareErrorMsg.value = `Cannot compare the same ${errorMsgId}. Please select different ${errorMsgId}.`;
    return;
  }
  if (route.query.first && route.query.second && !route.query.firstSeason && !route.query.secondSeason) {return;}
  if (!route.query.first || !route.query.second || !route.query.firstSeason || !route.query.secondSeason) {
    compareErrorMsg.value = `Please select both ${errorMsgId} and their seasons.`;
    return;
  }
  if (route.query.firstSeason === 'all-seasons' || route.query.secondSeason === 'all-seasons') {
    if (route.query.firstSeason === 'all-seasons') {
      firstSeasonParam.value = "";
    } else {
        firstSeasonParam.value = `&season_id=${route.query.firstSeason}`;
    }
    if (route.query.secondSeason === 'all-seasons') {
      secondSeasonParam.value = "";
    } else {
      secondSeasonParam.value = `&season_id=${route.query.secondSeason}`;
    }
  } else {
    firstSeasonParam.value = `&season_id=${route.query.firstSeason}`;
    secondSeasonParam.value = `&season_id=${route.query.secondSeason}`;
  }
  statsErrorMsg.value = "";
  return
}
async function fetchData() {
  isFetchingStats.value = true;
  statsForFirst.value = null;
  statsForSecond.value = null;
  statsErrorMsg.value = "";
  try {
    if (id.value === "Seasons") {
      const [first, second] = await Promise.all([
        $fetch(`${apiRoute}?season_id=${route.query.firstSeason}`),
        $fetch(`${apiRoute}?season_id=${route.query.secondSeason}`)
      ]);
      statsForFirst.value = first;
      statsForSecond.value = second;
    } else {
      if (!route.query.firstSeason || !route.query.secondSeason) {
        const [first, second] =await Promise.all([
          $fetch(`${apiRoute}?${pageId}=${route.query.first}`),
          $fetch(`${apiRoute}?${pageId}=${route.query.second}`)
        ])
        firstSeasons.value = first,
        secondSeasons.value = second;
      } else {
        const [first, second] = await Promise.all([
        $fetch(`${metricApiRoute}basic-stats?${pageId}=${route.query.first}${firstSeasonParam.value}`),
        $fetch(`${metricApiRoute}basic-stats?${pageId}=${route.query.second}${secondSeasonParam.value}`)
      ]);
      statsForFirst.value = first;
      statsForSecond.value = second;
      } 
    }
  } catch (error) {
    statsErrorMsg.value = "Error fetching stats: " + error.message;
  } finally {
    isFetchingStats.value = false;
  }
} 

onMounted(async () => {
  if (route.query.first && !firstName.value) {
    try {
      console.log("fetching first seasons for", firstId.value);
    } catch (error) {
      firstSeasonsError.value = error.message;
    }
  }
  if (route.query.second && !secondName.value) {
    try {
      console.log("fetching second seasons for", secondId.value);
    } catch (error) {
      secondSeasonsError.value = error.message;
    }
  }
})
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
          <div class="first-selects">
            <select v-model="firstSeason">
              <option disabled value="">Select</option>
              <option v-for="value in list" :key="value" @click="() => selectFirstSeason(value.season_id)">{{ value.season }}</option>
            </select>
            <select v-model="secondSeason">
              <option disabled value="">Select</option>
              <option v-for="value in list" :key="value" @click="() => selectSecondSeason(value.season_id)">{{ value.season }}</option>
            </select>
          </div>
        </div>
        <div v-else class="option-items">
          <div class="first-selects">
            <SearchableSelect v-model="firstObject" :options="list" :page="trimmedId"/>
            <SearchableSelect v-model="secondObject" :options="list" :page="trimmedId"/>
          </div>
          <div v-if="firstSeasonsError || secondSeasonsError">
            Error fetching seasons:
            <div v-if="firstSeasonsError">{{ firstSeasonsError.message }}</div>
            <div v-if="secondSeasonsError">{{ secondSeasonsError.message }}</div>
          </div>
          <div class="season-selects">
            <select v-model="firstSeason">
              <option disabled value="">Select</option>
              <option value="all-seasons" @click="selectFirstSeason(0)">all seasons</option>
              <option v-for="value in firstSeasons" :key="value" @click="selectFirstSeason(value)">{{ value }}</option>
            </select>
            <select v-model="secondSeason">
              <option disabled value="">Select</option>
              <option value="all-seasons" @click="selectSecondSeason(0)">all seasons</option>
              <option v-for="value in secondSeasons" :key="value" @click="selectSecondSeason(value)">{{ value }}</option>
             </select>
          </div>
        </div>
    </div>
    <div class="comparing-stats">
      <div v-if="compareErrorMsg" class="error-message">
        {{ compareErrorMsg }}
      </div>
      <div v-else-if="isFetchingStats" class="loading-message">
        Fetching stats... <LoadingSvg />
      </div>
      <div v-else-if="statsErrorMsg" class="error-message">
        {{ statsErrorMsg }}
      </div>
      <div v-else-if="firstSeason && secondSeason && !statsForFirst && !statsForSecond">
        No stats available for the selected seasons.
      </div>
      <div v-else-if="statsForFirst && statsForSecond">
        <div>
            <CompareStats v-if="statsForFirst && statsForSecond"
            :first-stats="statsForFirst" :first-name="firstName" :second-stats="statsForSecond" :second-name="secondName" :type="trimmedId"
            />
        </div>
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