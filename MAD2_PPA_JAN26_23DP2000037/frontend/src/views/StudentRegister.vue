<template>
  <div class="min-vh-100 bg-light d-flex flex-column">
    
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-4 py-3">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold text-primary fs-4" href="#">PlacementPortal</a>
        <div class="ms-auto d-flex align-items-center gap-3">
          <span class="text-muted">Already have an account?</span>
          <router-link to="/login" class="btn btn-primary rounded-pill px-4">Log In</router-link>
        </div>
      </div>
    </nav>

    
    <div class="flex-grow-1 d-flex justify-content-center align-items-center py-5">
      <div class="card border-0 shadow flex-row rounded-4 overflow-hidden" style="width: 100%; max-width: 900px;">
        
        
        <div class="bg-primary text-white p-5 d-none d-md-flex flex-column justify-content-center" style="width: 40%;">
          <h2 class="fw-bold mb-4">Start Your Career Journey</h2>
          <p class="fs-5 mb-4 opacity-75">Join thousands of students getting placed in top companies every month.</p>
          <ul class="list-unstyled opacity-75">
            <li class="mb-3"><i class="bi bi-check-circle-fill me-2"></i> Access to premium drives</li>
            <li class="mb-3"><i class="bi bi-check-circle-fill me-2"></i> Track applications easily</li>
            <li><i class="bi bi-check-circle-fill me-2"></i> Get instant notifications</li>
          </ul>
        </div>

        
        <div class="p-5" style="width: 60%; background: #fff;">
          <h3 class="fw-bold text-dark mb-4">Student Registration</h3>
          <form @submit.prevent="register">
            <div class="row g-3">
              <div class="col-md-6 form-floating">
                <input v-model="form.name" class="form-control bg-light border-0" id="nameInp" placeholder="Full Name" required />
                <label for="nameInp" class="ms-2 text-muted">Full Name</label>
              </div>
              <div class="col-md-6 form-floating">
                <input v-model="form.username" class="form-control bg-light border-0" id="usrInp" placeholder="Username" required />
                <label for="usrInp" class="ms-2 text-muted">Username</label>
              </div>
              <div class="col-md-6 form-floating">
                <input v-model="form.email" type="email" class="form-control bg-light border-0" id="emInp" placeholder="Email" required />
                <label for="emInp" class="ms-2 text-muted">Email Address</label>
              </div>
              <div class="col-md-6 form-floating">
                <input v-model="form.password" type="password" class="form-control bg-light border-0" id="pwInp" placeholder="Password" required />
                <label for="pwInp" class="ms-2 text-muted">Password</label>
              </div>
              
              <div class="col-md-6 form-floating">
                <input v-model="form.college" class="form-control bg-light border-0" id="clgInp" placeholder="College Name" required />
                <label for="clgInp" class="ms-2 text-muted">College Name</label>
              </div>
              <div class="col-md-6 form-floating">
                <input v-model="form.branch" class="form-control bg-light border-0" id="brInp" placeholder="Branch" required />
                <label for="brInp" class="ms-2 text-muted">Branch / Specialization</label>
              </div>
              
              <div class="col-md-4 form-floating">
                <input v-model.number="form.gpa" type="number" step="0.1" class="form-control bg-light border-0" id="gpaInp" placeholder="GPA" required />
                <label for="gpaInp" class="ms-2 text-muted">GPA (out of 10.0)</label>
              </div>
              <div class="col-md-4 form-floating">
                <input v-model.number="form.year" type="number" class="form-control bg-light border-0" id="yrInp" placeholder="Passing Year" required />
                <label for="yrInp" class="ms-2 text-muted">Passing Year</label>
              </div>
              <div class="col-md-4 form-floating">
                <input v-model="form.dob" type="date" class="form-control bg-light border-0" id="dobInp" required />
                <label for="dobInp" class="ms-2 text-muted">Date of Birth</label>
              </div>
              
              <div class="col-12 form-floating">
                <input v-model="form.address" class="form-control bg-light border-0" id="addInp" placeholder="City, State" />
                <label for="addInp" class="ms-2 text-muted">Location (City, State)</label>
              </div>

              <div class="col-12 mt-3">
                <label class="form-label text-muted small fw-bold mb-1">Upload Resume (PDF/DOC)</label>
                <input type="file" @change="onFile" class="form-control bg-light border-0 py-2" accept=".pdf,.doc,.docx" required />
              </div>
            </div>

            <button type="submit" class="btn btn-primary w-100 py-3 rounded-pill fw-bold shadow-sm mt-4 text-white" :disabled="loading" style="font-size: 1.1rem;">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ loading ? 'Creating Account...' : 'Register as Student' }}
            </button>
            <div class="text-center mt-3">
              <router-link to="/register/company" class="text-secondary small fw-semibold text-decoration-none">Looking to hire? Register as Company</router-link>
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
  data() { return { form: { name:'', username:'', email:'', password:'', dob:'', college:'', branch:'', gpa:null, year:null, address:'' }, file: null, msg: null, error: false, loading: false } },
  methods: {
    onFile(e) { this.file = e.target.files[0] },
    async register() {
      this.loading = true; this.msg = null; this.error = false
      try {
        const fd = new FormData()
        for (const k in this.form) { if (this.form[k] !== null) fd.append(k, this.form[k]) }
        if (this.file) fd.append('resume', this.file)
        
        const res = await api.post('/auth/register/student', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
        this.msg = res.data.message
        setTimeout(() => this.$router.push('/login'), 1500)
      } catch(e) { this.error = true; this.msg = e.response?.data?.error || 'Registration failed' }
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
