<script setup>
import { ref, computed } from 'vue';
import { Icon } from '@iconify/vue';

const { t } = useI18n()
const localePath = useLocalePath()
const activeTab = ref('teams');

const tabs = [
  { id: 'teams', label: t('pages.teams.title') },
  { id: 'players', label: t('pages.players.title') },
  { id: 'seasons', label: t('pages.seasons.title') },
  { id: 'compare', label: t('manual.compare.title') },
];

const pageSections = computed(() => {
  const sections = [
    { label: t('manual.sections.manualSelection'), anchor: 'manual-selection' }
  ];
  if (activeTab.value === 'teams') {
    sections.push(
      { label: t('manual.sections.teamsOverview'), anchor: 'teams-overview' },
      { label: t('manual.sections.teamsIndexPage'), anchor: 'teams-index' },
      { label: t('manual.sections.individualTeamPage'), anchor: 'individual-team' },
      { label: t('manual.sections.teamLogoSection'), anchor: 'team-logo' },
      { label: t('manual.sections.seasonSelection'), anchor: 'season-selection' },
      { label: t('manual.sections.teamStatistics'), anchor: 'team-statistics' },
      { label: t('manual.sections.teamMatches'), anchor: 'team-matches' },
      { label: t('manual.sections.metricsDashboard'), anchor: 'metrics-dashboard' },
      { label: t('manual.sections.navigationTips'), anchor: 'navigation-tips' }
    );
  } else if (activeTab.value === 'players') {
    sections.push(
      { label: t('manual.sections.playersOverview'), anchor: 'players-overview' },
      { label: t('manual.sections.playersIndexPage'), anchor: 'players-index' },
      { label: t('manual.sections.individualPlayerPage'), anchor: 'individual-player' },
      { label: t('manual.sections.playerInformation'), anchor: 'player-information' },
      { label: t('manual.sections.playerSeasonSelection'), anchor: 'player-season-selection' },
      { label: t('manual.sections.playerStatistics'), anchor: 'player-statistics' },
      { label: t('manual.sections.playerMetrics'), anchor: 'player-metrics' },
      { label: t('manual.sections.colorCoding'), anchor: 'color-coding' }
    );
  } else if (activeTab.value === 'seasons') {
    sections.push(
      { label: t('manual.sections.seasonsOverview'), anchor: 'seasons-overview' },
      { label: t('manual.sections.seasonsIndexPage'), anchor: 'seasons-index' },
      { label: t('manual.sections.individualSeasonPage'), anchor: 'individual-season' },
      { label: t('manual.sections.seasonStatsSection'), anchor: 'season-stats-section' },
      { label: t('manual.sections.seasonRanking'), anchor: 'season-ranking' },
      { label: t('manual.sections.seasonMatches'), anchor: 'season-matches' },
      { label: t('manual.sections.seasonNavigation'), anchor: 'season-navigation' },
      { label: t('manual.sections.usageTips'), anchor: 'usage-tips' }
    );
  } else if (activeTab.value === 'compare') {
    sections.push(
      { label: t('manual.sections.compareOverview'), anchor: 'compare-overview' },
      { label: t('manual.sections.compareIndex'), anchor: 'compare-index' },
      { label: t('manual.sections.pagesStructure'), anchor: 'pages-structure' },
      { label: t('manual.sections.seasonComparison'), anchor: 'season-comparison' },
      { label: t('manual.sections.teamComparison'), anchor: 'team-comparison' },
      { label: t('manual.sections.playerComparison'), anchor: 'player-comparison' },
      { label: t('manual.sections.navigationFeatures'), anchor: 'navigation-features' },
      { label: t('manual.sections.visualDesign'), anchor: 'visual-design' },
      { label: t('manual.sections.advancedTips'), anchor: 'advanced-tips' },
      { label: t('manual.sections.troubleshooting'), anchor: 'troubleshooting' },
      { label: t('manual.sections.quickReference'), anchor: 'quick-reference' }
    );
  }

  return sections;
});
</script>

<template>
  <div class="page-heading">
    <h1 class="h1-design">{{ $t('navigation.manual') }}</h1>
    <p class="subtitle">{{ $t('manual.subtitle') }}</p>
  </div>
  <div class="manual-container">
    <div class="tab-navigation" id="manual-selection">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- TEAMS MANUAL -->
    <div v-show="activeTab === 'teams'" class="manual-content">
      <h2 id="teams-overview">{{ $t('manual.sections.teamsOverview') }}</h2>
      <p class="lead">{{ $t('manual.teams.overview') }}</p>

      <section id="teams-index">
        <h3>{{ $t('manual.sections.teamsIndexPage') }}</h3>
        <p><strong>URL:</strong> <code>{{ $t('manual.teams.indexUrl') }}</code></p>

        <h4>{{ $t('manual.teams.searchFilter') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.teams.searchBar') }}:</strong> {{ $t('manual.teams.searchBarDesc') }}</li>
          <li><strong>{{ $t('manual.teams.filtersButton') }}:</strong> {{ $t('manual.teams.filtersButtonDesc') }}
            <ul>
              <li><strong>{{ $t('manual.teams.seasonFilter') }}:</strong> {{ $t('manual.teams.seasonFilterDesc') }}</li>
              <li>{{ $t('manual.teams.multipleFilters') }}</li>
              <li><strong>{{ $t('manual.teams.clearFilters') }}:</strong> {{ $t('manual.teams.clearFiltersDesc') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.teams.itemCounter') }}:</strong> {{ $t('manual.teams.itemCounterDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.teams.teamCards') }}</h4>
        <p>{{ $t('manual.teams.teamCardsDesc') }}</p>
      </section>

      <section id="individual-team">
        <h3>{{ $t('manual.sections.individualTeamPage') }}</h3>
        <p><strong>URL:</strong> <code>{{ $t('manual.teams.individualTeamUrl') }}</code></p>

        <h4 id="team-logo">{{ $t('manual.teams.logoSection') }}</h4>
        <ul>
          <li>{{ $t('manual.teams.logoDisplay') }}</li>
          <li>{{ $t('manual.teams.logoBackground') }}</li>
          <li>{{ $t('manual.teams.logoPattern') }}</li>
        </ul>

        <h4 id="season-selection">{{ $t('manual.teams.seasonSelectionHeading') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.teams.seasonCards') }}:</strong> {{ $t('manual.teams.seasonCardsDesc') }}</li>
          <li><strong>{{ $t('manual.teams.allSeasonsButton') }}:</strong> {{ $t('manual.teams.allSeasonsButtonDesc') }}</li>
          <li>{{ $t('manual.teams.selectedSeason') }}</li>
        </ul>

        <h4 id="team-statistics">{{ $t('manual.teams.statsDashboardHeading') }}</h4>
        <p>{{ $t('manual.teams.statsHeader') }}</p>
        <ul>
          <li><strong>{{ $t('manual.teams.formationsCard') }}:</strong> {{ $t('manual.teams.formationsCardDesc') }}
            <ul>
              <li>{{ $t('manual.teams.formationClick') }}</li>
              <li>{{ $t('manual.teams.formationExpandable') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.teams.matchesOverview') }}:</strong> {{ $t('manual.teams.matchesOverviewDesc') }}</li>
          <li><strong>{{ $t('manual.teams.goalsPerformance') }}:</strong> {{ $t('manual.teams.goalsPerformanceDesc') }}</li>
          <li><strong>{{ $t('manual.teams.streaks') }}:</strong> {{ $t('manual.teams.streaksDesc') }}</li>
          <li><strong>{{ $t('manual.teams.clearStatsButton') }}:</strong> {{ $t('manual.teams.clearStatsButtonDesc') }}</li>
        </ul>

        <h4 id="team-matches">{{ $t('manual.teams.matchesDashboardHeading') }}</h4>
        <p>{{ $t('manual.teams.matchesOverview') }}</p>
        <ul>
          <li><strong>{{ $t('manual.teams.venueFilter') }}:</strong> {{ $t('manual.teams.venueFilterDesc') }}</li>
          <li><strong>{{ $t('manual.teams.refereeFilter') }}:</strong> {{ $t('manual.teams.refereeFilterDesc') }}</li>
          <li><strong>{{ $t('manual.teams.matchesTable') }}:</strong> {{ $t('manual.teams.matchesTableDesc') }}</li>
          <li><strong>{{ $t('manual.teams.matchColumns') }}:</strong>
            <ul>
              <li>{{ $t('manual.teams.colDate') }}: {{ $t('manual.teams.colDateDesc') }}</li>
              <li>{{ $t('manual.teams.colRound') }}: {{ $t('manual.teams.colRoundDesc') }}</li>
              <li>{{ $t('manual.teams.colTeams') }}: {{ $t('manual.teams.colTeamsDesc') }}</li>
              <li>{{ $t('manual.teams.colScore') }}: {{ $t('manual.teams.colScoreDesc') }}</li>
              <li>{{ $t('manual.teams.colVenue') }}: {{ $t('manual.teams.colVenueDesc') }}</li>
              <li>{{ $t('manual.teams.colReferee') }}: {{ $t('manual.teams.colRefereeDesc') }}</li>
              <li>{{ $t('manual.teams.colStatus') }}: {{ $t('manual.teams.colStatusDesc') }}</li>
            </ul>
          </li>
        </ul>
      </section>

      <section id="metrics-dashboard">
        <h4 id="metrics-dashboard">{{ $t('manual.teams.metricsDashboardHeading') }}</h4>
        <p>{{ $t('manual.teams.metricsAdvanced') }}</p>
        <ul>
          <li><strong>{{ $t('manual.teams.metricSelection') }}:</strong>
            <ul>
              <li>{{ $t('manual.teams.metricSelectionDesc') }}</li>
              <li>{{ $t('manual.teams.metricConfirm') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.teams.seasonMetricFilter') }}:</strong> {{ $t('manual.teams.seasonMetricFilterDesc') }}</li>
          <li><strong>{{ $t('manual.teams.chartTypes') }}:</strong> {{ $t('manual.teams.chartTypesDesc') }}</li>
          <li><strong>{{ $t('manual.teams.sharedGraphs') }}:</strong> {{ $t('manual.teams.sharedGraphsDesc') }}</li>
        </ul>
      </section>
      <section id="navigation-tips">
        <h3>{{ $t('manual.sections.navigationTips') }}</h3>
        <ul>
          <li><strong>{{ $t('manual.teams.pageNavigator') }}:</strong> {{ $t('manual.teams.pageNavigatorDesc') }}</li>
          <li><strong>{{ $t('manual.teams.autoScroll') }}:</strong> {{ $t('manual.teams.autoScrollDesc') }}</li>
          <li><strong>{{ $t('manual.teams.hoverEffects') }}:</strong> {{ $t('manual.teams.hoverEffectsDesc') }}</li>
          <li><strong>{{ $t('manual.teams.responsive') }}:</strong> {{ $t('manual.teams.responsiveDesc') }}</li>
        </ul>
      </section>
    </div>
    <!-- PLAYERS MANUAL -->
    <div v-show="activeTab === 'players'" class="manual-content">
      <h2 id="players-overview">{{ $t('manual.sections.playersOverview') }}</h2>
      <p class="lead">{{ $t('manual.players.overview') }}</p>

      <section id="players-index">
        <h3>{{ $t('manual.sections.playersIndexPage') }}</h3>
        <p><strong>URL:</strong> <code>{{ $t('manual.players.indexUrl') }}</code></p>

        <h4>{{ $t('manual.teams.searchFilter') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.teams.searchBar') }}:</strong> {{ $t('manual.players.searchPlaceholder') }}</li>
          <li><strong>{{ $t('manual.teams.filtersButton') }}:</strong> {{ $t('manual.teams.filtersButtonDesc') }}
            <ul>
              <li><strong>{{ $t('manual.teams.seasonFilter') }}:</strong> {{ $t('manual.teams.seasonFilterDesc') }}</li>
              <li><strong>{{ $t('manual.players.teamFilter') }}:</strong> {{ $t('manual.players.teamFilterDesc') }}</li>
              <li>{{ $t('manual.teams.multipleFilters') }}</li>
              <li><strong>{{ $t('manual.teams.clearFilters') }}:</strong> {{ $t('manual.teams.clearFiltersDesc') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.teams.itemCounter') }}:</strong> {{ $t('manual.teams.itemCounterDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.teams.teamCards') }}</h4>
        <p>{{ $t('manual.teams.teamCardsDesc') }}</p>
      </section>

      <section id="individual-player">
        <h3>{{ $t('manual.sections.individualPlayerPage') }}</h3>
        <p><strong>URL:</strong> <code>/players/[player_id]</code></p>

        <h4 id="player-information">{{ $t('manual.players.playerInfoHeading') }}</h4>
        <ul>
          <li>{{ $t('manual.players.playerName') }}</li>
          <li><strong>{{ $t('manual.players.infoTable') }}:</strong> {{ $t('manual.players.infoTableDesc') }}</li>
          <li>{{ $t('manual.players.hoverRows') }}</li>
        </ul>

        <h4 id="player-season-selection">{{ $t('manual.players.playerSeasonSelectionHeading') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.players.playerSeasonCards') }}:</strong> {{ $t('manual.players.playerSeasonCardsDesc') }}</li>
          <li><strong>{{ $t('manual.players.playerAllSeasons') }}:</strong> {{ $t('manual.players.playerAllSeasonsDesc') }}</li>
          <li>{{ $t('manual.players.playerAutoLoad') }}</li>
        </ul>

        <h4 id="player-statistics">{{ $t('manual.players.playerStatsHeading') }}</h4>
        <p>{{ $t('manual.players.playerStatsExpand') }}</p>
        <ul>
          <li><strong>{{ $t('manual.players.games') }}:</strong>
            <ul><li>{{ $t('manual.players.gamesDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.players.goalsAssists') }}:</strong>
            <ul><li>{{ $t('manual.players.goalsAssistsDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.players.defensiveStats') }}:</strong>
            <ul><li>{{ $t('manual.players.defensiveStatsDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.players.passingStats') }}:</strong>
            <ul><li>{{ $t('manual.players.passingStatsDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.teams.streaks') }}:</strong>
            <ul><li>{{ $t('manual.players.duelsDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.teams.discipline') }}:</strong>
            <ul><li>{{ $t('manual.players.disciplineDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.players.penalties') }}:</strong>
            <ul><li>{{ $t('manual.players.penaltiesDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.players.goalkeeperStats') }}:</strong>
            <ul><li>{{ $t('manual.players.goalkeeperStatsDesc') }}</li></ul>
          </li>
        </ul>

        <p><strong>{{ $t('manual.players.noDataCategory') }}:</strong> {{ $t('manual.players.noDataCategoryDesc') }}</p>

        <h4 id="player-metrics">{{ $t('manual.players.playerMetricsHeading') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.players.playerMetricMulti') }}:</strong> {{ $t('manual.players.playerMetricMultiDesc') }}</li>
          <li><strong>{{ $t('manual.players.playerMetricSeason') }}:</strong> {{ $t('manual.players.playerMetricSeasonDesc') }}</li>
          <li><strong>{{ $t('manual.players.playerMetricChart') }}:</strong> {{ $t('manual.players.playerMetricChartDesc') }}</li>
          <li><strong>{{ $t('manual.players.playerClearStats') }}:</strong> {{ $t('manual.players.playerClearStatsDesc') }}</li>
        </ul>
      </section>

      <section id="color-coding">
        <h3>{{ $t('manual.sections.colorCoding') }}</h3>
        <ul>
          <li><strong>{{ $t('manual.players.colorGreen') }}:</strong> {{ $t('manual.players.colorGreenDesc') }}</li>
          <li><strong>{{ $t('manual.players.colorRed') }}:</strong> {{ $t('manual.players.colorRedDesc') }}</li>
          <li><strong>{{ $t('manual.players.colorYellow') }}:</strong> {{ $t('manual.players.colorYellowDesc') }}</li>
        </ul>
      </section>
    </div>
    <!-- SEASONS MANUAL -->
    <div v-show="activeTab === 'seasons'" class="manual-content">
      <h2 id="seasons-overview">{{ $t('manual.sections.seasonsOverview') }}</h2>
      <p class="lead">{{ $t('manual.seasons.overview') }}</p>

      <section id="seasons-index">
        <h3>{{ $t('manual.sections.seasonsIndexPage') }}</h3>
        <p><strong>URL:</strong> <code>{{ $t('manual.seasons.indexUrl') }}</code></p>

        <h4>{{ $t('manual.seasons.features') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.seasons.searchSeason') }}:</strong> {{ $t('manual.seasons.searchSeasonDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.seasonCards') }}:</strong> {{ $t('manual.seasons.seasonCardsDesc') }}</li>
          <li>{{ $t('manual.seasons.seasonClick') }}</li>
          <li><strong>{{ $t('manual.seasons.noSeasonFilters') }}:</strong> {{ $t('manual.seasons.noSeasonFiltersDesc') }}</li>
        </ul>
      </section>

      <section id="individual-season">
        <h3>{{ $t('manual.sections.individualSeasonPage') }}</h3>
        <p><strong>URL:</strong> <code>/seasons/[season_id]</code></p>

        <h4 id="season-stats-section">{{ $t('manual.seasons.statsHeading') }}</h4>
        <p>{{ $t('manual.seasons.statsComprehensive') }}</p>
        <ul>
          <li><strong>{{ $t('manual.seasons.seasonHeader') }}:</strong>
            <ul>
              <li>{{ $t('manual.seasons.seasonHeaderContent').split(',')[0] }}</li>
              <li>{{ $t('manual.seasons.seasonHeaderContent').split(',')[1] }}</li>
              <li>{{ $t('manual.seasons.seasonHeaderContent').split(',')[2] }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.seasons.overviewCards') }}:</strong>
            <ul>
              <li>{{ $t('manual.seasons.overviewCardsContent').split(',')[0] }}</li>
              <li>{{ $t('manual.seasons.overviewCardsContent').split(',')[1] }}</li>
              <li>{{ $t('manual.seasons.overviewCardsContent').split(',')[2] }}</li>
              <li>{{ $t('manual.seasons.overviewCardsContent').split(',')[3] }}</li>
            </ul>
          </li>
        </ul>

        <h4>{{ $t('manual.seasons.detailedStats') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.seasons.shooting') }}:</strong>
            <ul><li>{{ $t('manual.seasons.shootingDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.seasons.passing') }}:</strong>
            <ul><li>{{ $t('manual.seasons.passingDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.players.duelsDesc') }}:</strong>
            <ul><li>{{ $t('manual.seasons.duelsDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.teams.discipline') }}:</strong>
            <ul><li>{{ $t('manual.seasons.disciplineDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.players.penalties') }}:</strong>
            <ul><li>{{ $t('manual.seasons.penaltiesDesc') }}</li></ul>
          </li>
          <li><strong>{{ $t('manual.seasons.defense') }}:</strong>
            <ul><li>{{ $t('manual.seasons.defenseDesc') }}</li></ul>
          </li>
        </ul>

        <h4 id="season-ranking">{{ $t('manual.sections.seasonRanking') }}</h4>
        <p>{{ $t('manual.seasons.rankingInteractive') }}</p>

        <ul>
          <li><strong>{{ $t('manual.seasons.tableHeader') }}:</strong>
            <ul>
              <li>{{ $t('manual.seasons.tableHeaderContent').split(',')[0] }}</li>
              <li>{{ $t('manual.seasons.tableHeaderContent').split(',')[1] }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.seasons.sortOptions') }}:</strong>
            <ul>
              <li><strong>{{ $t('manual.seasons.sortPoints') }}:</strong> {{ $t('manual.seasons.sortPointsDesc') }}</li>
              <li><strong>{{ $t('manual.seasons.sortWins') }}:</strong> {{ $t('manual.seasons.sortWinsDesc') }}</li>
              <li><strong>{{ $t('manual.seasons.sortGoalDiff') }}:</strong> {{ $t('manual.seasons.sortGoalDiffDesc') }}</li>
              <li><strong>{{ $t('manual.seasons.sortGoalsScored') }}:</strong> {{ $t('manual.seasons.sortGoalsScoredDesc') }}</li>
              <li><strong>{{ $t('manual.seasons.sortGoalsConceded') }}:</strong> {{ $t('manual.seasons.sortGoalsConcededDesc') }}</li>
              <li><strong>{{ $t('manual.seasons.sortMatches') }}:</strong> {{ $t('manual.seasons.sortMatchesDesc') }}</li>
              <li><strong>{{ $t('manual.seasons.sortDraws') }}:</strong> {{ $t('manual.seasons.sortDrawsDesc') }}</li>
              <li><strong>{{ $t('manual.seasons.sortLosses') }}:</strong> {{ $t('manual.seasons.sortLossesDesc') }}</li>
              <li><strong>{{ $t('manual.seasons.sortWinRate') }}:</strong> {{ $t('manual.seasons.sortWinRateDesc') }}</li>
              <li><strong>{{ $t('manual.seasons.sortPtsMatch') }}:</strong> {{ $t('manual.seasons.sortPtsMatchDesc') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.seasons.sorting') }}:</strong>
            <ul>
              <li>{{ $t('manual.seasons.sortingDesc').split(',')[0] }}</li>
              <li>{{ $t('manual.seasons.sortingDesc').split(',')[1] }}</li>
              <li>{{ $t('manual.seasons.sortingDesc').split(',')[2] }}</li>
              <li>{{ $t('manual.seasons.sortingDesc').split(',')[3] }}</li>
            </ul>
          </li>
        </ul>

        <h4>{{ $t('manual.seasons.rankingTableColumns') }}</h4>
        <ul>
          <li>
            <strong>{{ $t('manual.seasons.colRank') }}:</strong> {{ $t('manual.seasons.colRankDesc') }}
            <ul>
              <li>
                <Icon icon="mdi:trophy" class="icon-gold" />
                {{ $t('manual.seasons.topHighlightDesc').split(',')[0] }}
              </li>
              <li>
                <Icon icon="mdi:trophy" class="icon-silver" />
                {{ $t('manual.seasons.topHighlightDesc').split(',')[1] }}
              </li>
              <li>
                <Icon icon="mdi:trophy" class="icon-bronze" />
                {{ $t('manual.seasons.topHighlightDesc').split(',')[2] }}
              </li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.seasons.colTeam') }}:</strong> {{ $t('manual.seasons.colTeamDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.colMP') }}:</strong> {{ $t('manual.seasons.colMPDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.colW') }}:</strong> {{ $t('manual.seasons.colWDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.colD') }}:</strong> {{ $t('manual.seasons.colDDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.colL') }}:</strong> {{ $t('manual.seasons.colLDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.colGF') }}:</strong> {{ $t('manual.seasons.colGFDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.colGA') }}:</strong> {{ $t('manual.seasons.colGADesc') }}</li>
          <li><strong>{{ $t('manual.seasons.colGD') }}:</strong> {{ $t('manual.seasons.colGDDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.colPts') }}:</strong> {{ $t('manual.seasons.colPtsDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.colPM') }}:</strong> {{ $t('manual.seasons.colPMDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.colWPct') }}:</strong> {{ $t('manual.seasons.colWPctDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.seasons.visualFeatures') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.seasons.formBars') }}:</strong> {{ $t('manual.seasons.formBarsDesc') }}
            <ul>
              <li>{{ $t('manual.seasons.formGreen') }}</li>
              <li>{{ $t('manual.seasons.formYellow') }}</li>
              <li>{{ $t('manual.seasons.formOrange') }}</li>
              <li>{{ $t('manual.seasons.formRed') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.seasons.topHighlight') }}:</strong> {{ $t('manual.seasons.topHighlightDesc') }}</li>
          <li><strong>{{ $t('manual.teams.hoverEffects') }}:</strong> {{ $t('manual.seasons.hoverRowsDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.responsiveTable') }}:</strong> {{ $t('manual.seasons.responsiveTableDesc') }}</li>
        </ul>
      </section>

      <section id="season-matches">
        <h3>{{ $t('manual.sections.seasonMatches') }}</h3>
        <p>{{ $t('manual.seasons.matchesDescription') }}</p>
        <ul>
          <li><strong>{{ $t('manual.seasons.expandMatches') }}:</strong> {{ $t('manual.seasons.expandMatchesDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.teamFilter') }}:</strong> {{ $t('manual.seasons.teamFilterDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.refereeFilter') }}:</strong> {{ $t('manual.seasons.refereeFilterDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.matchesDisplayed') }}:</strong> {{ $t('manual.seasons.matchesDisplayedDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.matchTableColumns') }}:</strong>
            <ul>
              <li>{{ $t('manual.seasons.dateColumn') }}: {{ $t('manual.seasons.dateColumnDesc') }}</li>
              <li>{{ $t('manual.seasons.roundColumn') }}: {{ $t('manual.seasons.roundColumnDesc') }}</li>
              <li>{{ $t('manual.seasons.teamsColumn') }}: {{ $t('manual.seasons.teamsColumnDesc') }}</li>
              <li>{{ $t('manual.seasons.scoreColumn') }}: {{ $t('manual.seasons.scoreColumnDesc') }}</li>
              <li>{{ $t('manual.seasons.venueColumn') }}: {{ $t('manual.seasons.venueColumnDesc') }}</li>
              <li>{{ $t('manual.seasons.refereeColumn') }}: {{ $t('manual.seasons.refereeColumnDesc') }}</li>
              <li>{{ $t('manual.seasons.statusColumn') }}: {{ $t('manual.seasons.statusColumnDesc') }}</li>
            </ul>
          </li>
        </ul>
      </section>

      <section id="season-navigation">
        <h3>{{ $t('manual.sections.seasonNavigation') }}</h3>
        <ul>
          <li><strong>{{ $t('manual.seasons.navigationSeasonNav') }}:</strong> {{ $t('manual.seasons.navigationSeasonNavDesc') }}</li>
        </ul>
      </section>

      <section id="usage-tips">
        <h3>{{ $t('manual.sections.usageTips') }}</h3>
        <ul>
          <li><strong>{{ $t('manual.seasons.compareTeams') }}:</strong> {{ $t('manual.seasons.compareTeamsDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.defensiveAnalysis') }}:</strong> {{ $t('manual.seasons.defensiveAnalysisDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.attackingAnalysis') }}:</strong> {{ $t('manual.seasons.attackingAnalysisDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.efficiency') }}:</strong> {{ $t('manual.seasons.efficiencyDesc') }}</li>
          <li><strong>{{ $t('manual.seasons.formAnalysis') }}:</strong> {{ $t('manual.seasons.formAnalysisDesc') }}</li>
        </ul>
      </section>
    </div>
    <!-- COMPARE MANUAL -->
    <div v-show="activeTab === 'compare'" class="manual-content">
      <h2 id="compare-overview">{{ $t('manual.sections.compareOverview') }}</h2>
      <p class="lead">{{ $t('manual.compare.overview') }}</p>

      <section id="compare-index">
        <h3>{{ $t('manual.sections.compareIndex') }}</h3>
        <p><strong>URL:</strong> <code>{{ $t('manual.compare.indexUrl') }}</code></p>

        <h4>{{ $t('manual.compare.indexOverview') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.compareSeasonsFull') }}:</strong> {{ $t('manual.compare.compareSeasonFullDesc') }}</li>
          <li><strong>{{ $t('manual.compare.compareTeamsFull') }}:</strong> {{ $t('manual.compare.compareTeamsFullDesc') }}</li>
          <li><strong>{{ $t('manual.compare.comparePlayersFull') }}:</strong> {{ $t('manual.compare.comparePlayersFullDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.gettingStarted') }}</h4>
        <ol>
          <li>{{ $t('manual.compare.step1') }}</li>
          <li>{{ $t('manual.compare.step2') }}</li>
          <li>{{ $t('manual.compare.step3') }}</li>
        </ol>
      </section>

      <section id="pages-structure">
        <h3>{{ $t('manual.sections.pagesStructure') }}</h3>
        <p><strong>{{ $t('manual.compare.structureUrls') }}:</strong></p>
        <ul>
          <li><code>{{ $t('manual.compare.urlSeasonComp') }}</code> - {{ $t('manual.compare.urlSeasonCompDesc') }}</li>
          <li><code>{{ $t('manual.compare.urlTeamComp') }}</code> - {{ $t('manual.compare.urlTeamCompDesc') }}</li>
          <li><code>{{ $t('manual.compare.urlPlayerComp') }}</code> - {{ $t('manual.compare.urlPlayerCompDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.pageLayout') }}</h4>
        <p>{{ $t('manual.compare.layoutConsistent') }}</p>
        <ol>
          <li><strong>{{ $t('manual.compare.layoutSelection') }}</strong></li>
          <li><strong>{{ $t('manual.compare.layoutStats') }}</strong></li>
        </ol>
      </section>

      <section id="season-comparison">
        <h3>{{ $t('manual.sections.seasonComparison') }}</h3>
        <p><strong>URL:</strong> <code>{{ $t('manual.compare.seasonUrl') }}</code></p>

        <h4>{{ $t('manual.compare.step1SelectSeasons') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.twoDropdowns') }}:</strong> {{ $t('manual.compare.twoDropdownsDesc') }}</li>
          <li><strong>{{ $t('manual.compare.leftDropdown') }}:</strong> {{ $t('manual.compare.leftDropdownDesc') }}</li>
          <li><strong>{{ $t('manual.compare.rightDropdown') }}:</strong> {{ $t('manual.compare.rightDropdownDesc') }}</li>
          <li>{{ $t('manual.compare.bothSeasons') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.selectionRules') }}</h4>
        <ul>
          <li>
            <Icon icon="mdi:close-circle" class="icon-error" />
            <strong>{{ $t('manual.compare.sameSeasonError') }}</strong> — {{ $t('manual.compare.sameSeasonErrorMsg') }}
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.selectBothSeasons') }}
          </li>
          <li>{{ $t('manual.compare.urlParams') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.step2ViewResults') }}</h4>
        <p>{{ $t('manual.compare.onceBothSelected') }}</p>

        <h5>{{ $t('manual.compare.comparisonHeader') }}</h5>
        <ul>
          <li><strong>{{ $t('manual.compare.headerLayout') }}:</strong> {{ $t('manual.compare.headerFormat') }}</li>
          <li>{{ $t('manual.compare.headerStyling') }}</li>
        </ul>

        <h5>{{ $t('manual.compare.winnerBanner') }}</h5>
        <p>{{ $t('manual.compare.winnerDisplay') }}</p>
        <ul>
          <li><strong>{{ $t('manual.compare.winnerAnnouncement') }}:</strong>
            <ul>
              <li>
                <Icon icon="mdi:crown" class="icon-gold" />
                <strong>{{ $t('manual.compare.winnerText') }}</strong>
              </li>
              <li>
                <Icon icon="mdi:handshake" class="icon-muted" />
                <strong>{{ $t('manual.compare.tieText') }}</strong>
              </li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.winBreakdown') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.winMetric1') }}</li>
              <li>{{ $t('manual.compare.winMetric2') }}</li>
              <li>{{ $t('manual.compare.winMetric3') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.visualBar') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.barDesc') }}</li>
              <li>{{ $t('manual.compare.barLeft') }}</li>
              <li>{{ $t('manual.compare.barRight') }}</li>
              <li>{{ $t('manual.compare.barPercentages') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.bannerColor') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.bannerWinner') }}</li>
              <li>{{ $t('manual.compare.bannerTie') }}</li>
            </ul>
          </li>
        </ul>

        <h5>{{ $t('manual.compare.metricsGrid') }}</h5>
        <p>{{ $t('manual.compare.gridOrganized') }}</p>

        <div class="metric-category">
          <h6>
            <Icon icon="mdi:soccer" class="icon-category" />
            {{ $t('manual.compare.seasonOverview') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.seasonOverviewDesc') }}</li>
          </ul>
        </div>

        <div class="metric-category">
          <h6>
            <Icon icon="mdi:target" class="icon-category" />
            {{ $t('manual.compare.attacking') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.attackingDesc') }}</li>
          </ul>
        </div>

        <div class="metric-category">
          <h6>
            <Icon icon="mdi:arrow-decision" class="icon-category" />
            {{ $t('manual.compare.passing') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.passingDesc') }}</li>
          </ul>
        </div>

        <div class="metric-category">
          <h6>
            <Icon icon="mdi:lightning-bolt" class="icon-category" />
            {{ $t('manual.compare.duelsDribbles') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.duelsDribblesDesc') }}</li>
          </ul>
        </div>

        <div class="metric-category">
          <h6>
            <Icon icon="mdi:shield-half-full" class="icon-category" />
            {{ $t('manual.compare.defensive') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.defensiveDesc') }}</li>
          </ul>
        </div>

        <div class="metric-category">
          <h6>
            <Icon icon="mdi:card-account-details" class="icon-category" />
            {{ $t('manual.compare.discipline') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.disciplineDesc') }}</li>
          </ul>
        </div>

        <div class="metric-category">
          <h6>
            <Icon icon="mdi:soccer-field" class="icon-category" />
            {{ $t('manual.compare.penaltiesComp') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.penaltiesCompDesc') }}</li>
          </ul>
        </div>

        <h5>{{ $t('manual.compare.readingGrid') }}</h5>
        <ul>
          <li><strong>{{ $t('manual.compare.layoutMetric') }}:</strong>
            <pre>First Value | Metric Label | Second Value</pre>
          </li>
          <li><strong>{{ $t('manual.compare.winnerHighlight') }}:</strong>
            <ul>
              <li>
                <Icon icon="mdi:trophy" class="icon-gold" />
                <strong>{{ $t('manual.compare.boldHighlight') }}</strong>
              </li>
              <li>{{ $t('manual.compare.regularStyling') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.colorCoding') }}:</strong>
            <ul>
              <li>
                <Icon icon="mdi:circle" class="icon-success" />
                <span style="color: #22c55e;">{{ $t('manual.compare.codeGreen') }}</span>
              </li>
              <li>
                <Icon icon="mdi:circle" class="icon-error" />
                <span style="color: #ef4444;">{{ $t('manual.compare.codeRed') }}</span>
              </li>
              <li>
                <Icon icon="mdi:circle" class="icon-warning" />
                <span style="color: #eab308;">{{ $t('manual.compare.codeYellow') }}</span>
              </li>
              <li>{{ $t('manual.compare.codeWhite') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.missingData') }}:</strong> {{ $t('manual.compare.missingDataDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.lowerBetter') }}</h4>
        <p>
          <Icon icon="mdi:arrow-down-bold" class="icon-warning" />
          {{ $t('manual.compare.lowerMetrics') }}
        </p>
        <ul>
          <li>{{ $t('manual.compare.lowerExamples') }}</li>
          <li>{{ $t('manual.compare.lowerWins') }}</li>
          <li>{{ $t('manual.compare.lowerExample') }}</li>
        </ul>
      </section>

      <section id="team-comparison">
        <h3>{{ $t('manual.sections.teamComparison') }}</h3>
        <p><strong>URL:</strong> <code>{{ $t('manual.compare.teamUrl') }}</code></p>

        <h4>{{ $t('manual.compare.step1SelectTeams') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.twoSearchableDropdowns') }}:</strong> {{ $t('manual.compare.twoSearchableDesc') }}</li>
          <li><strong>{{ $t('manual.compare.howToUse') }}:</strong>
            <ol>
              <li>{{ $t('manual.compare.useStep1') }}</li>
              <li>{{ $t('manual.compare.useStep2') }}</li>
              <li>{{ $t('manual.compare.useStep3') }}</li>
              <li>{{ $t('manual.compare.useStep4') }}</li>
              <li>
                <Icon icon="mdi:close-circle" class="icon-error" />
                {{ $t('manual.compare.useStep5') }}
              </li>
              <li>{{ $t('manual.compare.useStep6') }}</li>
            </ol>
          </li>
          <li><strong>{{ $t('manual.compare.visualIndicators') }}:</strong>
            <ul>
              <li>
                <Icon icon="mdi:chevron-down" class="icon-muted" />
                {{ $t('manual.compare.indicatorDown') }}
              </li>
              <li>
                <Icon icon="mdi:chevron-up" class="icon-muted" />
                {{ $t('manual.compare.indicatorUp') }}
              </li>
              <li>
                <Icon icon="mdi:close" class="icon-muted" />
                {{ $t('manual.compare.indicatorX') }}
              </li>
            </ul>
          </li>
        </ul>

        <h4>{{ $t('manual.compare.step2SelectSeasons') }}</h4>
        <p><strong>{{ $t('manual.compare.afterTeamsSelected') }}</strong></p>
        <ul>
          <li><strong>{{ $t('manual.compare.seasonSelectors') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.seasonShowsOnly') }}</li>
              <li>{{ $t('manual.compare.seasonOption') }}</li>
              <li>{{ $t('manual.compare.seasonIndividual') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.independentSeasons') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.eachTeamDesc') }}</li>
              <li>{{ $t('manual.compare.exampleComp') }}</li>
              <li>{{ $t('manual.compare.exampleOr') }}</li>
            </ul>
          </li>
        </ul>

        <h4>{{ $t('manual.compare.teamSelectionRules') }}</h4>
        <ul>
          <li>
            <Icon icon="mdi:close-circle" class="icon-error" />
            <strong>{{ $t('manual.compare.cantCompareTeam') }}</strong> — {{ $t('manual.compare.cantCompareTeamMsg') }}
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.selectBothTeams') }}
          </li>
          <li>{{ $t('manual.compare.urlTeamSelect') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.step3ViewTeamResults') }}</h4>

        <h5>{{ $t('manual.compare.teamComparisonHeader') }}</h5>
        <ul>
          <li><strong>{{ $t('manual.compare.teamHeaderLayout') }}:</strong> {{ $t('manual.compare.teamHeaderNames') }}</li>
          <li>{{ $t('manual.compare.vsBadge') }}</li>
        </ul>

        <h5>{{ $t('manual.compare.teamWinnerBanner') }}</h5>
        <p>{{ $t('manual.compare.sameAsSeasonComp') }}</p>
        <ul>
          <li>
            <Icon icon="mdi:crown" class="icon-gold" />
            {{ $t('manual.compare.teamWinnerBadge') }}
          </li>
          <li>{{ $t('manual.compare.teamWinCount') }}</li>
          <li>{{ $t('manual.compare.teamDualColor') }}</li>
        </ul>

        <h5>{{ $t('manual.compare.teamMetrics') }}</h5>
        <p>{{ $t('manual.compare.organized3') }}</p>

        <div class="metric-category">
          <h6>
            <Icon icon="mdi:soccer" class="icon-category" />
            {{ $t('manual.compare.matchesOverview') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.matchesOverviewDesc') }}</li>
          </ul>
        </div>

        <div class="metric-category">
          <h6>
            <Icon icon="mdi:target" class="icon-category" />
            {{ $t('manual.compare.goalsPerformance') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.goalsPerformanceDesc') }}</li>
          </ul>
        </div>
        <div class="metric-category">
          <h6>
            <Icon icon="mdi:trending-up" class="icon-category" />
            {{ $t('manual.compare.streaks') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.streaksDesc') }}</li>
          </ul>
        </div>
        <h5>{{ $t('manual.compare.formationsSection') }}</h5>
        <p>{{ $t('manual.compare.tacticalsFormations') }}</p>
        <ul>
          <li><strong>{{ $t('manual.compare.sideColumns') }}:</strong> {{ $t('manual.compare.sideColumnsDesc') }}</li>
          <li><strong>{{ $t('manual.compare.formationList') }}:</strong> {{ $t('manual.compare.formationListDesc') }}</li>
          <li><strong>{{ $t('manual.compare.matchFormationCount') }}:</strong> {{ $t('manual.compare.matchFormationCountDesc') }}</li>
          <li><strong>{{ $t('manual.compare.expandable') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.expandableDesc') }}</li>
              <li>{{ $t('manual.compare.showsLineup') }}</li>
              <li>
                <Icon icon="mdi:chevron-down" class="icon-muted" />
                {{ $t('manual.compare.arrowRotates') }}
              </li>
              <li>{{ $t('manual.compare.clickCollapse') }}</li>
            </ul>
          </li>
        </ul>
        <h5>{{ $t('manual.compare.recentForm') }}</h5>
        <p>{{ $t('manual.compare.visualForm') }}</p>
        <ul>
          <li><strong>{{ $t('manual.compare.sideDisplay') }}:</strong> {{ $t('manual.compare.sideDisplayDesc') }}</li>
          <li><strong>{{ $t('manual.compare.formBadges') }}:</strong>
            <ul>
              <li><span style="background: #22c55e; padding: 2px 6px; border-radius: 3px;">W</span> {{ $t('manual.compare.winBadge') }}</li>
              <li><span style="background: #eab308; padding: 2px 6px; border-radius: 3px;">D</span> {{ $t('manual.compare.drawBadge') }}</li>
              <li><span style="background: #ef4444; padding: 2px 6px; border-radius: 3px;">L</span> {{ $t('manual.compare.lossBadge') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.readingDirection') }}:</strong> {{ $t('manual.compare.readingDirectionDesc') }}</li>
          <li><strong>{{ $t('manual.compare.hoverScale') }}:</strong> {{ $t('manual.compare.hoverScaleDesc') }}</li>
        </ul>
        <h5>{{ $t('manual.compare.penaltiesSection') }}</h5>
        <p>{{ $t('manual.compare.penaltyKicks') }}</p>
        <ul>
          <li><strong>{{ $t('manual.compare.twoTeamColumns') }}:</strong> {{ $t('manual.compare.twoTeamColumnsDesc') }}</li>
          <li><strong>{{ $t('manual.compare.penaltyScored') }}:</strong> {{ $t('manual.compare.penaltyScoredDesc') }}</li>
          <li><strong>{{ $t('manual.compare.penaltyMissed') }}:</strong> {{ $t('manual.compare.penaltyMissedDesc') }}</li>
        </ul>
      </section>
      <section id="player-comparison">
        <h3>{{ $t('manual.sections.playerComparison') }}</h3>
        <p><strong>URL:</strong> <code>{{ $t('manual.compare.playerUrl') }}</code></p>

        <h4>{{ $t('manual.compare.step1SelectPlayers') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.twoSearchablePlayers') }}:</strong> {{ $t('manual.compare.twoSearchablePlayersDesc') }}</li>
          <li><strong>{{ $t('manual.compare.searchFunctionality') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.typeNames') }}</li>
              <li>{{ $t('manual.compare.caseInsensitive') }}</li>
              <li>{{ $t('manual.compare.partialNames') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.clearSelection') }}:</strong> {{ $t('manual.compare.clearSelectionDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.step2PlayerSeasons') }}</h4>
        <p>{{ $t('manual.compare.afterPlayersSelected') }}</p>
        <ul>
          <li><strong>{{ $t('manual.compare.seasonDropsAppear') }}:</strong> {{ $t('manual.compare.onePerPlayer') }}</li>
          <li><strong>{{ $t('manual.compare.seasonOptionsPlayer') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.allSeasonsCareer') }}</li>
              <li>{{ $t('manual.compare.individualSeasonsPlayer') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.mixAndMatch') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.playerMix1') }}</li>
              <li>{{ $t('manual.compare.playerMix2') }}</li>
              <li>{{ $t('manual.compare.playerMix3') }}</li>
            </ul>
          </li>
        </ul>
        <h4>{{ $t('manual.compare.playerSelectionRules') }}</h4>
        <ul>
          <li>
            <Icon icon="mdi:close-circle" class="icon-error" />
            <strong>{{ $t('manual.compare.cantCompareSelf') }}</strong>
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.selectBothPlayers') }}
          </li>
          <li>{{ $t('manual.compare.urlPlayerSelect') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.step3ViewPlayerResults') }}</h4>
        <h5>{{ $t('manual.compare.playerComparisonHeader') }}</h5>
        <ul>
          <li>{{ $t('manual.compare.playerHeaderLayout') }}</li>
          <li>{{ $t('manual.compare.cleanDisplay') }}</li>
        </ul>

        <h5>{{ $t('manual.compare.playerWinnerBanner') }}</h5>
        <ul>
          <li>{{ $t('manual.compare.calculatesAcross') }}</li>
          <li>{{ $t('manual.compare.totalWins') }}</li>
          <li>{{ $t('manual.compare.percentageDom') }}</li>
        </ul>

        <h5>{{ $t('manual.compare.playerMetricsComp') }}</h5>
        <p>{{ $t('manual.compare.organized6') }}</p>
        <div class="metric-category">
          <h6>
            <Icon icon="mdi:timer-outline" class="icon-category" />
            {{ $t('manual.compare.gameTime') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.gameTimeDesc') }}</li>
          </ul>
        </div>
        <div class="metric-category">
          <h6>
            <Icon icon="mdi:soccer" class="icon-category" />
            {{ $t('manual.compare.attackingPlayer') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.attackingPlayerDesc') }}</li>
          </ul>
        </div>
        <div class="metric-category">
          <h6>
            <Icon icon="mdi:target" class="icon-category" />
            {{ $t('manual.compare.passingPlayer') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.passingPlayerDesc') }}</li>
          </ul>
        </div>
        <div class="metric-category">
          <h6>
            <Icon icon="mdi:shield-half-full" class="icon-category" />
            {{ $t('manual.compare.defensivePlayer') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.defensivePlayerDesc') }}</li>
          </ul>
        </div>

        <!-- ⚠️ Discipline -->
        <div class="metric-category">
          <h6>
            <Icon icon="mdi:card-account-details" class="icon-category" />
            {{ $t('manual.compare.disciplinePlayer') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.disciplinePlayerDesc') }}</li>
          </ul>
        </div>
        <div class="metric-category">
          <h6>
            <Icon icon="mdi:handball" class="icon-category" />
            {{ $t('manual.compare.goalkeeper') }}
          </h6>
          <ul>
            <li>{{ $t('manual.compare.goalkeeperDesc') }}</li>
          </ul>
        </div>
        <h5>{{ $t('manual.compare.penaltiesPlayer') }}</h5>
        <p>{{ $t('manual.compare.ifEither') }}</p>
        <ul>
          <li>{{ $t('manual.compare.penaltySideBySide') }}</li>
          <li>{{ $t('manual.compare.penaltyScoredGreen') }}</li>
          <li>{{ $t('manual.compare.penaltyZero') }}</li>
        </ul>
      </section>
      <section id="navigation-features">
        <h3>{{ $t('manual.sections.navigationFeatures') }}</h3>

        <h4>{{ $t('manual.compare.pageContentNavigator') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.fixedSidebar') }}:</strong> {{ $t('manual.compare.fixedSidebarDesc') }}</li>
          <li><strong>{{ $t('manual.compare.quickLinks') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.linkSelection') }}</li>
              <li>{{ $t('manual.compare.linkStats') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.smoothScroll') }}:</strong> {{ $t('manual.compare.smoothScrollDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.urlStructure') }}</h4>
        <p>{{ $t('manual.compare.urlPreserves') }}</p>
        <ul>
          <li><strong>{{ $t('manual.compare.urlTeams') }}</strong></li>
          <li><strong>{{ $t('manual.compare.urlPlayers') }}</strong></li>
          <li><strong>{{ $t('manual.compare.urlSeasons') }}</strong></li>
          <li><strong>{{ $t('manual.compare.shareableLinks') }}:</strong> {{ $t('manual.compare.shareableLinkDesc') }}</li>
          <li><strong>{{ $t('manual.compare.bookmarkable') }}:</strong> {{ $t('manual.compare.bookmarkableDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.loadingStates') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.fetchingStats') }}</strong></li>
          <li>{{ $t('manual.compare.loadingSpinner') }}</li>
          <li>{{ $t('manual.compare.replacesContent') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.errorMessages') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.selectBothMsg') }}</strong></li>
          <li><strong>{{ $t('manual.compare.cantCompareMsg') }}</strong></li>
          <li><strong>{{ $t('manual.compare.selectBothSeasonMsg') }}</strong></li>
          <li><strong>{{ $t('manual.compare.errorFetchMsg') }}</strong></li>
          <li><strong>{{ $t('manual.compare.noStatsMsg') }}</strong></li>
        </ul>
      </section>
      <section id="visual-design">
        <h3>{{ $t('manual.sections.visualDesign') }}</h3>

        <h4>{{ $t('manual.compare.winnerHighlighting') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.boldEnhanced') }}:</strong> {{ $t('manual.compare.boldEnhancedDesc') }}</li>
          <li><strong>{{ $t('manual.compare.subtleBackground') }}:</strong> {{ $t('manual.compare.subtleBackgroundDesc') }}</li>
          <li><strong>{{ $t('manual.compare.typeColors') }}:</strong> {{ $t('manual.compare.typeColorsDesc') }}</li>
          <li><strong>{{ $t('manual.compare.noHighlight') }}:</strong> {{ $t('manual.compare.noHighlightDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.hoverEffects') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.hoverMetric') }}:</strong> {{ $t('manual.compare.hoverMetricDesc') }}</li>
          <li><strong>{{ $t('manual.compare.hoverFormation') }}:</strong> {{ $t('manual.compare.hoverFormationDesc') }}</li>
          <li><strong>{{ $t('manual.compare.hoverBadges') }}:</strong> {{ $t('manual.compare.hoverBadgesDesc') }}</li>
          <li><strong>{{ $t('manual.compare.hoverDropdowns') }}:</strong> {{ $t('manual.compare.hoverDropdownsDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.responsiveDesign') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.desktop') }}:</strong> {{ $t('manual.compare.desktopDesc') }}</li>
          <li><strong>{{ $t('manual.compare.mobile') }}:</strong> {{ $t('manual.compare.mobileDesc') }}</li>
        </ul>
      </section>
      <section id="advanced-tips">
        <h3>{{ $t('manual.sections.advancedTips') }}</h3>

        <h4>{{ $t('manual.compare.effectiveComparison') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.eraComparison') }}:</strong> {{ $t('manual.compare.eraComparisonDesc') }}</li>
          <li><strong>{{ $t('manual.compare.teamEvolution') }}:</strong> {{ $t('manual.compare.teamEvolutionDesc') }}</li>
          <li><strong>{{ $t('manual.compare.playerPeak') }}:</strong> {{ $t('manual.compare.playerPeakDesc') }}</li>
          <li><strong>{{ $t('manual.compare.positionalComparison') }}:</strong> {{ $t('manual.compare.positionalComparisonDesc') }}</li>
          <li><strong>{{ $t('manual.compare.styleAnalysis') }}:</strong> {{ $t('manual.compare.styleAnalysisDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.interpretingResults') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.contextMatters') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.contextMinutes') }}</li>
              <li>{{ $t('manual.compare.contextFouls') }}</li>
              <li>{{ $t('manual.compare.contextCleanSheets') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.lookPatterns') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.patternAttack') }}</li>
              <li>{{ $t('manual.compare.patternDiscipline') }}</li>
              <li>{{ $t('manual.compare.patternPassing') }}</li>
            </ul>
          </li>
          <li><strong>{{ $t('manual.compare.useMultiple') }}:</strong>
            <ul>
              <li>{{ $t('manual.compare.multipleDesc') }}</li>
              <li>{{ $t('manual.compare.multipleExample') }}</li>
              <li>{{ $t('manual.compare.multipleFuller') }}</li>
            </ul>
          </li>
        </ul>

        <h4>{{ $t('manual.compare.sharingCollaboration') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.copyUrl') }}:</strong> {{ $t('manual.compare.copyUrlDesc') }}</li>
          <li><strong>{{ $t('manual.compare.screenshot') }}:</strong> {{ $t('manual.compare.screenshotDesc') }}</li>
          <li><strong>{{ $t('manual.compare.bookmarkFavorites') }}:</strong> {{ $t('manual.compare.bookmarkFavoritesDesc') }}</li>
        </ul>

        <h4>{{ $t('manual.compare.performanceNotes') }}</h4>
        <ul>
          <li><strong>{{ $t('manual.compare.fastLoading') }}:</strong> {{ $t('manual.compare.fastLoadingDesc') }}</li>
        </ul>
      </section>
      <section id="troubleshooting">
        <h3>{{ $t('manual.sections.troubleshooting') }}</h3>

        <h4>Stats Not Loading?</h4>
        <ol>
          <li>Verify both items are selected (check both dropdowns)</li>
          <li>Ensure both seasons are selected</li>
          <li>Check that selections are different (no duplicate items)</li>
          <li>Look for error messages - they explain the issue</li>
          <li>Try refreshing the page</li>
        </ol>

        <h4>Dropdown Not Working?</h4>
        <ul>
          <li>Click directly on the input field</li>
          <li>If nothing appears, check for error messages</li>
          <li>Try clearing selection (<Icon icon="mdi:close" class="icon-muted" /> icon) and reselecting</li>
          <li>Refresh page if dropdown seems stuck</li>
        </ul>

        <h4>Some Metrics Show "-"?</h4>
        <ul>
          <li>This is normal - not all players/teams have all data types</li>
          <li>Goalkeeper stats only exist for goalkeepers</li>
          <li>Some older seasons may have incomplete data</li>
        </ul>

        <h4>Shared Link Not Working?</h4>
        <ul>
          <li>Ensure entire URL was copied (including query parameters after ?)</li>
          <li>Check that IDs in URL are valid (items might have been deleted)</li>
          <li>Try manually reselecting items if URL fails</li>
        </ul>
      </section>
      <section id="keyboard-shortcuts">
        <h3>{{ $t('manual.sections.keyboardShortcuts') }}</h3>
        <ul>
          <li><strong>Tab:</strong> Navigate between dropdowns and selections</li>
          <li><strong>Enter:</strong> Open dropdown when focused</li>
          <li><strong>Type:</strong> Filter options in open dropdown</li>
          <li><strong>Up/Down Arrows:</strong> Navigate dropdown options (limited support)</li>
          <li><strong>Click/Tap:</strong> Primary interaction method</li>
        </ul>
      </section>
      <section id="quick-reference">
        <h3>{{ $t('manual.sections.quickReference') }}</h3>

        <h4>{{ $t('manual.sections.seasonComparison') }}</h4>
        <ul>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.twoDropdowns') }}
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.gridOrganized') }}
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.winnerBanner') }}
          </li>
        </ul>

        <h4>{{ $t('manual.sections.teamComparison') }}</h4>
        <ul>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.twoSearchableDropdowns') }}
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.independentSeasons') }}
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.formationsSection') }}
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.organized3') }}
          </li>
        </ul>

        <h4>{{ $t('manual.sections.playerComparison') }}</h4>
        <ul>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.twoSearchablePlayers') }}
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.mixAndMatch') }}
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.organized6') }}
          </li>
          <li>
            <Icon icon="mdi:check-circle" class="icon-success" />
            {{ $t('manual.compare.goalkeeper') }}
          </li>
        </ul>
        <h4>Universal Features</h4>
        <ul>
          <li><Icon icon="mdi:check-circle" class="icon-success" /> {{ $t('manual.compare.winnerBanner') }}</li>
          <li><Icon icon="mdi:check-circle" class="icon-success" /> {{ $t('manual.compare.visualBar') }}</li>
          <li><Icon icon="mdi:check-circle" class="icon-success" /> {{ $t('manual.compare.shareableLinks') }}</li>
          <li><Icon icon="mdi:check-circle" class="icon-success" /> {{ $t('manual.compare.smoothScroll') }}</li>
          <li><Icon icon="mdi:check-circle" class="icon-success" /> {{ $t('manual.compare.responsiveDesign') }}</li>
          <li><Icon icon="mdi:check-circle" class="icon-success" /> {{ $t('manual.compare.colorCoding') }}</li>
          <li><Icon icon="mdi:check-circle" class="icon-success" /> {{ $t('manual.compare.hoverEffects') }}</li>
        </ul>
      </section>
    </div>

    <div class="back-link">
      <NuxtLink :to="localePath('/')" class="back-btn">← Back to home</NuxtLink>
    </div>
  </div>
  <PageContent :page-sections="pageSections" />
</template>

<style scoped>
.manual-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    text-align: left;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1.1rem;
    margin-top: 0.5rem;
}

.tab-navigation {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 2rem;
    border-bottom: 2px solid rgba(61, 214, 140, 0.2);
    flex-wrap: wrap;
    justify-content: center;
}

.tab-btn {
    padding: 0.75rem 1.5rem;
    background: transparent;
    border: none;
    color: #94a3b8;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;
}

.tab-btn:hover {
    color: #e2e8f0;
    background: rgba(61, 214, 140, 0.05);
}

.tab-btn.active {
    color: rgba(61, 214, 140, 0.95);
    border-bottom-color: rgba(61, 214, 140, 0.9);
}

.manual-content {
    animation: fadeIn 0.3s ease-in;
    text-align: left;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.manual-content h2 {
    color: rgba(61, 214, 140, 0.95);
    font-size: 2rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(61, 214, 140, 0.2);
    text-align: left;
}

.manual-content h3 {
    color: #e2e8f0;
    font-size: 1.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
    text-align: left;
}

.manual-content h4 {
    color: #cbd5e1;
    font-size: 1.2rem;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    text-align: left;
}

.manual-content section {
    margin-bottom: 2rem;
    text-align: left;
}

.manual-content .lead {
    font-size: 1.1rem;
    color: #cbd5e1;
    margin-bottom: 2rem;
    line-height: 1.6;
    text-align: left;
}

.manual-content p {
    color: #94a3b8;
    line-height: 1.8;
    margin-bottom: 1rem;
    text-align: left;
}

.manual-content ul,
.manual-content ol {
    color: #94a3b8;
    line-height: 1.8;
    margin-left: 1.5rem;
    margin-bottom: 1rem;
    text-align: left;
}

.manual-content li {
    margin-bottom: 0.5rem;
}

.manual-content ul ul {
    margin-top: 0.5rem;
}

.manual-content code {
    background: rgba(61, 214, 140, 0.1);
    color: rgba(61, 214, 140, 0.95);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
}

.manual-content strong {
    color: #e2e8f0;
    font-weight: 600;
}

.metric-category {
    background: rgba(61, 214, 140, 0.03);
    border-left: 3px solid rgba(61, 214, 140, 0.3);
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
    text-align: left;
}

.metric-category h6 {
    color: rgba(61, 214, 140, 0.95);
    font-size: 1.1rem;
    margin: 0 0 0.75rem 0;
    font-weight: 600;
    text-align: left;
}

.metric-category ul {
    margin-left: 1.5rem;
    margin-bottom: 0.5rem;
    text-align: left;
}

.manual-content pre {
    background: rgba(0, 0, 0, 0.3);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    color: #94a3b8;
    overflow-x: auto;
    margin: 0.5rem 0;
}

.back-link {
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(61, 214, 140, 0.2);
}

.back-btn {
    display: inline-flex;
    align-items: center;
    padding: 0.75rem 1.5rem;
    background: rgba(61, 214, 140, 0.1);
    border: 1px solid rgba(61, 214, 140, 0.3);
    border-radius: 8px;
    color: rgba(61, 214, 140, 0.95);
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s;
}

.back-btn:hover {
    background: rgba(61, 214, 140, 0.2);
    border-color: rgba(61, 214, 140, 0.5);
    transform: translateX(-5px);
}

@media (max-width: 768px) {
    .manual-container {
        padding: 1rem;
    }
    
    .tab-navigation {
        gap: 0.25rem;
    }
    
    .tab-btn {
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }
    
    .manual-content h2 {
        font-size: 1.5rem;
    }
    
    .manual-content h3 {
        font-size: 1.25rem;
    }
}
</style>