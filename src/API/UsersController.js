import usersData from "@/DB/LoginBackend"

// passing in refs
const login = (username, password) => {
    return ((username.value in usersData) && (usersData[username.value].password == password.value))
}

// passing in refs
const isSuccessfulLoginAlert = (username, password) => {
    if (login(username, password)) window.alert("Login Success!")
    else window.alert("Login Failed :(")
}

export default isSuccessfulLoginAlert;