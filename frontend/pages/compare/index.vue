<script setup>
import card from '~/components/card.vue';
</script>

<template>
    <div class="page-heading">
        <h1 class="h1-design">See the difference</h1>
        <h3>Compare individual players, teams or seasons</h3>
    </div>
    <div class="card-margin">
        <div class="card-grid">
            <card>
                <p>Compare Seasons</p>
            </card>
            <card>
                <p>Compare Teams</p>
            </card>
            <card>
                <p>Compare Players</p>
            </card>
        </div>
    </div>
</template>

<style scoped>
.card-margin {
  margin-top: 100px;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 120px;
}
@media (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>