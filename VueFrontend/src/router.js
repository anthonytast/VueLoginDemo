import { createWebHistory, createRouter } from 'vue-router'

import Login  from './pages/Login.vue';
import UserInfo from './pages/UserInfo.vue';
import CreateUser from './pages/CreateUser.vue';
import { getUser } from '@/controllers/usersController'
import { useLogin } from '@/composables/auth'

const routes = [
  { path: '/', component: Login, meta: { requiresAuth: false }  },
  { path: '/user-info', component: UserInfo, meta: { requiresAuth: true } },
  { path: '/sign-up', component: CreateUser, meta: { requiresAuth: false } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// const { successfulLogin } = useLogin()

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (!requiresAuth) return next()

  const token = localStorage.getItem('token')
  if (!token) {
    return next('/')
  }

  const user = await getUser() // getUser verifies token
  if (!user) {
    localStorage.clear()
    return next('/')
  }

  // successfulLogin(user.username)
  return next()
})

export default router