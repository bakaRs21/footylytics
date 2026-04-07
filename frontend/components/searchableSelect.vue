<script setup>
import { Icon } from '@iconify/vue';
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
            <Icon icon="mdi:check" />
        </div>
        <div v-else-if="!open && !optionSelected">
            <Icon icon="mdi:magnify" />
        </div>
        <div v-else-if="optionSelected" class="svg-x" @click="erase">
            <Icon icon="mdi:close" />
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