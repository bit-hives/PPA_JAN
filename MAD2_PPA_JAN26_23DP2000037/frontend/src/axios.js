import axios from 'axios'
import store from './store'
import router from './router'

const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use(c => {
    if (store.state.token) c.headers.Authorization = `Bearer ${store.state.token}`
    return c
})
api.interceptors.response.use(r => r, e => {
    if (e.response?.status === 401) { store.commit('LOGOUT'); router.push('/login') }
    return Promise.reject(e)
})
export default api
