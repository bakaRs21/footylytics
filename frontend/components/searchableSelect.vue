<script setup>
import { ref, computed, watch } from 'vue';
const props = defineProps({
    modelValue: {
        type: [Object, String],
        default: null
    }, 
    options: {
        type: Array,
        required: true
    },
    page: {
        type: String,
        required: true
    },
    placeholder: {
        type: String,
        default: "Select..."
    }
});

const emit = defineEmits(['update:modelValue']);

const search = ref("");
const open = ref(false);
const optionSelected = ref(false);

const filteredOptions = computed(() =>
    props.options.filter(option =>
        option.name.toLowerCase().includes((search.value ?? "").toLowerCase())
    )
);
const action = () => {
    if (open.value == false) {
        open.value = true;
    } else {
        open.value = false;
    }
}
const erase = () => {
    optionSelected.value = false;
    search.value = '';
    emit('update:modelValue', '');
}
const selectOption = (item) => {
    emit('update:modelValue', item);
    search.value = item.name;
    open.value = false;
    optionSelected.value = true;
}
watch(() => props.modelValue, val => {
    if (typeof val === "object" && val !== null) {
        search.value = val.name
    } else {
        search.value = val ?? ""
    }
},{ immediate: true });

</script>
<template>
    <div class="component">
        <input :placeholder="placeholder" v-model="search" @click="action"/>
        <div v-if="open && !optionSelected">
            <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path fill="none" stroke="#a9a9df" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m18 15l-6-6l-6 6"/></svg>
        </div>
        <div v-else-if="!open && !optionSelected">
            <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path fill="none" stroke="#a9a9df" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m6 9l6 6l6-6"/></svg>
        </div>
        <div v-else-if="optionSelected" class="svg-x" @click="erase">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><defs><path id="SVG0kegTdID" fill="#a9a9df" d="M8 6.943L1.807.75L.75 1.807L6.943 8L.75 14.193l1.057 1.057L8 9.057l6.193 6.193l1.057-1.057L9.057 8l6.193-6.193L14.193.75z"/></defs><use fill-rule="evenodd" href="#SVG0kegTdID" transform="translate(4 4)"/></svg>
        </div>
        <ul v-if="open" class="onOpen">
            <li v-for="option in filteredOptions" :key="option" @click="selectOption(option)">{{ option.name }}</li>
        </ul>
    </div>

</template>
<style scoped>
.component {
    position: relative;
    width: 100%;
    min-width: 150px;
}
input {
    border-radius: 0.5rem;
    border: none;
    padding: 0.75rem 1.5rem 0.75rem 1.5rem;
    background-color: #4d4d4de8;
    color: white;
    transition: all 0.15s ease;
    width: 100%;
    box-sizing: border-box;
}
input:focus {
    outline: none;
    box-shadow: 0 0 0 3px #889ab385;
}
input::placeholder {
    color: #dddddd;
}

.svg {
    position: absolute; 
    top: 50%; 
    right: 0.75rem; 
    transform: translateY(-50%);
    pointer-events: none;
}
.svg-x {
    cursor: pointer;
    position: absolute; 
    top: 50%; 
    right: 0.75rem; 
    transform: translateY(-50%);
}

ul {
    position: absolute; 
    z-index: 10; 
    margin: 4px 0 0 0;
    max-height: 16rem;
    padding: 0;
    width: 100%; 
    overflow-y: auto; 
    border-radius: 0.75rem;
    background-color: #303030e3;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
ul li {
    cursor: pointer; 
    padding: 0.5rem 0.75rem 0.5rem 0.75rem;
    background-color: #504e4ee7;
    transition: background 0.2s;
}
ul li:hover {
    background-color: #666464e7;
}
</style>