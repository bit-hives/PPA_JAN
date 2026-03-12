import { createStore } from 'vuex'

export default createStore({
    state: {
        token: localStorage.getItem('token'),
        role: localStorage.getItem('role'),
        username: localStorage.getItem('username'),
    },
    mutations: {
        LOGIN(s, { token, role, username }) {
            s.token = token; s.role = role; s.username = username
            localStorage.setItem('token', token)
            localStorage.setItem('role', role)
            localStorage.setItem('username', username)
        },
        LOGOUT(s) {
            s.token = s.role = s.username = null
            localStorage.clear()
        }
    },
    getters: {
        isLoggedIn: s => !!s.token,
        userRole: s => s.role,
    }
})
