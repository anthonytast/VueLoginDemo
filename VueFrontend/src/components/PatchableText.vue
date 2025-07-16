<script setup>
import api from '@/controllers/api';

    defineProps({
        usersData: Object,
        isEditing: Boolean
    })
    defineEmits(['update:inputValue']) // This exports updated value when event take place

</script>

<template>
    <!-- <label>
        <div class="label">{{title}}</div>
        <input :type="inputType" :value="inputValue" @input="$emit('update:inputValue', $event.target.value)"/>
    </label> -->
    <div v-if="!isEditing">
        <p>{{ usersData.first_name }}</p>
        <br>
        <p>{{ usersData.last_name }}</p>
        <br>
        <p>{{ usersData.phone_number }}</p>
    </div>
    <div v-else>
        <input :value="usersData.first_name" @input="$emit('update:inputValue', $event.target.value)"/>
        <br>
        <input :type="usersData.last_name" :value="inputValue" @input="$emit('update:inputValue', $event.target.value)"/>
        <br>
        <input :type="usersData.phone_number" :value="inputValue" @input="$emit('update:inputValue', $event.target.value)"/>
    </div>
</template>