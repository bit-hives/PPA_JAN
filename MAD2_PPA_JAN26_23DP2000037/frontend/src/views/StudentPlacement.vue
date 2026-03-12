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
            <router-link to="/student/profile" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-person-badge-fill me-2"></i> My Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/student/notifications" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-bell-fill me-2"></i> Alerts & Off-Campus</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/student/exams" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-pencil-square me-2"></i> Online Exams</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/student/placement" class="nav-link rounded-3 text-white fw-semibold bg-primary"><i class="bi bi-award-fill me-2"></i> Application Status</router-link>
          </li>
        </ul>
      </div>
      <div class="p-4 border-top">
        <button @click="$store.commit('LOGOUT'); $router.push('/login')" class="btn btn-light w-100 text-start fw-semibold text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</button>
      </div>
    </div>

    
    <div class="flex-grow-1 d-flex flex-column">
      
      <nav class="navbar navbar-light bg-white shadow-sm px-4 py-3">
        <h5 class="mb-0 fw-bold text-dark">Track Application Status</h5>
        <div class="ms-auto d-flex align-items-center gap-3">
          <button @click="csvExp" :disabled="loading" class="btn btn-outline-primary rounded-pill px-4 fw-semibold shadow-sm text-decoration-none">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i class="bi bi-cloud-arrow-down-fill me-1"></i> Email CSV Report
          </button>
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border ms-3">
            <div class="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">
              <i class="bi bi-person-fill"></i>
            </div>
            <span class="fw-semibold small">{{ $store.state.username }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto">
        <div v-if="msg" class="alert alert-success border-0 shadow-sm rounded-4 mb-4"><i class="bi bi-check-circle-fill me-2"></i> {{ msg }}</div>
        
        <h5 class="fw-bold mb-3">Active Pipeline</h5>
        <div class="card border-0 shadow-sm rounded-4 mb-5">
          <div class="card-body p-0">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Company</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Role</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold text-center">Applied On</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold text-end">Current Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="a in activeVars" :key="a.id">
                  <td class="px-4 py-3 fw-bold text-dark"><i class="bi bi-building text-muted me-2"></i>{{ a.company }}</td>
                  <td class="px-4 py-3">{{ a.job_title }}</td>
                  <td class="px-4 py-3 text-center text-muted">{{ formatDate(a.applied_at) }}</td>
                  <td class="px-4 py-3 text-end">
                    <span v-if="a.status === 'applied'" class="badge bg-secondary bg-opacity-10 text-secondary rounded-pill px-3 py-2">Applied</span>
                    <span v-else-if="a.status === 'shortlisted'" class="badge bg-info bg-opacity-10 text-info fw-bold rounded-pill px-3 py-2 border border-info">Shortlisted for Interview</span>
                    <span v-else class="badge bg-light text-dark rounded-pill px-3 py-2">{{ a.status }}</span>
                  </td>
                </tr>
                <tr v-if="activeVars.length === 0">
                  <td colspan="4" class="text-center py-4 text-muted">You have no active applications. Apply to a drive to get started.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <h5 class="fw-bold mb-3">Historical Results</h5>
        <div class="card border-0 shadow-sm rounded-4">
          <div class="card-body p-0">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Company</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Role</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold text-center">Result Date</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold text-end">Final Outcome</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="h in history" :key="h.id">
                  <td class="px-4 py-3 fw-bold text-dark"><i class="bi bi-building text-muted me-2"></i>{{ h.company }}</td>
                  <td class="px-4 py-3">{{ h.job_title }}</td>
                  <td class="px-4 py-3 text-center text-muted">{{ formatDate(h.result_date) }}</td>
                  <td class="px-4 py-3 text-end">
                    <span v-if="h.status === 'selected'" class="badge bg-success bg-opacity-10 text-success fw-bold rounded-pill px-3 py-2 border border-success"><i class="bi bi-award me-1"></i> Selected / Offered</span>
                    <span v-else-if="h.status === 'rejected'" class="badge bg-danger bg-opacity-10 text-danger fw-bold rounded-pill px-3 py-2">Rejected</span>
                  </td>
                </tr>
                <tr v-if="history.length === 0">
                  <td colspan="4" class="text-center py-4 text-muted">No historical data available yet.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import api from '../axios'
export default {
  data() { return { activeVars: [], history: [], msg: null, loading: false } },
  async mounted() {
    try {
      this.activeVars = (await api.get('/student/applications')).data
      this.history = (await api.get('/student/history')).data
    } catch(e) {
      console.error("Failed to load applications:", e)
      alert("Failed to load your application status. Please refresh the page.")
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr || dateStr === 'None' || dateStr === '') return 'N/A'
      return dateStr.split(' ')[0]
    },
    async csvExp() {
      this.loading = true; this.msg = null
      try {
        const res = await api.post('/jobs/export-csv')
        this.msg = res.data.message
      } catch(e) { alert('Failed to trigger export') }
      finally { this.loading = false }
    }
  }
}
</script>

<style scoped>
.font-sans { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
.nav-link:not(.bg-primary):hover { background-color: #f8f9fa; }
</style>
