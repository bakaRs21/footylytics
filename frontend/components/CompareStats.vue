<script setup>
const props = defineProps({
    firstStats: {
        type: Object,
        required: true
    },
    secondStats: {
        type: Object,
        required: true
    },
    firstName: {
        type: String,
        required: false
    },
    secondName: {
        type: String,
        required: false
    },
    type: {
        type: String,
        required: false
    }
})

const cleanFirstStats = computed(() => {
    Object.fromEntries(
        Object.entries(props.firstStats).filter(([_, v]) => v != null)
    )
})
const cleanSecondStats = computed(() => {
    Object.fromEntries(
        Object.entries(props.secondStats).filter(([_, v]) => v != null)
    )
})

const firstForm = computed(() =>{
    cleanFirstStats.value.form?.split("") || null
})
const secondForm = computed(() =>{
    cleanSecondStats.value.form?.split("") || null
})
</script>
<template>
{{ cleanFirstStats }}
{{ cleanSecondStats }}
{{ firstForm }}
{{ secondForm }}
</template>