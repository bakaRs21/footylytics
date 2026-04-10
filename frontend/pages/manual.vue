<script setup>
import { ref, computed } from 'vue';

const { t } = useI18n()
const localePath = useLocalePath()
const activeTab = ref('teams');

const tabs = [
  { id: 'teams', label: t('pages.teams.title') },
  { id: 'players', label: t('pages.players.title') },
  { id: 'seasons', label: t('pages.seasons.title') },
  { id: 'compare', label: t('pages.compare.title') },
];

const pageSections = computed(() => {
  const sections = [
    { label: 'Manual Selection', anchor: 'manual-selection' }
  ];
  if (activeTab.value === 'teams') {
    sections.push(
      { label: 'Teams Overview', anchor: 'teams-overview' },
      { label: 'Teams Index Page', anchor: 'teams-index' },
      { label: 'Individual Team Page', anchor: 'individual-team' },
      { label: 'Team Logo Section', anchor: 'team-logo' },
      { label: 'Season Selection', anchor: 'season-selection' },
      { label: 'Team Statistics', anchor: 'team-statistics' },
      { label: 'Metrics Dashboard', anchor: 'metrics-dashboard' },
      { label: 'Navigation & Tips', anchor: 'navigation-tips' }
    );
  } else if (activeTab.value === 'players') {
    sections.push(
      { label: 'Players Overview', anchor: 'players-overview' },
      { label: 'Players Index Page', anchor: 'players-index' },
      { label: 'Individual Player Page', anchor: 'individual-player' },
      { label: 'Player Information', anchor: 'player-information' },
      { label: 'Season Selection', anchor: 'player-season-selection' },
      { label: 'Player Statistics', anchor: 'player-statistics' },
      { label: 'Player Metrics', anchor: 'player-metrics' },
      { label: 'Color Coding', anchor: 'color-coding' }
    );
  } else if (activeTab.value === 'seasons') {
    sections.push(
      { label: 'Seasons Overview', anchor: 'seasons-overview' },
      { label: 'Seasons Index Page', anchor: 'seasons-index' },
      { label: 'Individual Season Page', anchor: 'individual-season' },
      { label: 'Season Stats Section', anchor: 'season-stats-section' },
      { label: 'Season Ranking', anchor: 'season-ranking' },
      { label: 'Navigation', anchor: 'season-navigation' },
      { label: 'Usage Tips', anchor: 'usage-tips' }
    );
  } else if (activeTab.value === 'compare') {
    sections.push(
      { label: 'Compare Overview', anchor: 'compare-overview' },
      { label: 'Compare Index', anchor: 'compare-index' },
      { label: 'Pages Structure', anchor: 'pages-structure' },
      { label: 'Season Comparison', anchor: 'season-comparison' },
      { label: 'Team Comparison', anchor: 'team-comparison' },
      { label: 'Player Comparison', anchor: 'player-comparison' },
      { label: 'Navigation Features', anchor: 'navigation-features' },
      { label: 'Visual Design', anchor: 'visual-design' },
      { label: 'Advanced Tips', anchor: 'advanced-tips' },
      { label: 'Troubleshooting', anchor: 'troubleshooting' },
      { label: 'Quick Reference', anchor: 'quick-reference' }
    );
  }

  return sections;
});
</script>

<template>
    <div class="page-heading">
      <h1 class="h1-design">{{ $t('navigation.manual') }}</h1>
      <p class="subtitle">Complete guide to using the Premier League Statistics Explorer</p>
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
            <h2 id="teams-overview">Team Pages Overview</h2>
            <p class="lead">
                The Team Pages provide a comprehensive interface to explore Premier League teams, their seasonal performance, 
                detailed statistics, and advanced metrics.
            </p>

            <section id="teams-index">
                <h3>Teams Index Page</h3>
                <p><strong>URL:</strong> <code>/teams</code></p>
                
                <h4>Search & Filter</h4>
                <ul>
                    <li><strong>Search Bar:</strong> Type team names to filter the list in real-time (case-insensitive)</li>
                    <li><strong>Filters Button:</strong> Click to reveal filter options:
                        <ul>
                            <li><strong>Seasons:</strong> Filter teams by the seasons they participated in</li>
                            <li>Multiple filters can be active simultaneously</li>
                            <li><strong>Clear Filters:</strong> Remove all active selections</li>
                        </ul>
                    </li>
                    <li><strong>Item Counter:</strong> Shows current count of displayed teams in top-left</li>
                </ul>

                <h4>Team Cards</h4>
                <p>Click any team card to navigate to that team's detailed page with statistics and metrics.</p>
            </section>

            <section id="individual-team">
                <h3>Individual Team Page</h3>
                <p><strong>URL:</strong> <code>/teams/[team_id]</code></p>
                
                <h4 id="team-logo">1. Team Logo Section</h4>
                <ul>
                    <li>Displays team logo and name</li>
                    <li>Background uses team colors extracted from the logo</li>
                    <li>Diagonal stripe pattern with dynamic color adjustment</li>
                </ul>

                <h4 id="season-selection">2. Season Selection</h4>
                <ul>
                    <li><strong>Season Cards:</strong> Click any season to load statistics for that specific period</li>
                    <li><strong>All Seasons Button:</strong> Aggregates data from all seasons the team participated in</li>
                    <li>Selected season updates the URL and triggers automatic statistics loading</li>
                </ul>

                <h4 id="team-statistics">3. Team Statistics Dashboard</h4>
                <p>Click the header to expand/collapse. Provides comprehensive statistics:</p>
                
                <ul>
                    <li><strong>Formations Card:</strong> Shows all formations used with match counts
                        <ul>
                            <li>Click any formation to see detailed lineup information</li>
                            <li>Expandable with smooth animation</li>
                        </ul>
                    </li>
                    <li><strong>Matches Overview:</strong> Total matches, wins (W), draws (D), losses (L)</li>
                    <li><strong>Goals & Performance:</strong> Goals scored/conceded, clean sheets, penalties</li>
                    <li><strong>Streaks:</strong> Biggest win/draw/loss streaks and team form badges (W/D/L)</li>
                    <li><strong>Clear Stats Button:</strong> Removes statistics display and resets view</li>
                </ul>

                <h4 id="metrics-dashboard">4. Metrics Dashboard</h4>
                <p>Advanced metrics with customizable visualizations:</p>
                
                <ul>
                    <li><strong>Metric Selection:</strong>
                        <ul>
                            <li>Use multi-select dropdown to choose metrics</li>
                            <li>Click "Confirm" to load selected metrics</li>
                        </ul>
                    </li>
                    <li><strong>Season Filter:</strong> Filter metrics by "all seasons" or specific season</li>
                    <li><strong>Chart Types:</strong> Switch between Bar, Line, Pie, and Donut charts</li>
                    <li><strong>Shared Graphs:</strong> Some metrics combine into grouped visualizations</li>
                </ul>
            </section>

            <section id="navigation-tips">
                <h3>Navigation & Tips</h3>
                <ul>
                    <li><strong>Page Navigator:</strong> Fixed sidebar on right with quick links to sections</li>
                    <li><strong>Auto-scroll:</strong> Page automatically scrolls to loaded content</li>
                    <li><strong>Hover Effects:</strong> Cards lift and highlight on hover</li>
                    <li><strong>Responsive:</strong> Adapts to desktop (multi-column) and mobile (stacked) layouts</li>
                </ul>
            </section>
        </div>

        <!-- PLAYERS MANUAL -->
        <div v-show="activeTab === 'players'" class="manual-content">
            <h2 id="players-overview">Player Pages Overview</h2>
            <p class="lead">
                The Player Pages allow you to explore individual player statistics, performance metrics, 
                and career data across multiple teams and seasons.
            </p>

            <section id="players-index">
                <h3>Players Index Page</h3>
                <p><strong>URL:</strong> <code>/players</code></p>
                
                <h4>Search & Filter</h4>
                <ul>
                    <li><strong>Search Bar:</strong> Type player names to filter the list in real-time</li>
                    <li><strong>Filters Button:</strong> Access multiple filter options:
                        <ul>
                            <li><strong>Seasons:</strong> Filter players by seasons they participated in</li>
                            <li><strong>Teams:</strong> Filter players by teams they played for</li>
                            <li>Multiple filters from both categories can be active</li>
                            <li><strong>Clear Filters:</strong> Remove all active selections</li>
                        </ul>
                    </li>
                    <li><strong>Item Counter:</strong> Displays current count of visible players</li>
                </ul>

                <h4>Player Cards</h4>
                <p>Click any player card to view detailed statistics and performance metrics.</p>
            </section>

            <section id="individual-player">
                <h3>Individual Player Page</h3>
                <p><strong>URL:</strong> <code>/players/[player_id]</code></p>
                
                <h4 id="player-information">1. Player Information</h4>
                <ul>
                    <li>Player name displayed prominently</li>
                    <li><strong>Info Table:</strong> Shows player details (nationality, position, etc.)</li>
                    <li>Hover effects on table rows for better readability</li>
                </ul>

                <h4 id="player-season-selection">2. Season Selection</h4>
                <ul>
                    <li><strong>Season Cards:</strong> Click to load statistics for specific seasons</li>
                    <li><strong>All Seasons Button:</strong> View aggregated career statistics</li>
                    <li>Automatic data loading when season is selected</li>
                </ul>

                <h4 id="player-statistics">3. Player Statistics Dashboard</h4>
                <p>Click header to expand/collapse. Eight comprehensive categories:</p>
                
                <ul>
                    <li><strong>Games:</strong>
                        <ul>
                            <li>Total matches played</li>
                            <li>Total minutes played</li>
                            <li>Player rating</li>
                        </ul>
                    </li>
                    <li><strong>Goals & Assists:</strong>
                        <ul>
                            <li>Total goals and assists</li>
                            <li>Total shots and shots on target</li>
                        </ul>
                    </li>
                    <li><strong>Defensive Stats:</strong>
                        <ul>
                            <li>Total tackles</li>
                            <li>Blocks and interceptions</li>
                        </ul>
                    </li>
                    <li><strong>Passing Stats:</strong>
                        <ul>
                            <li>Total passes</li>
                            <li>Key passes</li>
                        </ul>
                    </li>
                    <li><strong>Duels & Dribbles:</strong>
                        <ul>
                            <li>Total duels and duels won</li>
                            <li>Dribble attempts and successful dribbles</li>
                        </ul>
                    </li>
                    <li><strong>Discipline:</strong>
                        <ul>
                            <li>Red cards (red text)</li>
                            <li>Yellow cards (yellow text)</li>
                            <li>Fouls committed and drawn</li>
                        </ul>
                    </li>
                    <li><strong>Penalties:</strong>
                        <ul>
                            <li>Penalties scored (green text)</li>
                            <li>Penalties missed (red text)</li>
                            <li>Penalties won</li>
                        </ul>
                    </li>
                    <li><strong>Goalkeeper Stats:</strong>
                        <ul>
                            <li>Goals conceded</li>
                            <li>Saves</li>
                            <li>Penalties saved</li>
                            <li>Shows "No data" if player is not a goalkeeper</li>
                        </ul>
                    </li>
                </ul>

                <p><strong>Note:</strong> Each card shows "No data available" if the player has no statistics in that category for the selected season.</p>

                <h4 id="player-metrics">4. Player Metrics Dashboard</h4>
                <ul>
                    <li><strong>Metric Selection:</strong> Multi-select dropdown for choosing advanced metrics</li>
                    <li><strong>Season Filter:</strong> Apply to specific season or all seasons</li>
                    <li><strong>Chart Visualizations:</strong> Multiple chart types for data analysis</li>
                    <li><strong>Clear Stats:</strong> Reset and clear all loaded statistics</li>
                </ul>
            </section>

            <section id="color-coding">
                <h3>Color Coding</h3>
                <ul>
                    <li><strong>Green:</strong> Positive stats (goals, wins, successful actions)</li>
                    <li><strong>Red:</strong> Negative stats (cards, missed penalties, losses)</li>
                    <li><strong>Yellow:</strong> Warning stats (yellow cards)</li>
                </ul>
            </section>
        </div>

        <!-- SEASONS MANUAL -->
        <div v-show="activeTab === 'seasons'" class="manual-content">
            <h2 id="seasons-overview">Season Pages Overview</h2>
            <p class="lead">
                The Season Pages provide a comprehensive view of entire Premier League seasons, 
                including aggregate statistics and league standings.
            </p>

            <section id="seasons-index">
                <h3>Seasons Index Page</h3>
                <p><strong>URL:</strong> <code>/seasons</code></p>
                
                <h4>Features</h4>
                <ul>
                    <li><strong>Search Bar:</strong> Filter seasons by year</li>
                    <li><strong>Season Cards:</strong> Each card represents a season (e.g., "2006-2007")</li>
                    <li>Click any season card to view detailed statistics and rankings</li>
                    <li><strong>Note:</strong> Filters are not available on season pages (seasons only filter)</li>
                </ul>
            </section>

            <section id="individual-season">
                <h3>Individual Season Page</h3>
                <p><strong>URL:</strong> <code>/seasons/[season_id]</code></p>
                
                <h4 id="season-stats-section">1. Season Stats Section</h4>
                <p>Comprehensive aggregate statistics for the entire season:</p>
                
                <ul>
                    <li><strong>Season Header:</strong>
                        <ul>
                            <li>Season year displayed prominently</li>
                            <li>Total players count</li>
                            <li>Total player appearances</li>
                        </ul>
                    </li>
                    <li><strong>Overview Cards (Top Row):</strong>
                        <ul>
                            <li>Total Goals</li>
                            <li>Total Assists</li>
                            <li>Total Shots</li>
                            <li>Total Passes</li>
                        </ul>
                    </li>
                </ul>

                <h4>Detailed Statistics Cards:</h4>
                
                <ul>
                    <li><strong>Shooting:</strong>
                        <ul>
                            <li>Total shots and shots on target</li>
                            <li>Shot accuracy percentage with progress bar</li>
                        </ul>
                    </li>
                    <li><strong>Passing:</strong>
                        <ul>
                            <li>Total passes and key passes</li>
                            <li>Key pass rate percentage with progress bar</li>
                        </ul>
                    </li>
                    <li><strong>Duels & Dribbles:</strong>
                        <ul>
                            <li>Total duels and duels won</li>
                            <li>Duel win rate percentage</li>
                            <li>Dribble attempts and successful dribbles</li>
                            <li>Dribble success rate percentage</li>
                        </ul>
                    </li>
                    <li><strong>Discipline:</strong>
                        <ul>
                            <li>Yellow cards (yellow icon and text)</li>
                            <li>Red cards (red icon and text)</li>
                            <li>Fouls committed and drawn</li>
                        </ul>
                    </li>
                    <li><strong>Penalties:</strong>
                        <ul>
                            <li>Penalties scored and missed</li>
                            <li>Conversion rate percentage with progress bar</li>
                        </ul>
                    </li>
                    <li><strong>Defense:</strong>
                        <ul>
                            <li>Total tackles</li>
                        </ul>
                    </li>
                </ul>

                <h4 id="season-ranking">2. Season Ranking Section</h4>
                <p>Interactive league standings table with advanced sorting:</p>
                
                <ul>
                    <li><strong>Table Header:</strong>
                        <ul>
                            <li>"League Standings" title</li>
                            <li>Team count badge</li>
                        </ul>
                    </li>
                    <li><strong>Sort Options (10 sorting criteria):</strong>
                        <ul>
                            <li><strong>Points:</strong> Total points (default)</li>
                            <li><strong>Wins:</strong> Number of victories</li>
                            <li><strong>Goal Difference:</strong> Goals for minus goals against</li>
                            <li><strong>Goals Scored:</strong> Total goals for</li>
                            <li><strong>Goals Conceded:</strong> Total goals against</li>
                            <li><strong>Matches Played:</strong> Total matches</li>
                            <li><strong>Draws:</strong> Number of draws</li>
                            <li><strong>Losses:</strong> Number of defeats</li>
                            <li><strong>Win Rate %:</strong> Percentage of matches won</li>
                            <li><strong>Points / Match:</strong> Average points per match</li>
                        </ul>
                    </li>
                    <li><strong>Sorting:</strong>
                        <ul>
                            <li>Click any sort button to apply</li>
                            <li>Click again to reverse order (ascending/descending)</li>
                            <li>Active sort highlighted with green accent</li>
                            <li>Arrow icon shows current direction</li>
                        </ul>
                    </li>
                </ul>

                <h4>Ranking Table Columns:</h4>
                <ul>
                    <li><strong>#:</strong> Rank position
                        <ul>
                            <li>🏆 Gold trophy for 1st place</li>
                            <li>🏆 Silver trophy for 2nd place</li>
                            <li>🏆 Bronze trophy for 3rd place</li>
                        </ul>
                    </li>
                    <li><strong>Team:</strong> Team name with form bar indicator</li>
                    <li><strong>MP:</strong> Matches played</li>
                    <li><strong>W:</strong> Wins (green)</li>
                    <li><strong>D:</strong> Draws (muted)</li>
                    <li><strong>L:</strong> Losses (red)</li>
                    <li><strong>GF:</strong> Goals for</li>
                    <li><strong>GA:</strong> Goals against</li>
                    <li><strong>GD:</strong> Goal difference (color-coded: green positive, red negative)</li>
                    <li><strong>Pts:</strong> Total points (highlighted badge)</li>
                    <li><strong>P/M:</strong> Points per match (decimal)</li>
                    <li><strong>W%:</strong> Win rate percentage (color-coded: green ≥50%, yellow ≥30%, red <30%)</li>
                </ul>

                <h4>Visual Features:</h4>
                <ul>
                    <li><strong>Form Bars:</strong> Visual indicator under team names showing win rate
                        <ul>
                            <li>Green: ≥60% win rate (great form)</li>
                            <li>Yellow: 40-59% win rate (good form)</li>
                            <li>Orange: 20-39% win rate (poor form)</li>
                            <li>Red: <20% win rate (bad form)</li>
                        </ul>
                    </li>
                    <li><strong>Top 3 Highlighting:</strong> 1st, 2nd, and 3rd place rows have subtle background colors</li>
                    <li><strong>Hover Effects:</strong> Rows highlight on hover for better readability</li>
                    <li><strong>Responsive Table:</strong> Scrollable on mobile devices</li>
                </ul>
            </section>

            <section id="season-navigation">
                <h3>Navigation</h3>
                <ul>
                    <li><strong>Page Content Navigator:</strong> Fixed sidebar with quick links to:
                        <ul>
                            <li>Season Stats</li>
                            <li>Season Ranking</li>
                        </ul>
                    </li>
                    <li><strong>Smooth Scrolling:</strong> Click section links for smooth navigation</li>
                </ul>
            </section>

            <section id="usage-tips">
                <h3>Usage Tips</h3>
                <ul>
                    <li><strong>Compare Teams:</strong> Use different sort options to compare team performance</li>
                    <li><strong>Defensive Analysis:</strong> Sort by "Goals Conceded" to find best defenses</li>
                    <li><strong>Attacking Analysis:</strong> Sort by "Goals Scored" to find top attacking teams</li>
                    <li><strong>Efficiency:</strong> Use "Points / Match" or "Win Rate %" for performance consistency</li>
                    <li><strong>Form Analysis:</strong> Visual form bars show team quality at a glance</li>
                </ul>
            </section>
        </div>

        <!-- COMPARE MANUAL -->
        <div v-show="activeTab === 'compare'" class="manual-content">
            <h2 id="compare-overview">Compare Pages - Complete Guide</h2>
            <p class="lead">
                The Compare Pages provide powerful head-to-head comparison tools for analyzing players, teams, 
                or entire seasons side-by-side. Use advanced metrics and visualizations to discover performance 
                differences and identify statistical winners.
            </p>

            <section id="compare-index">
                <h3>Compare Index Page</h3>
                <p><strong>URL:</strong> <code>/compare</code></p>
                
                <h4>Overview</h4>
                <p>The main compare page presents three comparison options as large, clickable cards:</p>
                <ul>
                    <li><strong>Compare Seasons:</strong> Analyze entire Premier League seasons</li>
                    <li><strong>Compare Teams:</strong> Head-to-head team performance analysis</li>
                    <li><strong>Compare Players:</strong> Direct player-to-player statistical comparison</li>
                </ul>
                
                <h4>Getting Started</h4>
                <ol>
                    <li>Click on any of the three comparison type cards</li>
                    <li>You'll be taken to the dedicated comparison interface for that category</li>
                    <li>Select your items to compare and view detailed statistical breakdowns</li>
                </ol>
            </section>

            <section id="pages-structure">
                <h3>Comparison Pages Structure</h3>
                <p><strong>URLs:</strong></p>
                <ul>
                    <li><code>/compare/Seasons</code> - Season comparisons</li>
                    <li><code>/compare/Teams</code> - Team comparisons</li>
                    <li><code>/compare/Players</code> - Player comparisons</li>
                </ul>

                <h4>Page Layout</h4>
                <p>All comparison pages follow a consistent structure with two main sections:</p>
                <ol>
                    <li><strong>Selection Area</strong> (top) - Choose what to compare</li>
                    <li><strong>Stats Comparison</strong> (bottom) - View detailed statistical breakdown</li>
                </ol>
            </section>

            <section id="season-comparison">
                <h3>Season Comparison</h3>
                <p><strong>URL:</strong> <code>/compare/Seasons</code></p>

                <h4>Step 1: Select Seasons</h4>
                <ul>
                    <li><strong>Two Dropdown Menus:</strong> Side-by-side season selectors</li>
                    <li><strong>Left Dropdown:</strong> Select first season (e.g., "2006")</li>
                    <li><strong>Right Dropdown:</strong> Select second season (e.g., "2010")</li>
                    <li>Both dropdowns list all available seasons from 2006-2018</li>
                </ul>

                <h4>Selection Rules</h4>
                <ul>
                    <li>❌ <strong>Cannot select the same season twice</strong> - Error: "Cannot compare the same season"</li>
                    <li>✅ Must select both seasons before stats will load</li>
                    <li>Selections update the URL query parameters automatically</li>
                </ul>

                <h4>Step 2: View Comparison Results</h4>
                <p>Once both seasons are selected, the page displays:</p>

                <h5>A. Comparison Header</h5>
                <ul>
                    <li><strong>Layout:</strong> First Season | VS Badge | Second Season</li>
                    <li>Season names displayed as "YYYY-YYYY" format (e.g., "2006-2007")</li>
                    <li>Purple gradient styling with prominent "VS" badge in the center</li>
                </ul>

                <h5>B. Overall Winner Banner</h5>
                <p>Displays the overall statistical winner based on all compared metrics:</p>
                <ul>
                    <li><strong>Winner Announcement:</strong>
                        <ul>
                            <li>👑 <strong>"Overall Winner: [Season Name]"</strong> if one season dominates</li>
                            <li>🤝 <strong>"It's a Tie!"</strong> if both seasons are statistically equal</li>
                        </ul>
                    </li>
                    <li><strong>Win Breakdown:</strong> Shows "XW vs YW out of Z metrics"
                        <ul>
                            <li>X = number of metrics the first season wins</li>
                            <li>Y = number of metrics the second season wins</li>
                            <li>Z = total number of comparable metrics</li>
                        </ul>
                    </li>
                    <li><strong>Visual Progress Bar:</strong>
                        <ul>
                            <li>Two-color bar showing percentage dominance</li>
                            <li>Left side (blue) = first season's percentage</li>
                            <li>Right side (purple) = second season's percentage</li>
                            <li>Percentages displayed if each side is >15% wide</li>
                        </ul>
                    </li>
                    <li><strong>Banner Color:</strong>
                        <ul>
                            <li>Gold/yellow tint if there's a clear winner</li>
                            <li>Neutral if it's a tie</li>
                        </ul>
                    </li>
                </ul>

                <h5>C. Metrics Comparison Grid</h5>
                <p>Organized into 7 statistical categories, each with its own icon and metrics:</p>

                <div class="metric-category">
                    <h6>⚽ Season Overview</h6>
                    <ul>
                        <li><strong>Total Players:</strong> Number of players who appeared in the season</li>
                        <li><strong>Appearances:</strong> Total player appearances across all matches</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>🎯 Attacking</h6>
                    <ul>
                        <li><strong>Goals:</strong> Total goals scored (higher is better)</li>
                        <li><strong>Assists:</strong> Total assists provided (higher is better)</li>
                        <li><strong>Total Shots:</strong> All shot attempts</li>
                        <li><strong>Shots on Target:</strong> Accurate shots (higher is better)</li>
                        <li><strong>Shot Accuracy %:</strong> Percentage of shots on target (higher is better)</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>🎯 Passing</h6>
                    <ul>
                        <li><strong>Total Passes:</strong> All passes attempted</li>
                        <li><strong>Key Passes:</strong> Passes leading to shots (higher is better)</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>💥 Duels & Dribbles</h6>
                    <ul>
                        <li><strong>Total Duels:</strong> All 1v1 contests</li>
                        <li><strong>Duels Won:</strong> Successful duels (higher is better)</li>
                        <li><strong>Duel Win Rate %:</strong> Success percentage (higher is better)</li>
                        <li><strong>Dribble Attempts:</strong> All dribble tries</li>
                        <li><strong>Dribbles Successful:</strong> Completed dribbles (higher is better)</li>
                        <li><strong>Dribble Success %:</strong> Completion rate (higher is better)</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>🛡️ Defensive</h6>
                    <ul>
                        <li><strong>Tackles:</strong> Total tackles made (higher is better)</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>⚠️ Discipline</h6>
                    <ul>
                        <li><strong>Yellow Cards:</strong> Total yellow cards (lower is better) ⚠️</li>
                        <li><strong>Red Cards:</strong> Total red cards (lower is better) 🔴</li>
                        <li><strong>Fouls Committed:</strong> Total fouls (lower is better) 🔴</li>
                        <li><strong>Fouls Drawn:</strong> Fouls won (higher is better)</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>⚽ Penalties</h6>
                    <ul>
                        <li><strong>Penalties Scored:</strong> Successful penalties (higher is better)</li>
                        <li><strong>Penalties Missed:</strong> Failed penalties (lower is better) 🔴</li>
                    </ul>
                </div>

                <h5>Reading the Comparison Grid</h5>
                <ul>
                    <li><strong>Layout:</strong> Each metric row shows:
                        <pre>First Value | Metric Label | Second Value</pre>
                    </li>
                    <li><strong>Winner Highlighting:</strong>
                        <ul>
                            <li>🏆 <strong>Bold/highlighted value</strong> = winner for that metric</li>
                            <li>Regular styling = lower/equal value</li>
                        </ul>
                    </li>
                    <li><strong>Color Coding:</strong>
                        <ul>
                            <li><span style="color: #22c55e;">🟢 Green</span> = positive/success metrics (goals, assists, saves)</li>
                            <li><span style="color: #ef4444;">🔴 Red</span> = negative metrics (cards, fouls, missed penalties)</li>
                            <li><span style="color: #eab308;">🟡 Yellow</span> = warning metrics (yellow cards)</li>
                            <li>White = neutral metrics (total counts)</li>
                        </ul>
                    </li>
                    <li><strong>Missing Data:</strong> Shows "-" if data unavailable for that metric</li>
                </ul>

                <h4>Understanding "Lower is Better" Metrics</h4>
                <p>Some metrics favor lower values (marked with 🔴 above):</p>
                <ul>
                    <li>Yellow Cards, Red Cards, Fouls Committed, Penalties Missed</li>
                    <li>The season with the <em>lower</em> value wins these comparisons</li>
                    <li>Example: 50 fouls beats 75 fouls</li>
                </ul>
            </section>

            <section id="team-comparison">
                <h3>Team Comparison</h3>
                <p><strong>URL:</strong> <code>/compare/Teams</code></p>

                <h4>Step 1: Select Teams</h4>
                <ul>
                    <li><strong>Two Searchable Dropdowns:</strong> Side-by-side team selectors</li>
                    <li><strong>How to Use:</strong>
                        <ol>
                            <li>Click the left dropdown to select the first team</li>
                            <li>Type to filter/search team names in real-time</li>
                            <li>Click a team from the filtered list to select</li>
                            <li>Selected team name appears in the input field</li>
                            <li>❌ Click the X icon to clear selection and start over</li>
                            <li>Repeat for the right dropdown to select second team</li>
                        </ol>
                    </li>
                    <li><strong>Visual Indicators:</strong>
                        <ul>
                            <li>🔽 Down arrow = dropdown closed, click to open</li>
                            <li>🔼 Up arrow = dropdown open, showing options</li>
                            <li>❌ X icon = selection made, click to clear</li>
                        </ul>
                    </li>
                </ul>

                <h4>Step 2: Select Seasons</h4>
                <p><strong>After both teams are selected</strong>, two new dropdowns appear below:</p>
                <ul>
                    <li><strong>Season Selectors:</strong> One for each team
                        <ul>
                            <li>Shows only seasons that team participated in</li>
                            <li>Option: "all seasons" - aggregates all available data for that team</li>
                            <li>Individual seasons listed chronologically</li>
                        </ul>
                    </li>
                    <li><strong>Independent Seasons:</strong>
                        <ul>
                            <li>Each team can have a different season selected</li>
                            <li>Example: Compare Team A in 2008 vs Team B in 2015</li>
                            <li>Or compare Team A's 2010 season vs their "all seasons" aggregate</li>
                        </ul>
                    </li>
                </ul>

                <h4>Selection Rules</h4>
                <ul>
                    <li>❌ <strong>Cannot compare a team with itself</strong> - Error: "Cannot compare the same team"</li>
                    <li>✅ Must select both teams AND their respective seasons</li>
                    <li>Selections persist in URL (shareable link)</li>
                </ul>

                <h4>Step 3: View Comparison Results</h4>

                <h5>A. Comparison Header</h5>
                <ul>
                    <li><strong>Layout:</strong> Team 1 Name | VS | Team 2 Name</li>
                    <li>Team names displayed prominently</li>
                    <li>VS badge centered between teams</li>
                </ul>

                <h5>B. Overall Winner Banner</h5>
                <p>Same structure as season comparison:</p>
                <ul>
                    <li>👑 Winner announcement or 🤝 Tie declaration</li>
                    <li>Win count breakdown (e.g., "15W vs 12W out of 27 metrics")</li>
                    <li>Dual-color percentage bar showing dominance</li>
                </ul>

                <h5>C. Team Metrics Comparison</h5>
                <p>Organized into 3 main categories:</p>

                <div class="metric-category">
                    <h6>⚽ Matches Overview</h6>
                    <ul>
                        <li><strong>Matches Played:</strong> Total matches</li>
                        <li><strong>Wins:</strong> Victories (higher is better) 🟢</li>
                        <li><strong>Draws:</strong> Draw results</li>
                        <li><strong>Losses:</strong> Defeats (lower is better) 🔴</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>🎯 Goals & Performance</h6>
                    <ul>
                        <li><strong>Goals Scored:</strong> Total goals for (higher is better) 🟢</li>
                        <li><strong>Goals Conceded:</strong> Total goals against (lower is better) 🔴</li>
                        <li><strong>Clean Sheets:</strong> Matches without conceding (higher is better) 🟢</li>
                        <li><strong>Failed to Score:</strong> Goalless matches (lower is better) 🔴</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>📈 Streaks</h6>
                    <ul>
                        <li><strong>Win Streak:</strong> Longest consecutive wins (higher is better) 🟢</li>
                        <li><strong>Draw Streak:</strong> Longest consecutive draws</li>
                        <li><strong>Loss Streak:</strong> Longest consecutive losses (lower is better) 🔴</li>
                    </ul>
                </div>

                <h5>D. Formations Section</h5>
                <p>Shows tactical formations used by each team:</p>
                <ul>
                    <li><strong>Side-by-Side Columns:</strong> One column per team</li>
                    <li><strong>Formation List:</strong> All formations used (e.g., "4-4-2", "4-3-3")</li>
                    <li><strong>Match Count:</strong> Number of matches each formation was used</li>
                    <li><strong>Expandable Details:</strong>
                        <ul>
                            <li>Click any formation row to expand</li>
                            <li>Shows detailed lineup information</li>
                            <li>🔽 Arrow rotates 180° when expanded</li>
                            <li>Click again to collapse</li>
                        </ul>
                    </li>
                </ul>

                <h5>E. Recent Form Section</h5>
                <p>Visual representation of recent match results:</p>
                <ul>
                    <li><strong>Side-by-Side Display:</strong> One column per team</li>
                    <li><strong>Form Badges:</strong> Sequence of W/D/L letters
                        <ul>
                            <li><span style="background: #22c55e; padding: 2px 6px; border-radius: 3px;">W</span> = Win (green badge)</li>
                            <li><span style="background: #eab308; padding: 2px 6px; border-radius: 3px;">D</span> = Draw (yellow badge)</li>
                            <li><span style="background: #ef4444; padding: 2px 6px; border-radius: 3px;">L</span> = Loss (red badge)</li>
                        </ul>
                    </li>
                    <li><strong>Reading Direction:</strong> Latest match is on the RIGHT</li>
                    <li><strong>Hover Effect:</strong> Badges scale up 15% on hover</li>
                </ul>

                <h5>F. Penalties Section</h5>
                <p>Penalty kick statistics for each team:</p>
                <ul>
                    <li><strong>Two Columns:</strong> One per team</li>
                    <li><strong>Scored:</strong> Successful penalties (green text)</li>
                    <li><strong>Missed:</strong> Failed penalties (red text)</li>
                </ul>
            </section>

            <section id="player-comparison">
                <h3>Player Comparison</h3>
                <p><strong>URL:</strong> <code>/compare/Players</code></p>

                <h4>Step 1: Select Players</h4>
                <ul>
                    <li><strong>Two Searchable Dropdowns:</strong> Identical to team selection</li>
                    <li><strong>Search Functionality:</strong>
                        <ul>
                            <li>Type player names to filter list instantly</li>
                            <li>Case-insensitive search</li>
                            <li>Matches partial names</li>
                        </ul>
                    </li>
                    <li><strong>Clear Selection:</strong> Click X to reset and choose different player</li>
                </ul>

                <h4>Step 2: Select Seasons</h4>
                <p>After both players are selected:</p>
                <ul>
                    <li><strong>Season Dropdowns Appear:</strong> One for each player</li>
                    <li><strong>Season Options:</strong>
                        <ul>
                            <li>"all seasons" - career aggregated stats</li>
                            <li>Individual seasons the player participated in</li>
                        </ul>
                    </li>
                    <li><strong>Mix and Match:</strong>
                        <ul>
                            <li>Compare Player A's 2012 season vs Player B's entire career</li>
                            <li>Or compare same season for both players</li>
                            <li>Complete flexibility in time period selection</li>
                        </ul>
                    </li>
                </ul>

                <h4>Selection Rules</h4>
                <ul>
                    <li>❌ <strong>Cannot compare a player with themselves</strong></li>
                    <li>✅ Must select both players and their seasons</li>
                    <li>URL updates with all selections for sharing</li>
                </ul>

                <h4>Step 3: View Comparison Results</h4>

                <h5>A. Comparison Header</h5>
                <ul>
                    <li>Player 1 Name | VS | Player 2 Name</li>
                    <li>Clean, prominent display</li>
                </ul>

                <h5>B. Overall Winner Banner</h5>
                <ul>
                    <li>Calculates winner across ALL player metrics (6 categories)</li>
                    <li>Shows total wins breakdown</li>
                    <li>Percentage dominance bar</li>
                </ul>

                <h5>C. Player Metrics Comparison</h5>
                <p>Organized into 6 comprehensive categories:</p>

                <div class="metric-category">
                    <h6>⏱️ Game Time</h6>
                    <ul>
                        <li><strong>Appearances:</strong> Total matches played</li>
                        <li><strong>Starts:</strong> Matches started in lineup (higher is better)</li>
                        <li><strong>Minutes:</strong> Total playing time (higher is better)</li>
                        <li><strong>Avg Rating:</strong> Performance rating (higher is better) 🟢</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>⚽ Attacking</h6>
                    <ul>
                        <li><strong>Goals:</strong> Total goals scored (higher is better) 🟢</li>
                        <li><strong>Assists:</strong> Goals assisted (higher is better) 🟢</li>
                        <li><strong>Shots:</strong> Total shot attempts</li>
                        <li><strong>On Target:</strong> Accurate shots (higher is better) 🟢</li>
                        <li><strong>Dribbles Won:</strong> Successful dribbles (higher is better) 🟢</li>
                        <li><strong>Dribble Attempts:</strong> Total dribble tries</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>🎯 Passing</h6>
                    <ul>
                        <li><strong>Total Passes:</strong> All passes attempted</li>
                        <li><strong>Key Passes:</strong> Passes leading to shots (higher is better) 🟢</li>
                        <li><strong>Accuracy %:</strong> Pass completion rate (higher is better) 🟢</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>🛡️ Defensive</h6>
                    <ul>
                        <li><strong>Tackles:</strong> Total tackles made</li>
                        <li><strong>Interceptions:</strong> Passes intercepted (higher is better) 🟢</li>
                        <li><strong>Blocks:</strong> Shots/passes blocked (higher is better) 🟢</li>
                        <li><strong>Duels:</strong> Total 1v1 contests</li>
                        <li><strong>Duels Won:</strong> Successful duels (higher is better) 🟢</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>⚠️ Discipline</h6>
                    <ul>
                        <li><strong>Fouls Committed:</strong> Fouls given (lower is better) 🔴</li>
                        <li><strong>Fouls Drawn:</strong> Fouls won (higher is better) 🟢</li>
                        <li><strong>Yellow Cards:</strong> Cautions received (lower is better) 🟡</li>
                        <li><strong>Red Cards:</strong> Dismissals (lower is better) 🔴</li>
                    </ul>
                </div>

                <div class="metric-category">
                    <h6>🧤 Goalkeeper</h6>
                    <ul>
                        <li><strong>Saves:</strong> Shots saved (higher is better) 🟢</li>
                        <li><strong>Goals Conceded:</strong> Goals allowed (lower is better) 🔴</li>
                        <li><strong>Penalties Saved:</strong> Penalties stopped (higher is better) 🟢</li>
                        <li><em>Note: Shows "-" for non-goalkeepers</em></li>
                    </ul>
                </div>

                <h5>D. Penalties Section</h5>
                <p>If either player has penalty data:</p>
                <ul>
                    <li>Side-by-side columns</li>
                    <li>Scored (green) vs Missed (red)</li>
                    <li>Shows 0 if no data available</li>
                </ul>
            </section>

            <section id="navigation-features">
                <h3>Navigation & Interface Features</h3>

                <h4>Page Content Navigator</h4>
                <ul>
                    <li><strong>Fixed Sidebar:</strong> Right side of screen</li>
                    <li><strong>Quick Links:</strong>
                        <ul>
                            <li>"Selection" - jumps to selection area</li>
                            <li>"Stats comparison" - jumps to results</li>
                        </ul>
                    </li>
                    <li><strong>Smooth Scrolling:</strong> Animated transitions between sections</li>
                </ul>

                <h4>Auto-Scroll Behavior</h4>
                <ul>
                    <li>When stats load, page automatically scrolls to comparison results</li>
                    <li>80px offset from top for comfortable viewing</li>
                    <li>Smooth animation prevents jarring jumps</li>
                </ul>

                <h4>URL Query Parameters</h4>
                <p>All selections are stored in URL for easy sharing:</p>
                <ul>
                    <li><strong>Teams/Players:</strong>
                        <ul>
                            <li><code>?first=[ID]&second=[ID]</code> - selected items</li>
                            <li><code>&firstSeason=[YEAR]&secondSeason=[YEAR]</code> - seasons</li>
                        </ul>
                    </li>
                    <li><strong>Seasons:</strong>
                        <ul>
                            <li><code>?firstSeason=[YEAR]&secondSeason=[YEAR]</code></li>
                        </ul>
                    </li>
                    <li><strong>Shareable Links:</strong> Copy URL to share exact comparison</li>
                    <li><strong>Bookmarkable:</strong> URL maintains comparison on reload</li>
                </ul>

                <h4>Loading States</h4>
                <ul>
                    <li><strong>"Fetching stats..."</strong> - appears while loading data</li>
                    <li>Loading spinner SVG animation</li>
                    <li>Replaces content area until data arrives</li>
                </ul>

                <h4>Error Messages</h4>
                <ul>
                    <li><strong>"Please select both [items] first"</strong> - incomplete selection</li>
                    <li><strong>"Cannot compare the same [item]"</strong> - duplicate selection</li>
                    <li><strong>"Please select both [items] and their seasons"</strong> - missing season</li>
                    <li><strong>"Error fetching stats: [details]"</strong> - API/network error</li>
                    <li><strong>"No stats available"</strong> - valid selection but no data</li>
                </ul>
            </section>

            <section id="visual-design">
                <h3>Visual Design Elements</h3>

                <h4>Winner Highlighting</h4>
                <ul>
                    <li><strong>Bold/Enhanced Styling:</strong> Winner values stand out</li>
                    <li><strong>Subtle Background:</strong> Light glow on winning metrics</li>
                    <li><strong>Color Coding:</strong> Type-specific colors (success/danger/warning)</li>
                    <li><strong>No Highlight:</strong> If values are equal (tie)</li>
                </ul>

                <h4>Hover Effects</h4>
                <ul>
                    <li><strong>Metric Rows:</strong> Subtle highlight on hover</li>
                    <li><strong>Formation Items:</strong> Background change indicates clickability</li>
                    <li><strong>Form Badges:</strong> Scale up 15% on hover</li>
                    <li><strong>Dropdowns:</strong> Options highlight in darker shade</li>
                </ul>

                <h4>Responsive Design</h4>
                <ul>
                    <li><strong>Desktop (>840px):</strong>
                        <ul>
                            <li>Side-by-side layouts maintained</li>
                            <li>Wide comparison grids</li>
                            <li>All sections fully visible</li>
                        </ul>
                    </li>
                    <li><strong>Mobile (<840px):</strong>
                        <ul>
                            <li>Stacked layouts for better readability</li>
                            <li>Dropdowns become full-width</li>
                            <li>Metrics stack vertically</li>
                            <li>Touch-friendly targets</li>
                        </ul>
                    </li>
                </ul>
            </section>

            <section id="advanced-tips">
                <h3>Advanced Tips & Strategies</h3>

                <h4>Effective Comparison Strategies</h4>
                <ul>
                    <li><strong>Era Comparison:</strong> Compare early seasons (2006-2009) vs modern seasons (2015-2018)</li>
                    <li><strong>Team Evolution:</strong> Compare same team across different seasons</li>
                    <li><strong>Player Peak Analysis:</strong> Compare player's best season vs career average ("all seasons")</li>
                    <li><strong>Positional Comparison:</strong> Compare players in same position (both forwards, etc.)</li>
                    <li><strong>Style Analysis:</strong> Use formation data to understand tactical differences</li>
                </ul>

                <h4>Interpreting Results</h4>
                <ul>
                    <li><strong>Context Matters:</strong>
                        <ul>
                            <li>Higher minutes doesn't always mean better player (could be lack of alternatives)</li>
                            <li>More fouls committed might indicate aggressive defensive style</li>
                            <li>Clean sheets depend on entire team defense, not just one player</li>
                        </ul>
                    </li>
                    <li><strong>Look for Patterns:</strong>
                        <ul>
                            <li>Does one player excel in multiple attacking categories?</li>
                            <li>Is a team consistently winning discipline metrics (fewer cards)?</li>
                            <li>Which season had better overall passing efficiency?</li>
                        </ul>
                    </li>
                    <li><strong>Use Multiple Comparisons:</strong>
                        <ul>
                            <li>Compare 3+ items by doing multiple comparisons</li>
                            <li>Example: A vs B, then B vs C, then A vs C</li>
                            <li>Build a fuller picture of relative strengths</li>
                        </ul>
                    </li>
                </ul>

                <h4>Sharing & Collaboration</h4>
                <ul>
                    <li><strong>Copy URL:</strong> Share exact comparison with others</li>
                    <li><strong>Screenshot Results:</strong> Overall winner banner is perfect for sharing</li>
                    <li><strong>Bookmark Favorites:</strong> Save interesting comparisons for later</li>
                </ul>

                <h4>Performance Notes</h4>
                <ul>
                    <li><strong>Fast Loading:</strong> Parallel API requests fetch both items simultaneously</li>
                    <li><strong>Error Recovery:</strong> If one item fails, error message explains which one</li>
                    <li><strong>Smart Caching:</strong> Season lists cached after first load</li>
                </ul>
            </section>

            <section id="troubleshooting">
                <h3>Troubleshooting</h3>

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
                    <li>Try clearing selection (X icon) and reselecting</li>
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

            <section>
                <h3>Keyboard Shortcuts & Accessibility</h3>
                <ul>
                    <li><strong>Tab:</strong> Navigate between dropdowns and selections</li>
                    <li><strong>Enter:</strong> Open dropdown when focused</li>
                    <li><strong>Type:</strong> Filter options in open dropdown</li>
                    <li><strong>Up/Down Arrows:</strong> Navigate dropdown options (limited support)</li>
                    <li><strong>Click/Tap:</strong> Primary interaction method</li>
                </ul>
            </section>

            <section id="quick-reference">
                <h3>Quick Reference Summary</h3>
                
                <h4>Season Comparison</h4>
                <ul>
                    <li>✅ Simple dropdown selection</li>
                    <li>✅ 7 metric categories</li>
                    <li>✅ Overall statistical winner</li>
                </ul>

                <h4>Team Comparison</h4>
                <ul>
                    <li>✅ Searchable team selection</li>
                    <li>✅ Independent season choice per team</li>
                    <li>✅ Formation and form analysis</li>
                    <li>✅ 3 metric categories + formations + form</li>
                </ul>

                <h4>Player Comparison</h4>
                <ul>
                    <li>✅ Searchable player selection</li>
                    <li>✅ Independent season choice per player</li>
                    <li>✅ 6 comprehensive metric categories</li>
                    <li>✅ Goalkeeper-specific stats</li>
                </ul>

                <h4>Universal Features</h4>
                <ul>
                    <li>✅ Overall winner calculation</li>
                    <li>✅ Visual percentage dominance bar</li>
                    <li>✅ Shareable URLs</li>
                    <li>✅ Auto-scroll to results</li>
                    <li>✅ Responsive mobile design</li>
                    <li>✅ Color-coded metrics</li>
                    <li>✅ Hover effects and interactions</li>
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