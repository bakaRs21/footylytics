<script setup lang="ts">
const { finalizePendingLocaleChange } = useI18n()
const onBeforeEnter = async () => {
    await finalizePendingLocaleChange()
}
useHead({
  meta: [{ name: 'viewport', content: 'width=device-width, initial-scale=1' }]
})
</script>
<template>
    <NuxtLayout>
        <NuxtPage 
        :transition="{
            name: 'my',
            mode: 'out-in',
            onBeforeEnter
        }"
        />
    </NuxtLayout>
</template>
<style scoped>
.my-enter-active,
.my-leave-active {
  transition: opacity 0.3s;
}
.my-enter,
.my-leave-active {
  opacity: 0;
}
</style>