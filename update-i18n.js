const fs = require('fs');
const path = require('path');

// Update en.json
const enPath = path.join(__dirname, 'frontend/i18n/locales/en.json');
const en = JSON.parse(fs.readFileSync(enPath, 'utf8'));

// Add entries to sections
en.manual.sections.teamMatches = 'Team Matches';
en.manual.sections.seasonMatches = 'Season Matches';

// Add entries to teams
Object.assign(en.manual.teams, {
  matchesDashboardHeading: 'Team Matches Dashboard',
  venueFilter: 'Venue Filter',
  venueFilterDesc: 'Filter matches by venue: All, Home, or Away',
  refereeFilter: 'Referee Filter',
  refereeFilterDesc: 'Filter matches by referee (only shows referees officiating team matches)',
  matchesTable: 'Matches Table',
  matchesTableDesc: 'Interactive table displaying all team matches with detailed information',
  matchColumns: 'Table Columns',
  colDate: 'Date & Time',
  colDateDesc: 'Match date and time (UTC)',
  colRound: 'Round',
  colRoundDesc: 'Competition round (e.g., R1, R2 for league rounds)',
  colTeams: 'Teams',
  colTeamsDesc: 'Home and Away team names with logos',
  colScore: 'Score',
  colScoreDesc: 'Final score with halftime score breakdown below',
  colVenue: 'Venue',
  colVenueDesc: 'Stadium name and city',
  colReferee: 'Referee',
  colRefereeDesc: 'Match referee name or "—" if not assigned',
  colStatus: 'Status',
  colStatusDesc: 'Match status badge (FT=Full Time, NS=Not Started, etc.)'
});

// Add entries to seasons
Object.assign(en.manual.seasons, {
  matchesDescription: 'Interactive table displaying matches from the season with filtering options',
  expandMatches: 'Expanding Matches',
  expandMatchesDesc: 'Click the collapsible section header to show/hide matches list',
  teamFilter: 'Team Filter (Season Page)',
  teamFilterDesc: 'Filter matches to only those involving the selected team',
  refereeFilterSeason: 'Referee Filter (Season Page)',
  refereeFilterSeasonDesc: 'Filter matches by referee (only shows referees officiating season matches)',
  matchesDisplayed: 'Matches Count',
  matchesDisplayedDesc: 'Shows the total number of matches after applying filters',
  matchTableColumns: 'Table Columns',
  dateColumn: 'Date & Time',
  dateColumnDesc: 'Match date and time in UTC',
  roundColumn: 'Round',
  roundColumnDesc: 'Competition round identifier',
  teamsColumn: 'Teams',
  teamsColumnDesc: 'Home and away team names with logos',
  scoreColumn: 'Score',
  scoreColumnDesc: 'Final score with halftime breakdown',
  venueColumn: 'Venue',
  venueColumnDesc: 'Stadium name and city',
  refereeColumn: 'Referee',
  refereeColumnDesc: 'Match official name or "—" if unassigned',
  statusColumn: 'Status',
  statusColumnDesc: 'Match status badge'
});

// Write en.json
fs.writeFileSync(enPath, JSON.stringify(en, null, 2), 'utf8');
console.log('✓ en.json updated successfully');

// Update cs.json
const csPath = path.join(__dirname, 'frontend/i18n/locales/cs.json');
const cs = JSON.parse(fs.readFileSync(csPath, 'utf8'));

// Add entries to sections
cs.manual.sections.teamMatches = 'Zápasy týmu';
cs.manual.sections.seasonMatches = 'Zápasy sezony';

// Add entries to teams (Czech)
Object.assign(cs.manual.teams, {
  matchesDashboardHeading: 'Přehled zápasů týmu',
  venueFilter: 'Filtr umístění',
  venueFilterDesc: 'Filtrujte zápasy podle místa: Vše, Domácí nebo Venkovní',
  refereeFilter: 'Filtr rozhodčího',
  refereeFilterDesc: 'Filtrujte zápasy podle rozhodčího (zobrazuje pouze rozhodčí, kteří vedli zápasy týmu)',
  matchesTable: 'Tabulka zápasů',
  matchesTableDesc: 'Interaktivní tabulka zobrazující všechny zápasy týmu s podrobnostmi',
  matchColumns: 'Sloupce tabulky',
  colDate: 'Datum a čas',
  colDateDesc: 'Datum a čas zápasu (UTC)',
  colRound: 'Kolo',
  colRoundDesc: 'Identifikátor kola (např. R1, R2)',
  colTeams: 'Týmy',
  colTeamsDesc: 'Domácí a venkovní tým s logy',
  colScore: 'Skóre',
  colScoreDesc: 'Finální skóre se shrnutím poločasu',
  colVenue: 'Stadion',
  colVenueDesc: 'Název stadionu a město',
  colReferee: 'Rozhodčí',
  colRefereeDesc: 'Jméno rozhodčího nebo "—" pokud není přiřazen',
  colStatus: 'Stav',
  colStatusDesc: 'Odznak stavu zápasu (FT=Konec, NS=Nezačato, atd.)'
});

// Add entries to seasons (Czech)
Object.assign(cs.manual.seasons, {
  matchesDescription: 'Interaktivní tabulka zobrazující zápasy sezony s možnostmi filtrování',
  expandMatches: 'Rozbalení zápasů',
  expandMatchesDesc: 'Klikněte na záhlaví kolapsibilní sekce pro zobrazení/skrytí seznamu zápasů',
  teamFilter: 'Filtr týmu (stránka sezony)',
  teamFilterDesc: 'Filtrujte zápasy pouze ty, ve kterých hraje vybraný tým',
  refereeFilterSeason: 'Filtr rozhodčího (stránka sezony)',
  refereeFilterSeasonDesc: 'Filtrujte zápasy podle rozhodčího (zobrazuje pouze rozhodčí vedoucí zápasy sezony)',
  matchesDisplayed: 'Počet zápasů',
  matchesDisplayedDesc: 'Zobrazuje celkový počet zápasů po aplikaci filtrů',
  matchTableColumns: 'Sloupce tabulky',
  dateColumn: 'Datum a čas',
  dateColumnDesc: 'Datum a čas zápasu v UTC',
  roundColumn: 'Kolo',
  roundColumnDesc: 'Identifikátor kola soutěže',
  teamsColumn: 'Týmy',
  teamsColumnDesc: 'Domácí a venkovní tým s logy',
  scoreColumn: 'Skóre',
  scoreColumnDesc: 'Finální skóre se shrnutím poločasu',
  venueColumn: 'Stadion',
  venueColumnDesc: 'Název stadionu a město',
  refereeColumn: 'Rozhodčí',
  refereeColumnDesc: 'Jméno rozhodčího nebo "—" pokud není přiřazen',
  statusColumn: 'Stav',
  statusColumnDesc: 'Odznak stavu zápasu'
});

// Write cs.json
fs.writeFileSync(csPath, JSON.stringify(cs, null, 2), 'utf8');
console.log('✓ cs.json updated successfully');

console.log('\n✓ All translation files updated!');
