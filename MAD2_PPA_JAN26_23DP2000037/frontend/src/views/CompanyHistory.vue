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
            <router-link to="/company/dashboard" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-grid-fill me-2"></i> Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/company/drives" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-briefcase-fill me-2"></i> My Drives</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/company/exams" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-file-earmark-text-fill me-2"></i> Exams</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/company/history" class="nav-link rounded-3 text-white fw-semibold bg-success"><i class="bi bi-clock-history me-2"></i> Placement History</router-link>
          </li>
        </ul>
      </div>
      <div class="p-4 border-top">
        <button @click="$store.commit('LOGOUT'); $router.push('/login')" class="btn btn-light w-100 text-start fw-semibold text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</button>
      </div>
    </div>

    
    <div class="flex-grow-1 d-flex flex-column">
      
      <nav class="navbar navbar-light bg-white shadow-sm px-4 py-3">
        <h5 class="mb-0 fw-bold text-dark">Placement History (Closed Drives)</h5>
        <div class="ms-auto d-flex align-items-center gap-3">
          <button class="btn btn-light rounded-circle p-2 position-relative"><i class="bi bi-bell-fill"></i></button>
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border ms-2">
            <div class="bg-success text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">
              <i class="bi bi-building"></i>
            </div>
            <span class="fw-semibold small">{{ $store.state.username }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto">
        <div class="card border-0 shadow-sm rounded-4">
          <div class="card-body p-0">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold" style="font-size: 0.85rem; text-transform: uppercase;">Closed Drive</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold text-center" style="font-size: 0.85rem; text-transform: uppercase;">Total Applicants</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold text-center" style="font-size: 0.85rem; text-transform: uppercase;">Shortlisted</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold text-center" style="font-size: 0.85rem; text-transform: uppercase;">Selected</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold text-center" style="font-size: 0.85rem; text-transform: uppercase;">Rejected</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="h in history" :key="h.id">
                  <td class="px-4 py-4">
                    <div class="fw-bold text-dark fs-5 mb-1">{{ h.job_title }}</div>
                    <div class="text-muted small"><i class="bi bi-calendar-check me-1"></i> Closed On: {{ h.deadline ? h.deadline.split(' ')[0] : 'N/A' }}</div>
                  </td>
                  <td class="px-4 py-4 text-center">
                    <span class="badge bg-light text-dark border px-3 py-2 fs-6">{{ h.total_applicants || 0 }}</span>
                  </td>
                  <td class="px-4 py-4 text-center">
                    <span class="badge bg-warning bg-opacity-10 text-warning px-3 py-2 fs-6">{{ h.shortlisted || 0 }}</span>
                  </td>
                  <td class="px-4 py-4 text-center">
                    <span class="badge bg-success bg-opacity-10 text-success px-3 py-2 fs-6">{{ h.selected || 0 }}</span>
                  </td>
                  <td class="px-4 py-4 text-center">
                    <span class="badge bg-danger bg-opacity-10 text-danger px-3 py-2 fs-6">{{ h.rejected || 0 }}</span>
                  </td>
                </tr>
                <tr v-if="history.length === 0">
                  <td colspan="5" class="text-center py-5">
                    <div class="text-muted mb-2"><i class="bi bi-journal-x fs-1"></i></div>
                    <h5 class="fw-bold text-dark">No Historical Data</h5>
                    <p class="text-muted">You have no closed placement drives yet.</p>
                  </td>
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
  data() { return { history: [] } },
  async mounted() {
    this.history = (await api.get('/company/history')).data
  }
}
</script>

<style scoped>
.font-sans { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
.nav-link:not(.bg-success):hover { background-color: #f8f9fa; }
</style>
