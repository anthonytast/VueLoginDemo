<script setup>
  import { ref } from 'vue';
  import TextInput from '@/components/TextInput.vue'
  import FormButton from '@/components/FormButton.vue'
  import { login } from '@/controllers/usersController'
  import { clearForm } from '@/controllers/formController'
  import { useRouter } from 'vue-router'
  const router = useRouter();
  const username = ref("");
  const password = ref("");

  const loginPush = async (username, password) => {
    const isSuccessfulLogin = await login(username, password)
    if (isSuccessfulLogin) { // pinia store will be checked on UserInfo page, not here
      router.push({path: '/user-info'})
    } else window.alert("Login Failed :(")
  }

</script>

<template>
  <form class="card" >
    <div>
      <h2>Login to Your Account</h2>

      <TextInput :title="`Username`" :inputType="'text'" v-model:inputValue="username"/> <!-- Can use v-model:inputValue instead of v-model because our changing value is not title the default: modelValue-->
      <TextInput :title="`Password`" :inputType="'password'" v-model:inputValue="password"/>
      
      <div class="card-actions">
        <FormButton :button_func = "() => loginPush(username, password)" :text="'Login'"/>
        <FormButton :button_func = "() => clearForm(username, password)" :text = "'Clear'"/>
        <FormButton :button_func = "() => router.push('/sign-up')" :text = "'Sign Up'"/>
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