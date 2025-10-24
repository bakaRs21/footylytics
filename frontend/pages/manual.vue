<template>
    <div class="container">
    <main class="docs">
        <h1>About this website</h1>

        <p class="lead">
            This site is an interactive explorer for Premier League data covering seasons 2006–2018.
            Browse teams, players and match statistics, compare seasons and inspect visualizations.
        </p>

        <section>
            <h2>Purpose</h2>
            <p>
                Provide a lightweight, browsable interface to historical Premier League statistics for analysis,
                lightweight visualization and simple comparisons across seasons and clubs.
            </p>
        </section>

        <section>
            <h2>Data</h2>
            <ul>
                <li>Compiled from publicly available match and squad records for 2006–2018.</li>
                <li>All data is stored locally in the frontend or fetched from the project's API/back-end.</li>
                <li>No live betting or copyrighted proprietary feeds are used.</li>
            </ul>
        </section>

        <section>
            <h2>Features</h2>
            <ul>
                <li>Season and team overviews</li>
                <li>Player lists and basic statistics</li>
                <li>Interactive charts and comparisons</li>
                <li>CSV export and simple filtering</li>
            </ul>
        </section>

        <section>
            <h2>How to use</h2>
            <ol>
                <li>Open the navbar to choose a season or team.</li>
                <li>Use filters to narrow results (position, minutes, goals, etc.).</li>
                <li>Click a chart or table row to drill into player or match details.</li>
            </ol>
        </section>

        <section>
            <h2>Contributing</h2>
            <p>
                Contributions (bug fixes, data improvements, UI enhancements) are welcome. Please open issues
                or pull requests on the project's repository.
            </p>
        </section>

        <section>
            <h2>License & contact</h2>
            <p>
                This project is released under the MIT License. For questions or to report data issues, open an issue
                or contact the maintainers via the repository.
            </p>
        </section>

        <NuxtLink to="/" class="back">← Back to home</NuxtLink>
    </main>
    </div>
</template>

<script>
export default {
    name: 'DocsPage'
}
</script>

<style scoped>
.docs {
    max-width: 820px;
    margin: 48px auto;
    padding: 0 24px;
    line-height: 1.5;
}

h1 {
    margin-bottom: 12px;
    font-size: 1.8rem;
}

.lead {
    margin-bottom: 20px;
}

h2 {
    margin-top: 20px;
    font-size: 1.1rem;
}

ul, ol {
    margin: 8px 0 16px 20px;
}

.back {
    margin-top: 28px;
}

a:hover {
    text-decoration: underline;
}
</style>