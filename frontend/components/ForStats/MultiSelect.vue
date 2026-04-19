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
    <div class="msc_input input-dropdown" @click="toggleOpen">
      <span class="msc__text text-ellipsis">{{ selectedLabels }}</span>
      <span class="msc__chev">▾</span>
    </div>

    <div v-if="open" class="msc_panel panel-multiselect" @click.stop>
      <div class="msc_list panel-list">
        <label v-for="o in normalizedOptions" :key="o.key" class="msc_option panel-option">
          <input
            type="checkbox"
            :checked="localSelected.includes(o.key)"
            @change="() => toggleKey(o.key)"
          />
          <span>{{ o.label }}</span>
        </label>
      </div>

      <div class="msc_actions">
        <button class="msc_btn secondary btn-secondary" type="button" @click="clear">Clear</button>
        <button class="msc_btn primary btn-primary" type="button" @click="confirm">Confirm</button>
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
.msc_actions {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  padding: 10px;
  border-top: 1px solid rgba(255,255,255,0.08);
}
</style>