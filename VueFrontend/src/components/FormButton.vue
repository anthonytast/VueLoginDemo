<script setup>
    const props = defineProps({
        button_func: Function,
        text: String
    })
</script>

<template>
    <button @click.prevent="button_func()" class="btn btn-primary">{{ text }}</button>
</template>
