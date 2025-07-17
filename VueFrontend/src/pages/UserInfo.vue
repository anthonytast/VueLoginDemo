<script setup>
    import {ref, onMounted} from 'vue';
    import { getUsersData } from '@/controllers/usersController'
    import { deleteUser } from '@/controllers/usersController'
    import { useLoginStore } from '@/stores/auth'
    import { storeToRefs } from 'pinia'
    import PatchableText from '@/components/PatchableText.vue';
    import formButton from '@/components/FormButton.vue'
    import router from '@/router';
    const usersData = ref(null)

    const auth = useLoginStore()
    const { username, login } = storeToRefs(auth)

    // console.log('username on users page: ', route.query)
    console.log('usersData:', usersData)

    const logout = () => {
        localStorage.removeItem('token')
        localStorage.removeItem('username')
        auth.logoutUser()
        router.push("/")
    }

    const del = async (un) => {
        localStorage.removeItem('token')
        localStorage.removeItem('username')

        auth.logoutUser()
        await deleteUser(un)

        router.push("/")
    }

    const isWaiting = ref(true)
    const isEditing = ref(false)

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
            <PatchableText :usersData="usersData" v-bind:isEditing="isEditing"/>
            <br>
            <div class="card-actions">
                <formButton :button_func = "() => isEditing = !isEditing" :text="'Edit'"/>
                <formButton :button_func = "() => logout()" :text="'Logout'"/>
                <formButton :button_func = "() => del(username)" :text="'Delete User'"/>
            </div>
        </template>
        <template v-else>
            <h1>Loading User...</h1>
        </template>
    </template>
    <template v-else>
        <p>No User Found!</p>
    </template>
</template>