<script setup>
import { Icon } from '@iconify/vue';
const displayPageContent = ref(true)
const showPageContent = ref(false)

function syncListByWidth() {
    const width = window.innerWidth;

    if (width <= 1150) {
        showPageContent.value = false;
        displayPageContent.value = false;
        return;
    }
    if (width <= 1340) {
        showPageContent.value = true;
        return;
    }
    if (width <= 1680) {
        showPageContent.value = false;
        return;
    }
    showPageContent.value = true;
}
function displayPG() {
    displayPageContent.value = !displayPageContent.value
    showPageContent.value = displayPageContent.value
}

defineProps({
    pageSections: {
        type: Array,
        required: true,
    }
})

onMounted(() => {
    syncListByWidth();
    window.addEventListener('resize', syncListByWidth);
});

onBeforeUnmount(() => {
    window.removeEventListener('resize', syncListByWidth);
});

async function scrollTo(anchor) {
    if (!anchor) return;
    await nextTick()

    const element = document.getElementById(anchor);
    if (!element) return;
    element.scrollIntoView({ behavior: 'smooth', block: 'start'})
}

</script>
<template>
    <div class="pg-wrap">
        <button type="button" @click="displayPG()" class="pg-display icon-md">
            <Icon icon="material-symbols:arrow-drop-down-circle-outline" :class="{ 'rotated': displayPageContent }"/>
        </button>
        <nav v-show="displayPageContent" class="pg">
            <button type="button" @click="showPageContent = !showPageContent" class="title-with-arrows pg-tooltip">
                <Icon icon="mdi:chevron-down" :class="{ 'rotated': showPageContent }"/>
                <p class="pg-title">{{ $t('components.pageContent.title') }}</p>
                <Icon icon="mdi:chevron-down" :class="{ 'rotated': showPageContent }"/>
            </button>
            <ul v-show="showPageContent">
                <li v-for="section in pageSections" :key="section.anchor" @click="scrollTo(section.anchor)" class="pg-section">
                    {{  section.label }}
                </li>
            </ul>
        </nav>
    </div>    
</template>
<style scoped>
.pg-wrap {
    position: fixed;
    top: 120px;
    right: 20px;
    display: flex;
    justify-content: flex-end;
    align-items: flex-start;
    flex-direction: row-reverse;
    gap: 8px;
    z-index: 1200;
}
.pg-display {
    cursor: pointer;
    border: 0;
    background: transparent;
    color: #8ac8ff;
    padding: 0;
    line-height: 1;
    transition: color 0.2s ease;
    flex-shrink: 0;
    margin-top: 6px;
    transform: rotate(90deg);
}
.pg-display:hover {
    color: #b5dcff;
}
.pg {
    width: 240px;
    max-width: calc(100vw - 48px);
    background: rgba(25, 25, 34, 0.86);
    border: 1px solid rgba(95, 196, 255, 0.35);
    border-radius: 10px;
    padding: 10px 14px;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.28);
    backdrop-filter: blur(4px);
}
.pg-title {
    margin: 0;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #c5d3de;
}
ul {
    list-style: none;
    padding: 0;
    margin: 6px 0 0;
}
.pg-section {
    cursor: pointer;
    padding: 6px 0;
    font-size: 0.875rem;
    color: #5fc4ff;
    border-radius: 6px;
    transition: color 0.2s ease, background-color 0.2s ease;
}
.pg-section:hover {
    color: #9ddfff;
    background: rgba(95, 196, 255, 0.14);
    text-decoration: none;
}
.pg-tooltip {
    cursor: pointer;
}

.title-with-arrows  {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 0;
    border: 0;
    background: transparent;
    color: inherit;
    padding: 0;
}
.rotated {
    transform: rotate(180deg);
    transition: transform 0.2s ease;
}

@media (max-width: 1680px) {
    .pg-wrap {
        right: 12px;
    }
}

</style>
