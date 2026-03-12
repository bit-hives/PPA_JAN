import { createRouter, createWebHistory } from 'vue-router'
import store from './store'

const routes = [
    { path: '/', component: () => import('./views/Landing.vue') },
    { path: '/login', component: () => import('./views/Login.vue') },
    { path: '/register/student', component: () => import('./views/StudentRegister.vue') },
    { path: '/register/company', component: () => import('./views/CompanyRegister.vue') },
    { path: '/admin/dashboard', component: () => import('./views/AdminDashboard.vue'), meta: { role: 'admin' } },
    { path: '/admin/students', component: () => import('./views/AdminStudents.vue'), meta: { role: 'admin' } },
    { path: '/admin/companies', component: () => import('./views/AdminCompanies.vue'), meta: { role: 'admin' } },
    { path: '/admin/drives', component: () => import('./views/AdminDrives.vue'), meta: { role: 'admin' } },
    { path: '/student/dashboard', component: () => import('./views/StudentDashboard.vue'), meta: { role: 'student' } },
    { path: '/student/profile', component: () => import('./views/StudentProfile.vue'), meta: { role: 'student' } },
    { path: '/student/exams', component: () => import('./views/StudentExams.vue'), meta: { role: 'student' } },
    { path: '/student/placement', component: () => import('./views/StudentPlacement.vue'), meta: { role: 'student' } },
    { path: '/student/notifications', component: () => import('./views/StudentNotifications.vue'), meta: { role: 'student' } },
    { path: '/student/interviews', component: () => import('./views/StudentInterviews.vue'), meta: { role: 'student' } },
    { path: '/company/dashboard', component: () => import('./views/CompanyDashboard.vue'), meta: { role: 'company' } },
    { path: '/company/drives', component: () => import('./views/CompanyDrives.vue'), meta: { role: 'company' } },
    { path: '/company/exams', component: () => import('./views/CompanyExams.vue'), meta: { role: 'company' } },
    { path: '/company/history', component: () => import('./views/CompanyHistory.vue'), meta: { role: 'company' } },
    { path: '/company/interviews', component: () => import('./views/CompanyInterviews.vue'), meta: { role: 'company' } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
    if (!to.meta.role) return next()
    if (!store.getters.isLoggedIn) return next('/login')
    if (store.state.role !== to.meta.role) return next('/login')
    next()
})

export default router
