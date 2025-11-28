<template>
    <div class="card-margin">
        <div class="card-grid" v-for="value in items" :key="value">
            <card id="card">{{ value }}</card>
        </div>
    </div>
</template>
<script setup>
import card from '~/components/card.vue';

const items = ["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"];
</script>

<style scoped>
.card-margin {
  margin-top: 80px;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}
</style>