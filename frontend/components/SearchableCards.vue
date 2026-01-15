<script setup>
import { ref, watch, computed } from 'vue';

const search = ref("");
const count = ref(0);

const props = defineProps({
    items: {
        type: Array,
        required: true
    },
    placeholder: {
        type: String,
        default: "Search..."
    },
    enableLinks: {
        type: Boolean,
        default: true
    },
    page: {
        type: String,
        required: true
    }
});
const getItemId = (item) => {
  const key = `${props.page}_id`
  return item[key]
}

const filteredItems = computed(() => {
    if (!search.value.trim()) return props.items
    
    const searchLower = search.value.toLowerCase().trim()
    return props.items.filter((item) => {
        if (props.page === 'season') {
            const season = item.season ?? ''
            return season.toLowerCase().includes(searchLower)
        } else {
            const name = item.name ?? ''
            return name.toLowerCase().includes(searchLower)
        }
    })
});
watch(filteredItems, (newItems) => {
    count.value = newItems.length;
}, 
    { immediate: true }
);

</script>
<template>
    <div class="panel">
        <div class="left">
            <pre>Count: {{ count }}</pre>
        </div>
        <div class="right">
            <input v-model="search" type="text" :placeholder="placeholder"/>
        </div>
    </div>
    <hr />
    <div class="cards">
        <NuxtLink v-if="enableLinks" v-for="item in filteredItems" :key="getItemId(item)"  :to="`/${page}s/${getItemId(item)}`">
            <card v-if="page !== 'season'">{{ item.name }}</card>
            <card v-else>{{ item.season }}</card>
        </NuxtLink>
        <card v-else v-for="itm in filteredItems" :key="getItemId(itm)">{{ itm.name }}</card>
        <p v-if="filteredItems.length == 0">No items match {{ search }}</p>
    </div>
</template>

<style scoped>
.panel {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}
.left {
    display: flex;
    flex-shrink: 0;
    margin-left: 30px;
}
.right {
    flex: 1;
    display: flex;
    justify-content: flex-end;
}
input {
    justify-content: flex-end;
    margin: 15px 0 15px 0;
    padding: 8px 15px 8px 15px;
    font-size: 13px;
    background-color: #303030c4;
    color: white;
    border: 1px solid #3d4249d2;
    border-radius: 10px;

}
input:focus {
    outline: none;
    border-color: #5a9bfca6;
}
</style>