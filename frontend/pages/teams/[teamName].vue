<script setup>
const teamName = useRoute().params.teamName
</script>
<template>
<pre>You've selected team: {{ teamName }}</pre>
</template>