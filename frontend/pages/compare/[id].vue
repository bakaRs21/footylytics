<script setup>
  import { Icon } from '@iconify/vue';
  import { ref, onMounted, watch } from 'vue';
  import CompareSeasons from '~/components/CompareSeasons.vue';
  import PageContent from '~/components/PageContent.vue';
const config = useRuntimeConfig()
const route = useRoute();
const router = useRouter();
// route query constants
const firstSeasonSelected = ref(route.query.firstSeason || "");
const firstSeasonSelectedName = computed(() => `${firstSeasonSelected.value}-${Number(firstSeasonSelected.value) + 1}`)
const secondSeasonSelected = ref(route.query.secondSeason || "");
const secondSeasonSelectedName = computed(() => `${secondSeasonSelected.value}-${Number(secondSeasonSelected.value) + 1}`)
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
const seasonMetricApiRoute = `${config.public.apiBase}season-metrics/`; // season metrics api route
// First Item Constants
const firstObject = ref(null)
const firstName = ref("");
const firstId = ref(route.query.first || "");
const firstSeasons = ref(null); // seasons for first item
const firstSeasonsError = ref("");
// Second Item Constants
const secondObject = ref(null)
const secondName = ref("");
const secondId = ref(route.query.second || "");
const secondSeasons = ref(null); // seasons for second item
const secondSeasonsError = ref("");
// Fetching
const compareErrorMsg = ref(""); // error message used before fetching stats
const isFetchingStats = ref(false);
const statsErrorMsg = ref("");
// Stats Constants
const statsForFirst = ref(null);
const statsForSecond = ref(null);
// page content sections
const sections = [
  {label: "Selection", anchor: "top-section"},
  {label: "Stats comparison", anchor: "stats"}
]

watch([firstObject, secondObject, firstSeasonSelected, secondSeasonSelected], async ([newFirst, newSecond, newFirstSeason, newSecondSeason], [oldFirst, oldSecond]) => {
  if (newFirstSeason && newSecondSeason) {
    firstSeasonSelected.value = newFirstSeason || ""
    secondSeasonSelected.value = newSecondSeason || ""
  }
  if (newFirst != oldFirst){
    firstId.value = newFirst?.[pageId]
    firstName.value = newFirst?.name
    firstSeasons.value = null
    firstSeasonSelected.value = ""
    firstSeasonsError.value = ""
  }
  if (newSecond != oldSecond) {
    secondId.value = newSecond?.[pageId]
    secondName.value = newSecond?.name
    secondSeasons.value = null
    secondSeasonSelected.value = ""
    secondSeasonsError.value = ""
  }
  await router.replace({ query: { first: firstId.value, second: secondId.value, firstSeason: firstSeasonSelected.value, secondSeason: secondSeasonSelected.value } })
  await Inspection()
})

async function Inspection() {
  compareErrorMsg.value = "";
  statsForFirst.value = null
  statsForSecond.value = null
  statsErrorMsg.value = "";
  if (id.value === "Seasons") {
    if (!firstSeasonSelected.value|| !secondSeasonSelected.value ) {
      compareErrorMsg.value = "Please select both seasons.";
      return;
    }
    if (firstSeasonSelected.value === secondSeasonSelected.value) {
      compareErrorMsg.value = "Cannot compare the same season. Please select different seasons.";
      return;
    }
    isFetchingStats.value = true;
    try {
      const [first, second] = await Promise.all([
        $fetch(`${seasonMetricApiRoute}stats?season_id=${firstSeasonSelected.value}`),
        $fetch(`${seasonMetricApiRoute}stats?season_id=${secondSeasonSelected.value}`)
      ]);
      statsForFirst.value = first;
      statsForSecond.value = second;
    } catch (error) {
      statsErrorMsg.value = "Error fetching stats: " + error.message;
    } finally {
      isFetchingStats.value = false;
    }
    return; 
  }
  if (!firstId.value || !secondId.value) {
    compareErrorMsg.value = `Please select both ${errorMsgId} first.`;
    firstSeasons.value = "";
    secondSeasons.value = "";
    return;
  }
  if (firstId.value === secondId.value) {
    compareErrorMsg.value = `Cannot compare the same ${errorMsgId}. Please select different ${errorMsgId}.`;
    return;
  }
  if (!firstSeasons.value || !secondSeasons.value) {
    firstSeasonsError.value = ""
    secondSeasonsError.value = "" 
    try {
      const [first, second] = await Promise.all([
        $fetch(`${apiRoute}?${pageId}=${firstId.value}`),
        $fetch(`${apiRoute}?${pageId}=${secondId.value}`)
      ])
      firstSeasons.value = first
      secondSeasons.value = second
    } catch (error) {
      firstSeasonsError.value = error.message
      return
    }
    if (!firstSeasonSelected.value || !secondSeasonSelected.value) {
      return;
    }
  }
  if (!route.query.first || !route.query.second || !route.query.firstSeason || !route.query.secondSeason) {
    compareErrorMsg.value = `Please select both ${errorMsgId} and their seasons.`;
    return;
  }
  const firstSeasonParam = firstSeasonSelected.value === "all-seasons" ? "" : `&season_id=${firstSeasonSelected.value}`
  const secondSeasonParam = secondSeasonSelected.value === "all-seasons" ? "" : `&season_id=${secondSeasonSelected.value}`
  isFetchingStats.value = true;
  try {
    const [first, second] = await Promise.all([
      $fetch(`${metricApiRoute}basic-stats?${pageId}=${firstId.value}${firstSeasonParam}`),
      $fetch(`${metricApiRoute}basic-stats?${pageId}=${secondId.value}${secondSeasonParam}`)
    ])
    statsForFirst.value = first
    statsForSecond.value = second
  } catch (error) {
    statsErrorMsg.value = error.message
  } finally {
    isFetchingStats.value = false
  }
}

onMounted(async () => {
  const hasParams = firstId.value || secondId.value || firstSeasonSelected.value || secondSeasonSelected.value;
  if (hasParams) await Inspection();
})
</script>

<template>
  <div class="page-heading">
        <h1 class ="h1-design" id="top-section">Comparing {{ id }}</h1>
    </div>
    <div v-if="listError">
      Error fetching {{ id }} : {{ listError.message }}
    </div>
    <div v-else class="options">
        <div v-if="id == 'Seasons'" class="option-items">
          <div class="first-selects">
            <select v-model="firstSeasonSelected">
              <option disabled value="">Select</option>
              <option v-for="value in list" :key="value">{{ value.season_id }}</option>
            </select>
            <select v-model="secondSeasonSelected">
              <option disabled value="">Select</option>
              <option v-for="value in list" :key="value">{{ value.season_id }}</option>
            </select>
          </div>
        </div>
        <div v-else class="option-items">
          <div class="first-selects">
            <SearchableSelect v-model="firstObject" :options="list" :page="trimmedId"/>
            <SearchableSelect v-model="secondObject" :options="list" :page="trimmedId"/>
          </div>
          <div v-if="firstSeasonsError">
            Error fetching seasons:
            <div>{{ firstSeasonsError }}</div>
          </div>
          <div class="season-selects" v-if="firstId && secondId">
            <select v-model="firstSeasonSelected">
              <option disabled value="">Select season</option>
              <option value="all-seasons">all seasons</option>
              <option v-for="value in firstSeasons" :key="value">{{ value }}</option>
            </select>
            <select v-model="secondSeasonSelected">
              <option disabled value="">Select season</option>
              <option value="all-seasons">all seasons</option>
              <option v-for="value in secondSeasons" :key="value">{{ value }}</option>
             </select>
          </div>
        </div>
    </div>
    <div class="comparing-stats">
      <div v-if="compareErrorMsg" class="error-message">
        {{ compareErrorMsg }}
      </div>
      <div v-else-if="isFetchingStats" class="loading-message">
        Fetching stats... <Icon icon="mdi:loading" />
      </div>
      <div v-else-if="statsErrorMsg" class="error-message">
        {{ statsErrorMsg }}
      </div>
      <div v-else-if="firstSeasonSelected && secondSeasonSelected && !statsForFirst && !statsForSecond">
        No stats available for the selected seasons.
      </div>
      <div v-else-if="statsForFirst && statsForSecond">
        <div id="stats">
            <CompareStats v-if="statsForFirst && statsForSecond && id != 'Seasons'"
            :first-stats="statsForFirst" :first-name="firstName" :second-stats="statsForSecond" :second-name="secondName" :type="trimmedId"
            />
            <CompareSeasons v-else-if="statsForFirst && statsForSecond && id == 'Seasons'"
            :first-stats="statsForFirst" :second-stats="statsForSecond" :first-name="firstSeasonSelectedName" :second-name="secondSeasonSelectedName"
            />
        </div>
      </div>
    </div>

    <PageContent :page-sections="sections" />
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