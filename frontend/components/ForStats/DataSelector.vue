<script setup>
  import { Icon } from '@iconify/vue';
import { ref, computed } from 'vue';

const props = defineProps({
  options: {
    type: Object,
    required: true,
  },
})
const selectedKeys = ref([]);
const emitSelectedKeys = defineEmits(['update:selectedKeys']);

const keys = computed(() => {
  return Object.entries(props.options)
    .filter(([_, value]) => value !== null)
    .map(([key]) => ({
      raw: key,
      label: formatKey(key)
    }))
})
function formatKey(key) {
  return key
    .replace(/_/g, ' ')
    .replace(/(\d+)\s(\d+)/g, '$1–$2')
    .replace(/\b\w/g, c => c.toUpperCase())
}
const selectedObjects = computed(() => {
  return selectedKeys.value.map(key => ({
    key,
    value: props.options[key]
  }))
})

const search = ref("");
const open = ref(false);
const action = () => {
  open.value = !open.value
}
const clear = () => {
  selectedKeys.value = [];
  emitSelectedKeys('update:selectedKeys', selectedKeys.value);
}

const filter = () => {
  action();
  emitSelectedKeys('update:selectedKeys', selectedObjects.value);
}
const filteredOptions = computed(() =>
    keys.value.filter(key =>
        key.label.toLowerCase().includes(search.value.toLocaleLowerCase())
    ),
);

function selectAll() {
  selectedKeys.value = keys.value.map(k => k.raw);
  emitSelectedKeys('update:selectedKeys', selectedObjects.value)
}
watch(keys, (newKeys) => {
  if (newKeys.length > 0 && selectedKeys.value.length === 0) {
    selectAll();
  } 
}, { immediate: true})
</script>
<template>
  <div class="component">
    <div class="input-wrapper">
      <input class="type-input text-light" :placeholder="'filter data'" v-model="search" v-on:focus="true" @click="() => action()"/>
        <div v-if="open && selectedKeys.length === 0" class="icon">
          <Icon icon="mdi:chevron-up" />
        </div>
        <div v-else-if="!open && selectedKeys.length === 0" class="icon icon-positioned">
          <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path fill="none" stroke="#a9a9df" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m6 9l6 6l6-6"/></svg>
        </div>
        <div v-else-if="open && selectedKeys.length > 0" class="icon icon-positioned clickable" @click="() => filter()">
          <DoneArrow />
        </div>
        <div v-else-if="!open && selectedKeys.length > 0" class="icon icon-positioned clickable" @click="() => filter()">
          <Close @click="() => clear()"/>
        </div>
    </div>
    <div v-if="open" class="ds_panel panel-dropdown">
      <div class="ds_list panel-list-compact">
        <label v-for="option in filteredOptions" :key="option.raw" class="ds_option panel-option-compact">
          <input class="check-box text-light" type="checkbox" :value="option.raw" v-model="selectedKeys" @click.stop/>
          <span class="option-label">{{ option.label }}</span>
        </label>
      </div>
    </div>
  </div>
</template>
<style scoped>
.component {
  position: relative;
  width: 180px;
}
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
  border: 3px solid #1c1f24;
  background-color: #1d2025;
  border-radius: 0.375rem;
}
.input-wrapper:focus-within {
  border-color: #3b82f6;
}
.check-box {
  max-width: 16px;
  cursor: pointer;
  accent-color: #3b82f6;
}
input {
  background-color: #1d2025;
  border: none;
}
input:focus {
  outline: none;
}
</style>