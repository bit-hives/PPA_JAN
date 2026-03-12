<template>
  <div class="d-flex min-vh-100 bg-light font-sans">
    
    <div class="bg-white shadow-sm d-flex flex-column" style="width: 250px;">
      <div class="p-4 border-bottom text-center">
        <h4 class="fw-bold text-primary mb-0">PlacementPortal</h4>
        <span class="badge bg-primary mt-2">Admin Dashboard</span>
      </div>
      <div class="p-3 flex-grow-1">
        <ul class="nav flex-column gap-2">
          <li class="nav-item">
            <router-link to="/admin/dashboard" class="nav-link rounded-3 text-dark fw-semibold" active-class="bg-primary text-white"><i class="bi bi-grid-fill me-2"></i> Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/students" class="nav-link rounded-3 text-dark fw-semibold" active-class="bg-primary text-white"><i class="bi bi-person-lines-fill me-2"></i> Students</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/companies" class="nav-link rounded-3 text-dark fw-semibold" active-class="bg-primary text-white"><i class="bi bi-building-fill me-2"></i> Companies</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/drives" class="nav-link rounded-3 text-dark fw-semibold" active-class="bg-primary text-white"><i class="bi bi-briefcase-fill me-2"></i> Drives</router-link>
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
                <div class="fw-bold">{{ n.message }}</div>
                <div class="small text-muted">{{ n.date }}</div>
              </div>
            </div>
          </div>
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border cursor-pointer hover-lift" @click="showAdminModal = true" style="cursor: pointer;">
            <div class="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">{{ adminName.charAt(0).toUpperCase() }}</div>
            <span class="fw-semibold small">{{ adminName }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto">
        
        <div class="row g-4 mb-4">
          <div class="col-12 mb-3 text-end">
            <button @click="exportCSV" class="btn btn-outline-primary rounded-pill fw-bold shadow-sm">
              <i class="bi bi-file-earmark-spreadsheet me-2"></i> Export All Data (CSV)
            </button>
          </div>
          <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column">
                <div class="text-muted fw-semibold mb-2">Active Drives</div>
                <div class="d-flex justify-content-between align-items-center mt-auto">
                  <h2 class="fw-bold mb-0 text-primary">{{ stats.active_drives || 0 }}</h2>
                  <div class="bg-primary bg-opacity-10 text-primary rounded-circle p-3"><i class="bi bi-briefcase fs-4"></i></div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column">
                <div class="text-muted fw-semibold mb-2">Registered Students</div>
                <div class="d-flex justify-content-between align-items-center mt-auto">
                  <h2 class="fw-bold mb-0 text-success">{{ stats.students || 0 }}</h2>
                  <div class="bg-success bg-opacity-10 text-success rounded-circle p-3"><i class="bi bi-people fs-4"></i></div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column">
                <div class="text-muted fw-semibold mb-2">Registered Companies</div>
                <div class="d-flex justify-content-between align-items-center mt-auto">
                  <h2 class="fw-bold mb-0 text-warning">{{ stats.companies || 0 }}</h2>
                  <div class="bg-warning bg-opacity-10 text-warning rounded-circle p-3"><i class="bi bi-building fs-4"></i></div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column">
                <div class="text-muted fw-semibold mb-2">Pending Approvals</div>
                <div class="d-flex justify-content-between align-items-center mt-auto">
                  <h2 class="fw-bold mb-0 text-danger">{{ stats.pending_drives || 0 }}</h2>
                  <div class="bg-danger bg-opacity-10 text-danger rounded-circle p-3"><i class="bi bi-exclamation-circle fs-4"></i></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        
        <div class="row g-4">
          <div class="col-md-8">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4">
                <h5 class="fw-bold text-dark mb-4">Application Status Overview</h5>
                <canvas ref="appChart" style="max-height: 300px;"></canvas>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 bg-primary text-white h-100">
              <div class="card-body p-4 d-flex flex-column justify-content-center text-center">
                <i class="bi bi-rocket-takeoff display-3 mb-3"></i>
                <h4 class="fw-bold">Reports & Notifications</h4>
                <p class="opacity-75">Monthly activity reports are sent to your email automatically at the start of each month.<br>Click below to request a report now.</p>
                <div class="mt-auto">
                  <button @click="requestReport" class="btn btn-light text-primary rounded-pill fw-bold w-100 mb-2">
                    <i class="bi bi-file-earmark-bar-graph me-2"></i> Request Monthly Report
                  </button>
                  <router-link to="/admin/companies" class="btn btn-outline-light rounded-pill fw-bold w-100 mb-2">Review Companies</router-link>
                  <router-link to="/admin/drives" class="btn btn-outline-light rounded-pill fw-bold w-100">Review Drives</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    
    <div v-if="showAdminModal" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-primary text-white border-0">
            <h5 class="modal-title fw-bold">Admin Profile</h5>
            <button type="button" class="btn-close btn-close-white" @click="showAdminModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <div class="text-center mb-4">
              <div class="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center fw-bold mx-auto mb-3" style="width: 80px; height: 80px; font-size: 32px;">{{ adminName.charAt(0).toUpperCase() }}</div>
              <h5 class="fw-bold text-dark">{{ adminName }}</h5>
              <p class="text-muted">System Administrator</p>
            </div>
            <div class="row g-3">
              <div class="col-12">
                <label class="form-label text-muted fw-semibold small">Username</label>
                <div class="p-3 bg-light rounded-2">{{ $store.state.username }}</div>
              </div>
              <div class="col-12">
                <label class="form-label text-muted fw-semibold small">Email</label>
                <div class="p-3 bg-light rounded-2">{{ adminEmail }}</div>
              </div>
              <div class="col-12">
                <label class="form-label text-muted fw-semibold small">Role</label>
                <div class="p-3 bg-light rounded-2">
                  <span class="badge bg-primary">Administrator</span>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer border-top bg-light">
            <button type="button" class="btn btn-primary rounded-pill fw-semibold" @click="showAdminModal = false">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../axios'
import Chart from 'chart.js/auto'

export default {
  data() { return { stats: {}, chartData: null, chartInstance: null, notifications: [], showNotifications: false, adminName: 'Admin', adminEmail: '', showAdminModal: false } },
  async mounted() {
    
    try {
      const adminRes = await api.get('/admin/profile')
      this.adminName = adminRes.data.name || adminRes.data.username || 'Admin'
      this.adminEmail = adminRes.data.email || ''
    } catch(e) {
      console.error("Failed to fetch admin profile", e)
      this.adminName = this.$store.state.username || 'Admin'
    }
    
    const res = await api.get('/admin/stats')
    this.stats = res.data
    this.notifications = (await api.get('/admin/notifications')).data
    
    try {
      const cRes = await api.get('/admin/chart-data')
      this.chartData = cRes.data.applications
      this.renderChart()
    } catch(e) { console.error("Chart data failed", e) }
  },
  methods: {
    renderChart() {
      if(!this.$refs.appChart || !this.chartData) return;
      if(this.chartInstance) this.chartInstance.destroy();
      const ctx = this.$refs.appChart.getContext('2d');
      this.chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.chartData.labels,
          datasets: [{
            label: 'Total Applications',
            data: this.chartData.data,
            backgroundColor: ['#0d6efd', '#ffc107', '#198754', '#dc3545'],
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, grid: { borderDash: [4, 4] } }, x: { grid: { display: false } } }
        }
      });
    },
    async exportCSV() {
      try {
        const res = await api.post('/admin/export-csv')
        alert(res.data.message || 'CSV export started. You will receive it by email.')
      } catch(e) {
        alert(e.response?.data?.error || 'Failed to start CSV export')
      }
    },
    async requestReport() {
      try {
        await api.post('/admin/request-report')
        alert('Report request sent! You will receive it by email.')
      } catch(e) {
        alert(e.response?.data?.error || 'Failed to request report.')
      }
    },
    toggleNotifications() {
      this.showNotifications = !this.showNotifications
    }
  },
  beforeUnmount() {
    if(this.chartInstance) this.chartInstance.destroy();
  }
}
</script>

<style scoped>
.font-sans { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
.nav-link:not(.active):hover { background-color: #f8f9fa; }
.cursor-pointer { cursor: pointer; }
.hover-lift:hover { transform: translateY(-2px); box-shadow: 0 .25rem .75rem rgba(0,0,0,.1)!important; }
</style>
