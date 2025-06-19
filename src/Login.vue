<script setup>
    import { ref } from 'vue';
    import textInput from './components/TextInput.vue'
    import clear from './components/ClearButton.vue'
    import logins from './DB/LoginBackend.js'
    const username = ref("")
    const password = ref("")
    const login = () => {
        if ((username.value in logins) && (logins[username.value] == password.value)) {
            window.alert("Login Success!")
        }
        console.log(username.value, password.value)
    }
    const canBeCleared = ref([username, password])
</script>

<template>
  <form class="card" >
    <div class="card-body">
      <h2 class="card-title">Login to Your Account</h2>

      <textInput :title="`Username`" :inputType="'text'" v-model:inputValue="username"/> <!-- Can use v-model:inputValue instead of v-model because our changing value is not title the default: modelValue-->
      <textInput :title="`Password`" :inputType="'password'" v-model:inputValue="password"/>
      
      <div class="card-actions">
        <button @click.prevent="login()" class="btn btn-primary">Login</button>
        <clear v-model:toBeCleared = "canBeCleared"/>
      </div>

    </div>
  </form>
</template>

<style scoped>
    .card {
        text-align: center;
    }
    h2 {
        text-align: center;
        font-weight: bold;

    }
    button {
        padding: 1em 2em;
        margin-top: 0.5em;
        background-color: lightblue;
    }
</style>