<script setup>
import { Icon } from '@iconify/vue';
const { t } = useI18n()
const localePath = useLocalePath()

const features = [
    {
        title: t('pages.index.features.compareStats.title'),
        description: t('pages.index.features.compareStats.description'),
        icon: 'openmoji:chart-increasing',
        link: '/compare',
        color: '#3b82f6'
    },
    {
        title: t('pages.index.features.teamStatistics.title'),
        description: t('pages.index.features.teamStatistics.description'),
        icon: 'openmoji:soccer-ball',
        link: '/teams',
        color: '#22c55e'
    },
    {
        title: t('pages.index.features.playerAnalysis.title'),
        description: t('pages.index.features.playerAnalysis.description'),
        icon: 'openmoji:trophy',
        link: '/players',
        color: '#f59e0b'
    },
    {
        title: t('pages.index.features.seasonOverview.title'),
        description: t('pages.index.features.seasonOverview.description'),
        icon: 'openmoji:calendar',
        link: '/seasons',
        color: '#ef4444'
    }
];
</script>

<template>
    <div class="index-headings">
        <h1 class="h1-design">{{ $t('pages.index.title') }}</h1>
        <h2 class="text-green text-semibold">
            {{ $t('pages.index.subtitle') }}
        </h2>
        <p class="text-gray subheader-text">
            {{ $t('pages.index.description') }}
        </p>
    </div>
    <div class="grid-auto-fit feature-cards-links">
            <NuxtLink v-for="(feature, index) in features" 
                :key="index"
                :to="localePath(feature.link)"
                class="card-base feature-card"
                :style="{ '--card-color': feature.color }"
            >
                <div class="icon-wrapper m-lg">
                    <Icon :icon="feature.icon" class="icon-xl" />
                </div>
                <h3 class="header-text text-light m-md">{{ feature.title }}</h3>
                <p class="text-gray feature-description">
                    {{ feature.description }}
                </p>
                <div class="feature-arrow">
                    <Icon icon="openmoji:right-arrow" />
                </div>
            </NuxtLink>
    </div>
    <div class="flex-center gap-xl stat-badges">
        <div class="stat-badge">
            <Icon icon="openmoji:fire" class="icon-md" />
            <span>{{ $t('pages.index.badges.liveStatistics') }}</span>
        </div>
        <div class="stat-badge">
            <Icon icon="openmoji:chart-increasing" class="icon-md" />
            <span>{{ $t('pages.index.badges.visualAnalytics') }}</span>
        </div>
        <div class="stat-badge">
            <Icon icon="emojione-v1:lightning-mood" class="icon-md" />
            <span>{{ $t('pages.index.badges.fastComparisons') }}</span>
        </div>
    </div>
</template>

<style scoped>
.index-headings {
    text-align: center; 
    margin-bottom: 3rem; 
    padding: 2rem 0;
}
h2 {
    font-size: 1.5rem; 
    margin-bottom: 1.5rem;
}
.subheader-text {
    font-size: 1.1rem; 
    line-height: 1.6; 
    max-width: 600px; 
    margin: 0 auto;
}

.feature-cards-links {
    max-width: 1200px; 
    margin: 0 auto 3rem;
}

.feature-card {
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
}
.feature-card:hover::before {
    transform: scaleX(1);
}
.feature-card:hover {
    border-color: var(--card-color);
}

.feature-description {
    font-size: 0.95rem; 
    line-height: 1.5; 
    margin-bottom: 1rem;
}

.feature-arrow {
    position: absolute;
    bottom: 1rem;
    right: 1rem;
    font-size: 1.5rem;
    opacity: 0;
    transform: translateX(-10px);
    transition: all 0.3s ease;
}

.feature-card:hover .feature-arrow {
    opacity: 1;
    transform: translateX(0);
}

.stat-badges {
    flex-wrap: wrap; 
    padding: 2rem 0;
}
.stat-badge {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: rgba(74, 222, 128, 0.1);
    border: 1px solid rgba(74, 222, 128, 0.3);
    border-radius: 50px;
    color: #4ade80;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
}

.stat-badge:hover {
    background: rgba(74, 222, 128, 0.2);
    transform: scale(1.05);
}
</style>