<script setup>
    import { ref } from 'vue';
    import textInput from './components/TextInput.vue'
    import formButton from './components/FormButton.vue'
    // import {isSuccessfulLoginAlert} from './API/UsersController'
    import {loginPushToUserInfo} from '../controllers/usersController'
    import clearForm from '../controllers/formController'
    import { useRouter } from 'vue-router'
    const router = useRouter();
    const username = ref("");
    const password = ref("");

</script>

<template>
  <form class="card" >
    <div>
      <h2>Login to Your Account</h2>

      <textInput :title="`Username`" :inputType="'text'" v-model:inputValue="username"/> <!-- Can use v-model:inputValue instead of v-model because our changing value is not title the default: modelValue-->
      <textInput :title="`Password`" :inputType="'password'" v-model:inputValue="password"/>
      
      <div class="card-actions">
        <formButton :button_func = "() => loginPushToUserInfo({router:router, username:username, password:password})" :text="'Login'"/>
        <formButton :button_func = "() => clearForm(username, password)" :text = "'Clear'"/>
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