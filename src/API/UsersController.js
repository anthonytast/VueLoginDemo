import usersData from "@/DB/LoginBackend"

let username = ""
let isLoggedIn = false

// passing in strs
const login = ({username, password}) => {
    if ((username in usersData) && (usersData[username].password == password)) {
        isLoggedIn = true
    }
    return isLoggedIn
}

// passing in strs
// export const isSuccessfulLoginAlert = (username, password) => {
//     if (login(username, password)) window.alert("Login Success!")
//     else window.alert("Login Failed :(")
// }

export const loginPushToUserInfo = ({router, username, password}) => {
    if (login({username:username, password:password})) {
        router.push({path: '/user-info', query: {username: username, login: isLoggedIn}})
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