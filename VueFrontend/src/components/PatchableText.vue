<script setup>
    import { ref, watch } from 'vue'
    import { patchUsersData } from '@/controllers/usersController'
    import formButton from '@/components/FormButton.vue'

    const props = defineProps({
        usersData: Object,
        isEditing: Boolean
    })
    const emit = defineEmits(['update:isEditing']) // This exports updated value when event take place

    const first_name = ref(props.usersData.first_name)
    const last_name = ref('')
    const phone_number = ref('')

    // 🔁 Watch for when usersData becomes available and update local refs
    //onMounted(()=> {
    //first_name.value = props.userData.first_name})


    watch(
    () => props.usersData,
    (newVal) => {
        if (newVal) {
        first_name.value = newVal.first_name
        last_name.value = newVal.last_name
        phone_number.value = newVal.phone_number
        }
    },
    { immediate: true }
    )

    const submitChanges = () => {
        patchUsersData(
            props.usersData.username,
            first_name.value,
            last_name.value,
            phone_number.value
        )
        emit('update:isEditing', false)
        
        window.location.reload()
    }

</script>

<template>
    <!-- <label>
        <div class="label">{{title}}</div>
        <input :type="inputType" :value="inputValue" @input="$emit('update:inputValue', $event.target.value)"/>
    </label> -->
    <div v-if="!props.isEditing">
        <p>{{ props.usersData.first_name }}</p>
        <br>
        <p>{{ props.usersData.last_name }}</p>
        <br>
        <p>{{ props.usersData.phone_number }}</p>
    </div>
    <div v-else>
        <input v-model="first_name" />
        <br>
        <input v-model="last_name" />
        <br>
        <input v-model="phone_number" />
        <br>
        <formButton :button_func = "submitChanges" :text="'Submit Changes'"/>
    </div>
</template>