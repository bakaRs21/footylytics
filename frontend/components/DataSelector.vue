<script setup>
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
      <input class="type-input" :placeholder="'filter data'" v-model="search" v-on:focus="true" @click="() => action()"/>
        <div v-if="open && selectedKeys.length === 0" class="icon">
          <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path fill="none" stroke="#a9a9df" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m18 15l-6-6l-6 6"/></svg>
        </div>
        <div v-else-if="!open && selectedKeys.length === 0" class="icon">
          <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path fill="none" stroke="#a9a9df" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m6 9l6 6l6-6"/></svg>
        </div>
        <div v-else-if="open && selectedKeys.length > 0" class="icon icon-clickable" @click="() => filter()">
          <DoneArrow />
        </div>
        <div v-else-if="!open && selectedKeys.length > 0" class="icon icon-clickable" @click="() => filter()">
          <Close @click="() => clear()"/>
        </div>
    </div>
    <div v-if="open" class="ds_panel">
      <div class="ds_list">
        <label v-for="option in filteredOptions" :key="option.raw" class="ds_option">
          <input class="check-box" type="checkbox" :value="option.raw" v-model="selectedKeys" @click.stop/>
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
}
.type-input {
    width: 100%; 
    border-radius: 0.5rem;
    border: none;
    padding: 6px 36px 6px 12px;
    background-color: #0f131b;
    color: white;
    transition: all 0.15s ease;
    box-sizing: border-box;
  }
.type-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px #4d576685;
}
.type-input::placeholder {
    color: #8899aa;
}
.icon {
    position: absolute; 
    top: 50%; 
    right: 0.5rem; 
    transform: translateY(-50%);
    pointer-events: none;
    display: flex;
    align-items: center;
    justify-content: center;
}
.icon-clickable {
  pointer-events: auto;
  cursor: pointer;
}
.ds_panel {
  position: absolute;
  top: calc(100%);
  left: 0;
  width: 100%;
  z-index: 50;
  overflow-y: auto;
  border-radius: 0.5rem;
  background-color: #1a2332;
  border: 1px solid #2d3a4a;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}
.ds_list {
  max-height: 120px;
  overflow: auto;
  padding: 4px;
}
.ds_option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 6px;
  cursor: pointer;
  border-radius: 0.5rem;
}
.ds_option:hover {
  background-color: #243044;
}
.option-label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.8rem;
}
.check-box {
  max-width: 16px;
  cursor: pointer;
  accent-color: #3b82f6;
}
</style>