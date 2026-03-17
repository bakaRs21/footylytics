<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  options: {
    type: Array,
    required: true,
  },
  modelValue: {
    type: Array,
    default: () => [],
  },
  placeholder: {
    type: String,
    default: 'Select metrics…',
  }
})

const emit = defineEmits([
  'update:modelValue',
  'confirm',
])

const open = ref(false)
const localSelected = ref([...(props.modelValue ?? [])])

watch(() => props.modelValue,
  (v) => { localSelected.value = [...(v ?? [])] },
  { deep: true, immediate: true }
)

const normalizedOptions = computed(() => {
  return (props.options ?? []).map(o => {
    if (typeof o === 'string') return { key: o, label: o }
    return { key: o.key, label: o.label ?? o.key }
  })
})

const selectedLabels = computed(() => {
  if (!localSelected.value.length) return props.placeholder
  const map = new Map(normalizedOptions.value.map(o => [o.key, o.label]))
  return localSelected.value.map(k => map.get(k) ?? k).join(', ')
})

function toggleOpen() {
  open.value = !open.value
}
function close() {
  open.value = false
}
function toggleKey(key) {
  const set = new Set(localSelected.value)
  if (set.has(key)) set.delete(key)
  else set.add(key)
  localSelected.value = Array.from(set)
  emit('update:modelValue', localSelected.value)
}
function confirm() {
  emit('confirm', localSelected.value)
  close()
}
function clear() {
  localSelected.value = []
  emit('update:modelValue', [])
}
</script>

<template>
  <div class="msc" @mouseleave="close">
    <div class="msc_input" @click="toggleOpen">
      <span class="msc__text">{{ selectedLabels }}</span>
      <span class="msc__chev">▾</span>
    </div>

    <div v-if="open" class="msc_panel" @click.stop>
      <div class="msc_list">
        <label v-for="o in normalizedOptions" :key="o.key" class="msc_option">
          <input
            type="checkbox"
            :checked="localSelected.includes(o.key)"
            @change="() => toggleKey(o.key)"
          />
          <span>{{ o.label }}</span>
        </label>
      </div>

      <div class="msc_actions">
        <button class="msc_btn secondary" type="button" @click="clear">Clear</button>
        <button class="msc_btn primary" type="button" @click="confirm">Confirm</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.msc {
  position: relative;
  width: 260px;
  font-size: 14px;
}
.msc_input {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;

  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #374153;
  background: #111822;
  color: white;
  cursor: pointer;
}
.msc_text {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.msc_panel {
  position: absolute;
  top: calc(100%);
  left: 0;
  width: 100%;
  z-index: 50;

  border: 1px solid #374153;
  border-radius: 10px;
  background: #0b1220;
  color: white;
  box-shadow: 0 10px 24px rgba(0,0,0,0.35);
  overflow: hidden;
}
.msc_list {
  max-height: 220px;
  overflow: auto;
  padding: 8px;
}
.msc_option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 6px;
  cursor: pointer;
  border-radius: 8px;
}
.msc_option:hover {
  background: rgba(255,255,255,0.06);
}
.msc_actions {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  padding: 10px;
  border-top: 1px solid rgba(255,255,255,0.08);
}
.msc_btn {
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  font-weight: 600;
}
.msc_btn.primary {
  background: #0369a1;
  color: white;
}
.msc_btn.primary:hover {
  background: #0284c7;
}
.msc_btn.secondary {
  background: transparent;
  color: #cbd5e1;
  border: 1px solid rgba(255,255,255,0.18);
}
.msc_btn.secondary:hover {
  background: rgba(255,255,255,0.06);
}
</style>