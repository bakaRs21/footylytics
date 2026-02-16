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
</script>