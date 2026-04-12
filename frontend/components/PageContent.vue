<script setup>

const props = defineProps({
    pageSections: {
        type: Array,
        required: true,
    }
})
async function scrollTo(anchor) {
    if (!anchor) return;
    await nextTick()

    const element = document.getElementById(anchor);
    if (!element) return;
    element.scrollIntoView({ behavior: 'smooth', block: 'start'})
}

</script>
<template>
    <nav class="pg">
        <p class="pg-title">{{ $t('components.pageContent.title') }}</p>
        <ul>
            <li v-for="section in pageSections" :key="section.anchor" @click="scrollTo(section.anchor)" class="pg-section">
                {{  section.label }}
            </li>
        </ul>
    </nav>
</template>
<style scoped>
.pg {
    position: fixed;
    top: 120px;
    right: 38px;
    width: 200px;
    background: #1e1e2e;
    border-left: 2px solid #3234b1;
    padding: 8px 14px;
    border-radius: 6px;
    z-index: 100; 
}
.pg-title {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
    color: #aaa;   
}
ul {
    list-style: none;
    padding: 0;
    margin: 0; 
}
.pg-section {
    cursor: pointer;
    padding: 5px 0;
    font-size: 0.875rem;
    color: #5fc4ff;
}
.pg-section:hover {
    text-decoration: underline;
}
</style>