<template>
  <div class="d-flex min-vh-100 bg-light font-sans">
    
    <div class="bg-white shadow-sm d-flex flex-column" style="width: 250px;">
      <div class="p-4 border-bottom text-center">
        <h4 class="fw-bold text-success mb-0">PlacementPortal</h4>
        <span class="badge bg-success mt-2">Employer Panel</span>
      </div>
      <div class="p-3 flex-grow-1">
        <ul class="nav flex-column gap-2">
          <li class="nav-item">
            <router-link to="/company/dashboard" class="nav-link rounded-3 text-white fw-semibold bg-success"><i class="bi bi-grid-fill me-2"></i> Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/company/drives" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-briefcase-fill me-2"></i> My Drives</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/company/exams" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-file-earmark-text-fill me-2"></i> Exams</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/company/history" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-clock-history me-2"></i> Placement History</router-link>
          </li>
        </ul>
      </div>
      <div class="p-4 border-top">
        <button @click="$store.commit('LOGOUT'); $router.push('/login')" class="btn btn-light w-100 text-start fw-semibold text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</button>
      </div>
    </div>

    
    <div class="flex-grow-1 d-flex flex-column">
      
      <nav class="navbar navbar-light bg-white shadow-sm px-4 py-3">
        <h5 class="mb-0 fw-bold text-dark">Welcome back, {{ $store.state.username }}!</h5>
        <div class="ms-auto d-flex align-items-center gap-3">
          <div class="dropdown">
            <button class="btn btn-light rounded-circle p-2 position-relative" @click="toggleNotifications">
              <i class="bi bi-bell-fill"></i>
              <span v-if="notifications.length" class="position-absolute top-0 start-100 translate-middle p-1 bg-danger rounded-circle"></span>
            </button>
            <div v-if="showNotifications" class="dropdown-menu dropdown-menu-end show shadow" style="min-width: 320px;">
              <div v-if="notifications.length === 0" class="px-3 py-2 text-muted">No notifications</div>
              <div v-for="(n, i) in notifications" :key="i" class="px-3 py-2 border-bottom">
                <div class="fw-bold small">{{ n.message }}</div>
                <div class="small text-muted">{{ n.date }}</div>
              </div>
            </div>
          </div>
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border cursor-pointer hover-lift" @click="showCompanyModal = true" style="cursor: pointer;">
            <div class="bg-success text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">{{ (profile.name || $store.state.username).charAt(0).toUpperCase() }}</div>
            <span class="fw-semibold small">{{ profile.name || $store.state.username }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto">
        
        <div class="row g-4 mb-4">
          <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column">
                <div class="text-muted fw-semibold mb-2">Total Drives Posted</div>
                <div class="d-flex justify-content-between align-items-center mt-auto">
                  <h2 class="fw-bold mb-0 text-primary">{{ stats.drives || 0 }}</h2>
                  <div class="bg-primary bg-opacity-10 text-primary rounded-circle p-3"><i class="bi bi-briefcase fs-4"></i></div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column">
                <div class="text-muted fw-semibold mb-2">Total Applications Received</div>
                <div class="d-flex justify-content-between align-items-center mt-auto">
                  <h2 class="fw-bold mb-0 text-success">{{ stats.applicants || 0 }}</h2>
                  <div class="bg-success bg-opacity-10 text-success rounded-circle p-3"><i class="bi bi-people fs-4"></i></div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column">
                <div class="text-muted fw-semibold mb-2">Candidates Selected</div>
                <div class="d-flex justify-content-between align-items-center mt-auto">
                  <h2 class="fw-bold mb-0 text-info">{{ stats.selected || 0 }}</h2>
                  <div class="bg-info bg-opacity-10 text-info rounded-circle p-3"><i class="bi bi-check-circle fs-4"></i></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        
        <div class="card border-0 shadow-sm rounded-4 mb-4">
          <div class="card-body p-4">
            <h5 class="fw-bold text-dark mb-4">Quick Actions</h5>
            <div class="d-flex gap-3">
              <router-link to="/company/drives" class="btn btn-success fw-bold px-4 rounded-pill shadow-sm"><i class="bi bi-plus-circle me-2"></i> Post New Drive</router-link>
              <router-link to="/company/history" class="btn btn-outline-success fw-bold px-4 rounded-pill shadow-sm"><i class="bi bi-clock-history me-2"></i> View Past Hires</router-link>
            </div>
          </div>
        </div>

        
        <div class="card border-0 shadow-sm rounded-4">
          <div class="card-body p-4">
            <h5 class="fw-bold text-dark mb-4">Company Profile Details</h5>
            <div class="row g-4">
              <div class="col-md-6">
                <p class="mb-1 text-muted small fw-semibold">Company Name</p>
                <div class="fw-bold">{{ profile.name }}</div>
              </div>
              <div class="col-md-6">
                <p class="mb-1 text-muted small fw-semibold">Sector / Industry</p>
                <div class="fw-bold">{{ profile.sector }}</div>
              </div>
              <div class="col-md-6">
                <p class="mb-1 text-muted small fw-semibold">HR Contact</p>
                <div class="fw-bold">{{ profile.hr_contact }}</div>
              </div>
              <div class="col-md-6">
                <p class="mb-1 text-muted small fw-semibold">Website</p>
                <div class="fw-bold"><a :href="profile.website" target="_blank" class="text-decoration-none">{{ profile.website }}</a></div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    
    <div v-if="showCompanyModal" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-success text-white border-0">
            <h5 class="modal-title fw-bold">Company Profile</h5>
            <button type="button" class="btn-close btn-close-white" @click="showCompanyModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <div class="text-center mb-4">
              <div class="bg-success text-white rounded-circle d-flex justify-content-center align-items-center fw-bold mx-auto mb-3" style="width: 80px; height: 80px; font-size: 32px;">{{ (profile.name || $store.state.username).charAt(0).toUpperCase() }}</div>
              <h5 class="fw-bold text-dark">{{ profile.name }}</h5>
              <p class="text-muted">Employer Account</p>
            </div>
            <div class="row g-3">
              <div class="col-12">
                <label class="form-label text-muted fw-semibold small">Company Name</label>
                <div class="p-3 bg-light rounded-2">{{ profile.name }}</div>
              </div>
              <div class="col-12">
                <label class="form-label text-muted fw-semibold small">Email</label>
                <div class="p-3 bg-light rounded-2">{{ profile.email }}</div>
              </div>
              <div class="col-12">
                <label class="form-label text-muted fw-semibold small">HR Contact</label>
                <div class="p-3 bg-light rounded-2">{{ profile.hr_contact || 'N/A' }}</div>
              </div>
              <div class="col-12">
                <label class="form-label text-muted fw-semibold small">Sector / Industry</label>
                <div class="p-3 bg-light rounded-2">{{ profile.sector || 'N/A' }}</div>
              </div>
              <div class="col-12">
                <label class="form-label text-muted fw-semibold small">Website</label>
                <div class="p-3 bg-light rounded-2">
                  <a v-if="profile.website" :href="profile.website" target="_blank" class="text-decoration-none text-success fw-semibold">{{ profile.website }}</a>
                  <span v-else class="text-muted">N/A</span>
                </div>
              </div>
              <div class="col-12">
                <label class="form-label text-muted fw-semibold small">Account Status</label>
                <div class="p-3 bg-light rounded-2">
                  <span class="badge" :class="profile.approval_status === 'approved' ? 'bg-success' : profile.approval_status === 'pending' ? 'bg-warning' : 'bg-danger'">
                    {{ profile.approval_status || 'Unknown' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer border-top bg-light">
            <button type="button" class="btn btn-success rounded-pill fw-semibold" @click="showCompanyModal = false">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../axios'
export default {
  data() { return { stats: {}, profile: {}, showCompanyModal: false, notifications: [], showNotifications: false } },
  async mounted() {
    await this.loadStats()
  },
  activated() {
    this.loadStats()
  },
  methods: {
    async loadStats() {
      try {
        this.profile = (await api.get('/company/profile')).data
        this.stats = (await api.get('/company/stats')).data
        this.notifications = (await api.get('/company/notifications')).data
      } catch(e) {
        console.error("Failed to load company data:", e)
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
.nav-link:not(.bg-success):hover { background-color: #f8f9fa; }
.cursor-pointer { cursor: pointer; }
.hover-lift:hover { transform: translateY(-2px); box-shadow: 0 .25rem .75rem rgba(0,0,0,.1)!important; }
</style>
