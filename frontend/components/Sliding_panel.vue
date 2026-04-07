<script setup>
import { Icon } from "@iconify/vue"
import { ref, onMounted } from "vue"

const props = defineProps({
  items: Array
})

const items = ref([...props.items])
const track = ref(null)
const Duration = 600

const cardWidth = 280
const gap = 0
const offset = cardWidth + gap

const animate = () => {
  track.value.style.transition = `transform ${Duration}ms cubic-bezier(0.4, 1, 0.4, 1)`
}

const reset = () => {
  track.value.style.transition = "none"
  track.value.style.transform = `translateX(-${offset}px)`
}

const next = () => {
  animate()
  track.value.style.transform = `translateX(-${offset * 2}px)`

  const onEnd = () => {
    items.value.push(items.value.shift())
    reset()
    track.value.removeEventListener("transitionend", onEnd)
  }

  track.value.addEventListener("transitionend", onEnd)
}

const prev = () => {
  animate()
  track.value.style.transform = `translateX(0px)`

  const onEnd = () => {
    items.value.unshift(items.value.pop())
    reset()
    track.value.removeEventListener("transitionend", onEnd)
  }

  track.value.addEventListener("transitionend", onEnd)
}

onMounted(reset)
</script>
<template>
  <div class="slider">
    <Icon icon="mdi:chevron-left" @click="prev"/>
    <div class="viewport">
      <div class="track" ref="track">
        <div v-for="(item, i) in items" :key="item.id" class="card" :class="{ active: i === 2 }">
          <h4>{{ item }}</h4>
        </div>
      </div>
    </div>

    <Icon icon="mdi:chevron-right" @click="next"/>
  </div>
</template>
<style scoped>
.slider {
  display: flex;
  align-items: center;
  max-width: 100%;
  margin: auto;
}

.viewport {
  overflow: hidden;
  width: 100%;
}

.track {
  display: flex;
  will-change: transform;
}

.card {
  flex: 0 0 280px;
  height: 180px;
  border-radius: 16px;
  background: #111822;
  border: 1px solid #374153;

  opacity: 0.4;
  transform: scale(0.8);
  filter: blur(2px);
  transition:
    transform 0.6s cubic-bezier(0.4, 1, 0.4, 1),
    opacity 0.6s ease,
    box-shadow 0.8s ease,
    filter 0.6s ease;

  padding: 1rem;
  will-change: transform, opacity;
}

.card.active {
  opacity: 1;
  transform: scale(1);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
  filter: blur(0);
}

.card h4 {
  margin: 0;
  font-size: 20px;
}
</style>