<template>
  <div class="min-vh-100 bg-light d-flex flex-column">
    
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-4 py-3">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold text-success fs-4" href="#">PlacementPortal <span class="text-dark">Employers</span></a>
        <div class="ms-auto d-flex align-items-center gap-3">
          <span class="text-muted">Already registered?</span>
          <router-link to="/login" class="btn btn-outline-success rounded-pill px-4">Log In</router-link>
        </div>
      </div>
    </nav>

    
    <div class="flex-grow-1 d-flex justify-content-center align-items-center py-5">
      <div class="card border-0 shadow flex-row rounded-4 overflow-hidden" style="width: 100%; max-width: 900px;">
        
        
        <div class="bg-success text-white p-5 d-none d-md-flex flex-column justify-content-center" style="width: 40%;">
          <h2 class="fw-bold mb-4">Hire Top Talent Today</h2>
          <p class="fs-5 mb-4 opacity-75">Connect with brilliant minds from top colleges and build your dream team.</p>
          <ul class="list-unstyled opacity-75">
            <li class="mb-3"><i class="bi bi-briefcase-fill me-2"></i> Post seamless placement drives</li>
            <li class="mb-3"><i class="bi bi-people-fill me-2"></i> Manage applications effectively</li>
            <li><i class="bi bi-graph-up-arrow me-2"></i> Access detailed recruitment analytics</li>
          </ul>
        </div>

        
        <div class="p-5" style="width: 60%; background: #fff;">
          <h3 class="fw-bold text-dark mb-4">Company Registration</h3>
          <form @submit.prevent="register">
            <div class="row g-3">
              <div class="col-md-6 form-floating">
                <input v-model="form.name" class="form-control bg-light border-0" id="nameInp" placeholder="Company Name" required />
                <label for="nameInp" class="ms-2 text-muted">Company Name</label>
              </div>
              <div class="col-md-6 form-floating">
                <input v-model="form.username" class="form-control bg-light border-0" id="usrInp" placeholder="Company ID (Username)" required />
                <label for="usrInp" class="ms-2 text-muted">Company ID (Username)</label>
              </div>
              <div class="col-md-6 form-floating">
                <input v-model="form.email" type="email" class="form-control bg-light border-0" id="emInp" placeholder="Work Email" required />
                <label for="emInp" class="ms-2 text-muted">Work Email Address</label>
              </div>
              <div class="col-md-6 form-floating">
                <input v-model="form.password" type="password" class="form-control bg-light border-0" id="pwInp" placeholder="Password" required />
                <label for="pwInp" class="ms-2 text-muted">Password</label>
              </div>
              
              <div class="col-md-6 form-floating">
                <input v-model="form.sector" class="form-control bg-light border-0" id="secInp" placeholder="Industry/Sector" required />
                <label for="secInp" class="ms-2 text-muted">Industry / Sector</label>
              </div>
              <div class="col-md-6 form-floating">
                <input v-model="form.established_in" type="number" class="form-control bg-light border-0" id="estInp" placeholder="Established Year" required />
                <label for="estInp" class="ms-2 text-muted">Established Year</label>
              </div>
              
              <div class="col-12 form-floating">
                <input v-model="form.website" class="form-control bg-light border-0" id="webInp" placeholder="Website URL" required />
                <label for="webInp" class="ms-2 text-muted">Company Website URL</label>
              </div>

              <div class="col-12 form-floating">
                <input v-model="form.hr_contact" class="form-control bg-light border-0" id="hrInp" placeholder="HR Contact Name & Phone" required />
                <label for="hrInp" class="ms-2 text-muted">HR Contact (Name & Phone)</label>
              </div>
            </div>

            <button type="submit" class="btn btn-success w-100 py-3 rounded-pill fw-bold shadow-sm mt-4 text-white" :disabled="loading" style="font-size: 1.1rem;">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ loading ? 'Submitting...' : 'Register as Employer' }}
            </button>
            <div class="text-center mt-3">
              <router-link to="/register/student" class="text-secondary small fw-semibold text-decoration-none">Looking for a job? Register as Student</router-link>
            </div>
            
            <div v-if="msg" class="alert mt-4 text-center border-0 rounded-3 mb-0" :class="error ? 'alert-danger' : 'alert-success'">{{ msg }}</div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../axios'
export default {
  data() { return { form: { name:'', username:'', email:'', password:'', hr_contact:'', website:'', sector:'', established_in:'' }, msg: null, error: false, loading: false } },
  methods: {
    async register() {
      this.loading = true; this.msg = null; this.error = false
      try {
        const res = await api.post('/auth/register/company', this.form)
        this.msg = res.data.message
        setTimeout(() => this.$router.push('/login'), 2000)
      } catch(e) { this.error = true; this.msg = e.response?.data?.error || 'Registration failed' }
      finally { this.loading = false }
    }
  }
}
</script>

<style scoped>
.form-control:focus {
  box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.15);
  background-color: #fff !important;
}
</style>
