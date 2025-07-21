import { ref, onMounted, onUnmounted } from 'vue'

export function useLogin() {

  const username = ref(null)

  function successfulLogin(user_login) {
    username.value = user_login
  }
  
  function logoutUser() {
    username.value = null
  }

  onMounted(() => {
    const localStorageUsername = localStorage.getItem('username')
    if (localStorageUsername) successfulLogin(localStorageUsername) //jwt is checked after username is assigned by state
  })
  onUnmounted(() => {
    logoutUser() // user is moved removed from state storage on each time for security purposes, new check on every page refresh
  })

  return { username, successfulLogin, logoutUser }
}