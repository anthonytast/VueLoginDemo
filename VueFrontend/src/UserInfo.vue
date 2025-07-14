<script setup>
    import {ref, onMounted} from 'vue';
    import {getUsersData} from './API/UsersController'
    const username = localStorage.getItem('username')
    const usersData = ref(null)
    const isLoggedIn = localStorage.getItem('login')

    // console.log('username on users page: ', route.query)
    console.log('usersData:', usersData)

    const isWaiting = ref(true)
    onMounted(async () => {
        usersData.value = await getUsersData(username);
        isWaiting.value = false
        console.log('usersData:', usersData.value);
    });

</script>

<!-- NEXT STEPS IS TO TAKE INTO ACCOUNT SECURITY ASPECTS -->
<template>
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