<template>
  <div class="d-flex min-vh-100 bg-light font-sans">
    
    <div class="bg-white shadow-sm d-flex flex-column" style="width: 250px;">
      <div class="p-4 border-bottom text-center">
        <h4 class="fw-bold text-primary mb-0">PlacementPortal</h4>
        <span class="badge bg-primary mt-2">Student Portal</span>
      </div>
      <div class="p-3 flex-grow-1">
        <ul class="nav flex-column gap-2">
          <li class="nav-item">
            <router-link to="/student/dashboard" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-grid-fill me-2"></i> Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/student/profile" class="nav-link rounded-3 text-white fw-semibold bg-primary"><i class="bi bi-person-badge-fill me-2"></i> My Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/student/notifications" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-bell-fill me-2"></i> Alerts & Off-Campus</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/student/exams" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-pencil-square me-2"></i> Online Exams</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/student/placement" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-award-fill me-2"></i> Application Status</router-link>
          </li>
        </ul>
      </div>
      <div class="p-4 border-top">
        <button @click="$store.commit('LOGOUT'); $router.push('/login')" class="btn btn-light w-100 text-start fw-semibold text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</button>
      </div>
    </div>

    
    <div class="flex-grow-1 d-flex flex-column">
      
      <nav class="navbar navbar-light bg-white shadow-sm px-4 py-3">
        <h5 class="mb-0 fw-bold text-dark">My Profile</h5>
        <div class="ms-auto d-flex align-items-center gap-3">
          <button class="btn btn-light rounded-circle p-2 position-relative"><i class="bi bi-bell-fill"></i></button>
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border ms-2">
            <div class="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">
              <i class="bi bi-person-fill"></i>
            </div>
            <span class="fw-semibold small">{{ form.name || $store.state.username }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto d-flex justify-content-center">
        <div class="card border-0 shadow-sm rounded-4 w-100" style="max-width: 800px;">
          <div class="card-header bg-white border-bottom-0 pt-4 px-4 pb-0">
            <h5 class="fw-bold"><i class="bi bi-person-lines-fill text-primary me-2"></i> Personal Details</h5>
            <p class="text-muted small">Update your academic details and resume to stay eligible for upcoming drives.</p>
          </div>
          <div class="card-body p-4">
            <div v-if="msg" class="alert alert-success border-0 shadow-sm rounded-3 py-2 mb-4"><i class="bi bi-check-circle-fill me-2"></i> {{ msg }}</div>
            
            <form @submit.prevent="update">
              <div class="row g-4">
                <div class="col-md-6 form-floating">
                  <input v-model="form.name" class="form-control bg-light border-0" id="fn" />
                  <label for="fn" class="ms-2">Full Name</label>
                </div>
                <div class="col-md-6 form-floating">
                  <input v-model="form.dob" type="date" class="form-control bg-light border-0" id="dob" />
                  <label for="dob" class="ms-2">Date of Birth</label>
                </div>
                <div class="col-md-6 form-floating">
                  <input v-model="form.email" type="email" class="form-control bg-light border-0" id="em" readonly disabled />
                  <label for="em" class="ms-2">Email Address (Readonly)</label>
                </div>
                <div class="col-md-6 form-floating">
                  <input v-model="form.address" class="form-control bg-light border-0" id="loc" />
                  <label for="loc" class="ms-2">Location</label>
                </div>

                <div class="col-12 mt-4"><h6 class="fw-bold border-bottom pb-2">Academic Information</h6></div>

                <div class="col-md-6 form-floating">
                  <input v-model="form.college" class="form-control bg-light border-0" id="col" />
                  <label for="col" class="ms-2">College Name</label>
                </div>
                <div class="col-md-6 form-floating">
                  <input v-model="form.branch" class="form-control bg-light border-0" id="br" />
                  <label for="br" class="ms-2">Branch / Major</label>
                </div>
                <div class="col-md-6 form-floating">
                  <input v-model.number="form.gpa" type="number" step="0.1" class="form-control bg-light border-0" id="gpa" />
                  <label for="gpa" class="ms-2">CGPA</label>
                </div>
                <div class="col-md-6 form-floating">
                  <input v-model.number="form.year" type="number" class="form-control bg-light border-0" id="yr" />
                  <label for="yr" class="ms-2">Passing Year</label>
                </div>
              </div>

              <div class="mt-4 pt-4 border-top text-end">
                <button type="submit" class="btn btn-primary rounded-pill px-5 fw-bold shadow-sm">Save Profile Updates</button>
              </div>
            </form>

            
            <div class="mt-5 bg-light p-4 rounded-4 border">
              <h6 class="fw-bold mb-3"><i class="bi bi-file-earmark-pdf text-danger me-2"></i> Update Resume</h6>
              <div class="d-flex align-items-center gap-3">
                <input type="file" @change="onFile" class="form-control bg-white border-0 py-2 w-auto flex-grow-1" accept=".pdf,.doc,.docx" />
                <button @click="uploadResume" class="btn btn-dark rounded-pill px-4 fw-bold">Upload</button>
              </div>
              <div v-if="resumeMsg" class="text-success small mt-2 fw-semibold"><i class="bi bi-check-lg"></i> {{ resumeMsg }}</div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../axios'
export default {
  data() { return { form: {}, file: null, msg: null, resumeMsg: null } },
  async mounted() {
    const data = (await api.get('/student/profile')).data
    this.form = {
      name: data.name || '',
      dob: data.dob || '',
      email: data.email || '',
      address: data.address || '',
      college: data.college || '',
      branch: data.branch || '',
      gpa: data.gpa || '',
      year: data.year || '',
      resume_path: data.resume_path || ''
    }
  },
  methods: {
    async update() {
      await api.put('/student/profile', this.form)
      this.msg = 'Profile updated securely'
      setTimeout(() => this.msg = null, 3000)
    },
    onFile(e) { this.file = e.target.files[0] },
    async uploadResume() {
      if(!this.file) return
      const fd = new FormData()
      fd.append('resume', this.file)
      await api.post('/student/resume', fd)
      this.resumeMsg = 'Resume saved securely'
      setTimeout(() => this.resumeMsg = null, 3000)
    }
  }
}
</script>

<style scoped>
.font-sans { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
.nav-link:not(.bg-primary):hover { background-color: #f8f9fa; }
</style>
