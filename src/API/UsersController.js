import usersData from "@/DB/LoginBackend"

let username = ""

// passing in refs
const login = (username, password) => {
    return ((username in usersData) && (usersData[username].password == password))
}

// passing in refs
export const isSuccessfulLoginAlert = (username, password) => {
    if (login(username, password)) window.alert("Login Success!")
    else window.alert("Login Failed :(")
}

//toRefs()

export const getUsersData = (username) => {
    //return userData[username] ? userData[usernane] : {}
    if (usersData[username]) return usersData[username]
    else return {}
    // else return 'No user data Available'
}
// export default {getUsersData, isSuccessfulLoginAlert}