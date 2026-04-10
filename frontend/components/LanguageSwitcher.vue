<script setup lang="ts">
const { locale, locales } = useI18n()
const switchLocalePath = useSwitchLocalePath()

const availableLocales = computed(() => {
  return locales.value
})
</script>

<template>
  <div class="lang-switcher" role="navigation" aria-label="Language Switcher">
    <NuxtLink
      v-for="loc in availableLocales"
      :key="loc.code"
      :to="switchLocalePath(loc.code)"
      :class="['lang-option', { active: locale === loc.code }]"
      :aria-current="locale === loc.code ? 'true' : undefined"
    >
      {{ loc.code.toUpperCase() }}
    </NuxtLink>
  </div>
</template>

<style scoped>
.lang-switcher {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  padding: 3px;
}

.lang-option {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.5);
  transition:
    background 180ms ease,
    color 180ms ease;
}

.lang-option:hover:not(.active) {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.85);
}

.lang-option.active {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  font-weight: 600;
}

.flag {
  font-size: 0.85rem;
  line-height: 1;
}

.code {
  line-height: 1;
}
</style>