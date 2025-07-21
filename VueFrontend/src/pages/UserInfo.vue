<script setup>
    import {ref, onMounted} from 'vue';
    import { getUser } from '@/controllers/usersController'
    import { deleteUser } from '@/controllers/usersController'
    import { useLogin } from '@/composables/auth'
    import PatchableText from '@/components/PatchableText.vue';
    import FormButton from '@/components/FormButton.vue'
    import router from '@/router';
    const usersData = ref(null)

    const { username, logoutUser } = useLogin()
    // console.log('username on users page: ', route.query)
    console.log('usersData:', usersData)

    const logout = () => {
        localStorage.removeItem('token')
        localStorage.removeItem('username')
        logoutUser()
        router.push("/")
    }

    const del = async (un) => {
        localStorage.removeItem('token')
        localStorage.removeItem('username')

        logoutUser()
        await deleteUser(un)

        router.push("/")
    }

    const isWaiting = ref(true)
    const isEditing = ref(false)

    onMounted(async () => {
        usersData.value = await getUser(username.value);
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
        <PatchableText :usersData="usersData" v-bind:isEditing="isEditing"/>
        <br>
        <div class="card-actions">
            <FormButton :button_func = "() => isEditing = !isEditing" :text="'Edit'"/>
            <FormButton :button_func = "() => logout()" :text="'Logout'"/>
            <FormButton :button_func = "() => del(username)" :text="'Delete User'"/>
        </div>
    </template>
    <template v-else>
        <h1>Loading User...</h1>
    </template>
</template>