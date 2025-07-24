import api from './api.js';
import qs from 'qs';
// import { useLogin } from '@/composables/auth'

export const login = async (username, password) => {
    try {
        const response = await api.post('/users/token', qs.stringify({ username, password }), {
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        });

        const { access_token } = response.data;
        if (!access_token) throw new Error("No token received");

        localStorage.setItem("token", access_token);
        localStorage.setItem("username", username);

        // const { successfulLogin } = useLogin();
        // successfulLogin(username);

        return true;
    } catch (error) {
        console.error("Login failed:", error);
        return false;
    }
}

export const getUser = async () => {
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
        const response = await api.patch(`/users/${username}`,{
            first_name,
            last_name,
            phone_number
        }, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error) {
        console.error("Token invalid or expired", error);
        return null;
    }
}

export const deleteUser = async (username) => {
    try {
        const response = await api.delete(`/users/${username}`, {username}, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error) {
        console.error("Token invalid or expired", error);
        return null;
    }
}

export const createUser = async (username, first_name, last_name, phone_number, password) => {
    try {
        const response = await api.post(`/users/`, {
            username,
            first_name,
            last_name,
            phone_number,
            password
        });
        return response.data;
    } catch (error) {
        console.error("Create Account issue", error);
        return null;
    }
}