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

export const patchUsersData = async (username, first_name, last_name, phone_number) => {
    try {
        // should add an additional verification here maybe
        const response = await api.patch(`/users/${username}`, params={'username':username, 'first_name':first_name, 'last_name':last_name, 'phone_number':phone_number});
        return response.data;
    } catch (error) {
        console.error("Token invalid or expired", error);
        return null;
    }
}