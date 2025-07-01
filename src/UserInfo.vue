<script setup>
    import { useRoute, useRouter } from 'vue-router'
    // import usersData from './DB/LoginBackend'
    const router = useRouter()
    const route = useRoute()
    import {getUsersData} from './API/UsersController'
    const username = route.query.username ?? ''
    const usersData = getUsersData(username)
    const isLoggedIn = route.query.login ?? ''

    console.log('username on users page: ', route.query)
    console.log('usersData:', usersData)

    // const usersData = {
    //     firstname: "Anthony",
    //     lastname: "Tast",
    //     phonenumber: "6319257508",
    // }
</script>

<template>
    <template v-if="username && (isLoggedIn === 'true')">
        <!-- <template v-if="username && isLoggedIn"> -->
        <h1>{{ username }}</h1>
        <br>
        <p>{{ usersData.firstName }}</p>
        <br>
        <p>{{ usersData.lastName }}</p>
        <br>
        <p>{{ usersData.phoneNumber }}</p>
    </template>
 <template v-else>
    <h1>No user found!</h1>
 </template>
</template>