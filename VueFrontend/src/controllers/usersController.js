import api from './api.js';
import { useLoginStore } from '@/stores/auth'

export const login = async (username, password) => {
    try {
        const response = await api.post('/users/token', null, {
            params: { username, password }
        });

        const { access_token } = response.data;
        if (!access_token) throw new Error("No token received");

        localStorage.setItem("token", access_token);
        localStorage.setItem("username", username);

        const authStore = useLoginStore();
        authStore.successfulLogin(username);

        return true;
    } catch (error) {
        console.error("Login failed:", error);
        return false;
    }
}

export const getUsersData = async () => {
    try {
        const response = await api.get('/users/verify');
        return response.data;
    } catch (error) {
        console.error("Token invalid or expired", error);
        return null;
    }
}


// export const loginSaveInfo = async ({username, password}) => { // seperate concerns V and M
//     const loginSuccess = await login(username, password);
//     if (loginSuccess) {
//         loginStore.loginSuccess(username)
//     } else 
// }

// Needs to be async if making asynchronous api calls