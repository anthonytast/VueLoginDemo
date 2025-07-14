<script setup>
    // const props = defineProps(['title', 'inputType', 'inputValue'])
    // let inputType = props.inputType
    // let inputValue = props.inputValue
    // let title = props.title
    defineProps({
        title: String, 
        inputType: String, 
        inputValue: String
    })
    defineEmits(['update:inputValue']) // This exports updated value when event take place
</script>

<template>
    <label>
        <div class="label">{{title}}</div>
        <input :type="inputType" :value="inputValue" @input="$emit('update:inputValue', $event.target.value)"/>
    </label>
</template>

<style scoped>

</style>