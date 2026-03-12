<template>
  <div class="min-vh-100 bg-light d-flex flex-column">
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-4 py-3">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold text-primary fs-4" href="#">PlacementPortal</a>
        <div class="ms-auto d-flex gap-3">
          <router-link to="/register/student" class="btn btn-outline-primary rounded-pill px-4">Student Signup</router-link>
          <router-link to="/register/company" class="btn btn-outline-primary rounded-pill px-4">Company Signup</router-link>
        </div>
      </div>
    </nav>

    <div class="flex-grow-1 d-flex justify-content-center align-items-center py-5">
      <div class="card border-0 shadow-lg rounded-4" style="width: 100%; max-width: 450px; overflow: hidden;">
        <div class="card-header bg-white border-0 text-center pt-5 pb-2">
          <h3 class="fw-bold text-dark">Welcome Back</h3>
          <p class="text-muted mb-0">Login to continue your journey</p>
        </div>
        <div class="card-body p-5 pt-4">
          <form @submit.prevent="login">
            <div class="form-floating mb-4">
              <input v-model="form.username" type="text" class="form-control rounded-3 bg-light border-0" id="usernameInput" placeholder="Email or Username" required />
              <label for="usernameInput" class="text-muted">Email or Username</label>
            </div>

            <div class="form-floating mb-4">
              <input v-model="form.password" type="password" class="form-control rounded-3 bg-light border-0" id="passwordInput" placeholder="Password" required />
              <label for="passwordInput" class="text-muted">Password</label>
            </div>

            <button type="submit" class="btn btn-primary w-100 py-3 rounded-pill fw-bold shadow-sm" :disabled="loading" style="font-size: 1.1rem;">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ loading ? 'Authenticating...' : 'Log In' }}
            </button>
            
            <div v-if="error" class="alert alert-danger mt-4 text-center border-0 rounded-3 mb-0">{{ error }}</div>
          </form>
        </div>
        <div class="card-footer bg-light border-0 text-center py-4">
          <p class="mb-0 text-muted">Don't have an account? 
            <router-link to="/register/student" class="text-primary fw-semibold text-decoration-none ms-1">Register Here</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../axios'
export default {
  data() { return { form: { username: '', password: '' }, error: null, loading: false } },
  methods: {
    async login() {
      this.loading = true; this.error = null
      try {
        const res = await api.post('/auth/login', this.form)
        this.$store.commit('LOGIN', res.data)
        const routes = { admin: '/admin/dashboard', student: '/student/dashboard', company: '/company/dashboard' }
        this.$router.push(routes[res.data.role])
      } catch(e) { this.error = e.response?.data?.error || 'Login failed Check Credentials' }
      finally { this.loading = false }
    }
  }
}
</script>

<style scoped>
.form-control:focus {
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
  background-color: #fff !important;
}
</style>
