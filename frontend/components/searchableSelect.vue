<script setup>
import { ref, computed, watch } from 'vue';
const props = defineProps({
    modelValue: {
        type: String,
        default: ""
    }, 
    options: {
        type: Array,
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

const filteredOptions = computed(() =>
    props.options.filter(option =>
        option.toLowerCase().includes(search.value.toLocaleLowerCase())
    )
);
const action = () => {
    if (open.value == false) {
        open.value = true;
    } else {
        open.value = false;
    }
}
const selectOption = (item) => {
    emit('update:modelValue', item);
    search.value = item;
    open.value = false;
}
watch(() => props.modelValue, val => {
    search.value = val
},
    { immediate: true }
);

</script>
<template>
    <div class="component">
        <input :placeholder="placeholder" v-model="search" v-on:focus="true" @click="() => action()"/>
        <div v-if="open">
            <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path fill="none" stroke="#a9a9df" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m18 15l-6-6l-6 6"/></svg>
        </div>
        <div v-else>
            <svg class="svg" xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path fill="none" stroke="#a9a9df" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m6 9l6 6l6-6"/></svg>
        </div>
        <ul v-if="open" class="onOpen">
            <li v-for="option in filteredOptions" :key="option" @click="() => selectOption(option)">{{ option }}</li>
        </ul>
    </div>

</template>
<style scoped>
.component {
    position: relative;
    width: 100px;   
}
input {
    width: 100%; 
    border-radius: 0.5rem;
    border: none;
    padding: 0.75rem 2rem 0.75rem 1.5rem;
    background-color: #4d4d4de8;
    color: white;
    transition: all 0.15s ease;
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
    right: -2.8rem; 
    transform: translateY(-50%);
    pointer-events: none;
}

ul {
    position: absolute; 
    z-index: 10; 
    margin: 2px 0 0 2px;
    max-height: 12rem;
    padding: 0;
    width: 150px; 
    overflow-y: auto; 
    border-radius: 0.75rem 0.75rem 0.75rem 0.75rem;
    background-color: #303030e3;
}
ul li {
    cursor: pointer; 
    padding: 0.5rem 0.75rem 0.5rem 0.75rem;
    background-color: #504e4ee7;
}
</style>