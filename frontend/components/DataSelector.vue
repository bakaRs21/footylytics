<script setup>
  import { ref, computed } from 'vue';
import DoneArrow from './Icons/DoneArrow.vue';
import Close from './Icons/Close.vue';

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
    if (open.value == false) {
        open.value = true;
    } else {
        open.value = false;
    }
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

</script>
<template>
  <div class="component">
        <input class="type-input" :placeholder="'filter data'" v-model="search" v-on:focus="true" @click="() => action()"/>
        <div v-if="open && selectedKeys.length === 0">
          <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path fill="none" stroke="#a9a9df" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m18 15l-6-6l-6 6"/></svg>
        </div>
        <div v-else-if="!open && selectedKeys.length === 0">
          <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path fill="none" stroke="#a9a9df" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m6 9l6 6l6-6"/></svg>
        </div>
        <div v-else-if="open && selectedKeys.length > 0" class="svg-x" @click="() => filter()">
          <DoneArrow />
        </div>
        <div v-else-if="!open && selectedKeys.length > 0" class="svg-x">
          <Close @click="() => clear()"/>
        </div>
        <ul v-if="open" class="onOpen">
            <li v-for="option in filteredOptions" :key="option.raw">
              <input class="check-box" type="checkbox" :value="option.raw" v-model="selectedKeys" @click.stop/>
              {{ option.label }}
            </li>
        </ul>
    </div>
</template>
<style scoped>
.component {
  position: relative;
  width: 100px;
}
.type-input {
    width: 100%; 
    border-radius: 0.5rem;
    border: none;
    padding: 4px 30px 6px 12px;
    background-color: #252525e8;
    color: white;
    transition: all 0.15s ease;
}
.type-input:focus {
    outline: none;
    box-shadow: 0 0 0 3px #4d576685;
}
.type-input::placeholder {
    color: #dddddd;
}
.svg {
    position: absolute; 
    top: 50%; 
    right: -2.5rem; 
    transform: translateY(-50%);
    pointer-events: none;
}
.svg-x {
    position: absolute; 
    top: 55%; 
    right: -2.4rem; 
    transform: translateY(-50%);
}

ul {
    position: absolute; 
    z-index: 10; 
    margin: 2px 0 0 -8px;
    max-height: 16rem;
    padding: 0;
    width: 170px; 
    overflow-y: auto; 
    border-radius: 0.75rem 0.75rem 0.75rem 0.75rem;
    background-color: #303030e3;
}
ul li {
  display: flex;
  flex-direction: row;
  cursor: pointer; 
  padding: 0.5rem 0.5rem 0.5rem 0.5rem;
  background-color: #3d3c3ce7;
  font-size: 12px;
}
.chek-box {
  max-width: 16px;
}
</style>