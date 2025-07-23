import { ref, onMounted, onUnmounted } from 'vue'

export const useLogin = () => {

  const username = ref(null)

  const successfulLogin = (user_login) => {
    username.value = user_login
  }
  
  const logoutUser = () => {
    username.value = null
  }

  onMounted(() => {
    const localStorageUsername = localStorage.getItem('username')
    if (localStorageUsername) successfulLogin(localStorageUsername) //jwt is checked after username is assigned by state
    // console.log("MOUNT:", username.value)
  })
  onUnmounted(() => {
    logoutUser() // user is moved removed from state storage on each time for security purposes, new check on every page refresh
    // console.log("UNMOUNT:", username.value)
  })

  return { username, successfulLogin, logoutUser }
}