<script setup>
    import {ref, onMounted} from 'vue';
    import { getUsersData } from '@/controllers/usersController'
    import { useLoginStore } from '@/stores/auth'
    import { storeToRefs } from 'pinia'
    const usersData = ref(null)

    const auth = useLoginStore()
    const { username, login } = storeToRefs(auth)

    // console.log('username on users page: ', route.query)
    console.log('usersData:', usersData)

    const isWaiting = ref(true)

    onMounted(async () => {
        usersData.value = await getUsersData(username.value);
        isWaiting.value = false
        console.log('usersData:', usersData.value);
    });

</script>

<!-- NEXT STEPS IS TO TAKE INTO ACCOUNT SECURITY ASPECTS -->
<template>
    <template v-if="login">
        <template v-if="!isWaiting">
        <!-- <template v-if="username && isLoggedIn"> -->
            <h1>{{ username }}</h1>
            <br>
            <p>{{ usersData.first_name }}</p>
            <br>
            <p>{{ usersData.last_name }}</p>
            <br>
            <p>{{ usersData.phone_number }}</p>
        </template>
        <template v-else>
            <h1>Loading User...</h1>
        </template>
    </template>
    <template v-else>
        <p>No User Found!</p>
    </template>
</template>