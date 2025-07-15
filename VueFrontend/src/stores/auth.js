import { defineStore } from 'pinia'

export const useLoginStore = defineStore('auth', {
  state: () => ({
    username: null,
    login: false
  }),
  actions: {
    successfulLogin(username) {
      this.username = username
      this.login = true
    },
    logoutUser() {
        this.username = null,
        this.login = false
    }
  },
})