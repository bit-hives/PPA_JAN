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
            <router-link to="/student/dashboard" class="nav-link rounded-3 text-white fw-semibold bg-primary"><i class="bi bi-grid-fill me-2"></i> Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/student/profile" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-person-badge-fill me-2"></i> My Profile</router-link>
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
        <h5 class="mb-0 fw-bold text-dark">Welcome, {{ $store.state.username }}!</h5>
        <div class="ms-auto d-flex align-items-center gap-3">
          <div class="input-group" style="width: 250px;">
            <span class="input-group-text bg-light border-0"><i class="bi bi-search"></i></span>
            <input v-model="filters.branch" @keyup="loadDrives" type="text" class="form-control bg-light border-0" placeholder="Filter by Job Title...">
          </div>
          <div class="dropdown">
            <button class="btn btn-light rounded-circle p-2 position-relative" @click="toggleNotifications">
              <i class="bi bi-bell-fill"></i>
              <span v-if="notifications.length" class="position-absolute top-0 start-100 translate-middle p-1 bg-danger rounded-circle"></span>
            </button>
            <div v-if="showNotifications" class="dropdown-menu dropdown-menu-end show shadow" style="min-width: 320px;">
              <div v-if="notifications.length === 0" class="px-3 py-2 text-muted">No notifications</div>
              <div v-for="(n, i) in notifications" :key="i" class="px-3 py-2 border-bottom">
                <div class="fw-bold">{{ n.message }}</div>
                <div class="small text-muted">{{ n.date }}</div>
              </div>
            </div>
          </div>
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border ms-2">
            <div class="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">
              <i class="bi bi-person-fill"></i>
            </div>
            <span class="fw-semibold small">{{ $store.state.username }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto">
        
        <div class="row g-4 mb-4">
          <div class="col-12 mb-3 text-end">
            <button @click="exportCSV" class="btn btn-outline-primary rounded-pill fw-bold shadow-sm">
              <i class="bi bi-file-earmark-spreadsheet me-2"></i> Export My Applications (CSV)
            </button>
          </div>
          <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column">
                <div class="text-muted fw-semibold mb-2">My Applications</div>
                <div class="d-flex justify-content-between align-items-center mt-auto">
                  <h2 class="fw-bold mb-0 text-primary">{{ stats.applications || 0 }}</h2>
                  <div class="bg-primary bg-opacity-10 text-primary rounded-circle p-3"><i class="bi bi-file-earmark-check fs-4"></i></div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column">
                <div class="text-muted fw-semibold mb-2">Shortlisted For</div>
                <div class="d-flex justify-content-between align-items-center mt-auto">
                  <h2 class="fw-bold mb-0 text-warning">{{ stats.shortlisted || 0 }}</h2>
                  <div class="bg-warning bg-opacity-10 text-warning rounded-circle p-3"><i class="bi bi-star-fill fs-4"></i></div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column">
                <div class="text-muted fw-semibold mb-2">Offers Selected</div>
                <div class="d-flex justify-content-between align-items-center mt-auto">
                  <h2 class="fw-bold mb-0 text-success">{{ stats.selected || 0 }}</h2>
                  <div class="bg-success bg-opacity-10 text-success rounded-circle p-3"><i class="bi bi-award fs-4"></i></div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-4 bg-primary text-white h-100">
              <div class="card-body p-4 d-flex flex-column justify-content-center text-center">
                <h5 class="fw-bold mb-2">Profile Completeness</h5>
                <h2 class="fw-bold mb-0">100%</h2>
                <router-link to="/student/profile" class="btn btn-sm btn-light text-primary rounded-pill fw-bold mt-2 mx-auto px-3">Update Resume</router-link>
              </div>
            </div>
          </div>
        </div>

        
        <h5 class="fw-bold text-dark mb-4">Latest Opportunities <span class="badge bg-primary ms-2">{{ drives.length }}</span></h5>
        
        <div class="row g-4">
          <div v-for="d in drives" :key="d.id" class="col-md-6 col-lg-4">
            <div class="card border-0 shadow-sm rounded-4 h-100 position-relative hover-lift">
              <div class="card-body p-4">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <div class="bg-primary bg-opacity-10 text-primary rounded-3 d-flex justify-content-center align-items-center fw-bold fs-4" style="width: 50px; height: 50px;">
                    {{ d.company_name.charAt(0).toUpperCase() }}
                  </div>
                  <span class="badge bg-light text-dark border px-2 py-1"><i class="bi bi-calendar-event me-1"></i> Due: {{ d.deadline ? d.deadline.split(' ')[0] : 'Open' }}</span>
                </div>
                
                <h5 class="fw-bold text-dark mb-1">{{ d.job_title }}</h5>
                <p class="text-muted fw-semibold mb-3">{{ d.company_name }}</p>
                
                <div class="d-flex flex-wrap gap-2 mb-4">
                  <span v-if="d.eligibility_branch" class="badge bg-light text-dark border px-2"><i class="bi bi-mortarboard text-muted me-1"></i> {{ d.eligibility_branch }}</span>
                  <span v-if="d.eligibility_gpa" class="badge bg-light text-dark border px-2"><i class="bi bi-clipboard-data text-muted me-1"></i> Target GPA: {{ d.eligibility_gpa }}</span>
                  <span v-if="d.eligibility_year" class="badge bg-light text-dark border px-2"><i class="bi bi-clock-history text-muted me-1"></i> {{ d.eligibility_year }} Batch</span>
                </div>
                
                <div class="mt-auto border-top pt-3 d-flex justify-content-between align-items-center">
                  <span class="text-success small fw-bold"><i class="bi bi-check-circle-fill me-1"></i> Actively Recruiting</span>
                  <button @click="apply(d.id)" :disabled="d.already_applied" class="btn rounded-pill px-4 fw-bold shadow-sm" :class="d.already_applied ? 'btn-secondary' : 'btn-primary'" style="font-size: 0.9rem;">
                    {{ d.already_applied ? 'Already Applied' : 'Apply Now' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="drives.length === 0" class="col-12 text-center py-5">
            <div class="bg-white rounded-circle d-inline-flex justify-content-center align-items-center shadow-sm mb-3" style="width: 80px; height: 80px;">
              <i class="bi bi-briefcase text-muted fs-1"></i>
            </div>
            <h4 class="fw-bold text-dark">No Active Drives Match Your Profile</h4>
            <p class="text-muted">Check back later or adjust your profile filters.</p>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import api from '../axios'
export default {
  data() { return { stats: {}, drives: [], filters: { branch:'', min_gpa:null, year:null }, notifications: [], showNotifications: false } },
  async mounted() {
    await this.loadDashboard()
  },
  activated() {
    this.loadDashboard()
  },
  methods: {
    async loadDashboard() {
      try {
        this.stats = (await api.get('/student/stats')).data
        this.notifications = (await api.get('/student/notifications')).data
        await this.loadDrives()
      } catch(e) {
        console.error("Failed to load student dashboard:", e)
      }
    },
    async loadDrives() {
      const p = new URLSearchParams()
      if(this.filters.branch) p.append('branch', this.filters.branch)
      this.drives = (await api.get('/student/drives?'+p.toString())).data
    },
    async apply(id) {
      if(confirm('Submit application?')) {
        try {
          const res = await api.post(`/student/apply/${id}`)
          alert(res.data.message)
          this.stats = (await api.get('/student/stats')).data
          this.loadDrives()  
        } catch(e) { alert(e.response?.data?.error || 'Failed to apply') }
      }
    },
    async exportCSV() {
      try {
        const res = await api.post('/jobs/export-csv')
        alert(res.data.message || 'CSV export started. You will receive it by email.')
      } catch(e) {
        alert(e.response?.data?.error || 'Failed to start CSV export')
      }
    },
    toggleNotifications() {
      this.showNotifications = !this.showNotifications
    }
  }
}
</script>

<style scoped>
.font-sans { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
.nav-link:not(.bg-primary):hover { background-color: #f8f9fa; }
.hover-lift { transition: transform 0.2s ease, box-shadow 0.2s ease; }
.hover-lift:hover { transform: translateY(-5px); box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important; }
</style>
