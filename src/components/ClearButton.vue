<script setup>
    import { isRef } from 'vue'
    const props = defineProps({
        toBeCleared: {type: Array, required: true}
    })
    const emit = defineEmits(['update:toBeCleared'])
    const clear = () => {
        console.log("clear function was run")
        props.toBeCleared.forEach(prop => { // had to use forEach because regular for loop didn't work here
            if (isRef(prop)) {
            prop.value = ''
            }
        })
    }
</script>

<template>
    <button @click.prevent="clear()" class="btn btn-primary">Clear</button>
</template>