import api from './api.js';
import { useLoginStore } from '@/stores/auth'

export const login = async (username, password) => {
    // return ((username in usersData) && (usersData[username].password == password))
    try {
        const response = await api.post(`/users/login?username=${username}&password=${password}`)
        console.assert(response.status == 200)
        // console.log("login response:", response)
        // console.log("login value", response.data.login)
        const authStore = useLoginStore()
        authStore.successfulLogin(username)
        return response.data.login
    } catch (error) {
        console.error("Login API Error")
        return false
    }
}

export const getUsersData = async (username) => {
    try {
        const response = await api.get(`/users/${username}`);
        console.log("user data response:", response.data)
        return response.data
    } catch (error) {
        console.error("Could not get user data")
    }
}

// export const loginSaveInfo = async ({username, password}) => { // seperate concerns V and M
//     const loginSuccess = await login(username, password);
//     if (loginSuccess) {
//         loginStore.loginSuccess(username)
//     } else 
// }

// Needs to be async if making asynchronous api calls