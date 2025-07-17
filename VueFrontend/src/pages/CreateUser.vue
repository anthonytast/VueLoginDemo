<script setup>
    import {ref} from 'vue';
    import { createUser } from '@/controllers/usersController';
    import FormButton from '@/components/FormButton.vue';
    import TextInput from '@/components/TextInput.vue'
    import { clearForm } from '@/controllers/formController'
    import { useRouter } from 'vue-router'
    const router = useRouter();
    const username = ref("");
    const first_name = ref("");
    const last_name = ref("");
    const phone_number = ref("");
    const password1 = ref("");
    const password2 = ref("");
    const pushUserCreation = async () => {
        if ((username.value, first_name.value, last_name.value, phone_number.value, password1.value, password2.value != "") && (password1.value == password2.value)) {
        await createUser(username.value, first_name.value, last_name.value, phone_number.value, password1.value)
        router.push("/")
        } else {
            window.alert("Enter a value for each field. Make sure passwords match")
        }
    }
</script>

<template>
  <form class="card" >
    <div>
      <h2>Create an Account</h2>

      <TextInput :title="`Username`" :inputType="'text'" v-model:inputValue="username"/>
      <TextInput :title="`First name`" :inputType="'text'" v-model:inputValue="first_name"/>
      <TextInput :title="`Last name`" :inputType="'text'" v-model:inputValue="last_name"/>
      <TextInput :title="`Phone number`" :inputType="'text'" v-model:inputValue="phone_number"/>
      <TextInput :title="`Password`" :inputType="'password'" v-model:inputValue="password1"/>
      <TextInput :title="`Confirm Password`" :inputType="'password'" v-model:inputValue="password2"/>

      
      <div class="card-actions">
        <FormButton :button_func = "() => pushUserCreation(username, password)" :text="'Create Account'"/>
        <FormButton :button_func = "() => clearForm(username, first_name, last_name, phone_number, password1, password2)" :text = "'Clear'"/>
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