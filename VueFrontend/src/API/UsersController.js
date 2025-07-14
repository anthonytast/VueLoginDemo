/*
import usersData from "@/DB/LoginBackend"

let username = ""

// passing in strs
const login = (username, password) => {
    return ((username in usersData) && (usersData[username].password == password))
}

// passing in strs
export const isSuccessfulLoginAlert = (username, password) => {
    if (login(username, password)) window.alert("Login Success!")
    else window.alert("Login Failed :(")
}

export const loginPushToUserInfo = (router, username, password) => {
    if (login(username, password)) {
        router.push({path: '/user-info', query: {username: username, login: 'true'}})
    } else window.alert("Login Failed :(")
}

export const getUsersData = (username) => {
    //return userData[username] ? userData[usernane] : {}
    // if (usersData[username]) return usersData[username]
    // else return {}
    // else return 'No user data Available'
    return usersData[username]
}
// export default {getUsersData, isSuccessfulLoginAlert}

/*
CAN LATER ADD toRefs() on these methods
*/

import api from '../api.js';

const login = async (username, password) => {
    // return ((username in usersData) && (usersData[username].password == password))
    try {
        const response = api.get(`/users/login?username=${username}&password=${password}`)
        console.log("login response:", response.data["login"])
        console.log("login response status code:", response.status)
    } catch (error) {
        console.error("Login API Error")
        return
    }
    return response.data["login"]
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

export const loginPushToUserInfo = async (router, username, password) => {
    if (login(username, password)) {
        router.push({path: '/user-info', query: {username: username, login: 'true'}})
    } else window.alert("Login Failed :(")
}

// Needs to be async if making asynchronous api calls