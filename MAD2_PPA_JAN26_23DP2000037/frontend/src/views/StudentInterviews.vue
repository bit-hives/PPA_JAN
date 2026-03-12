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
            <router-link to="/student/placement" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-award-fill me-2"></i> Application Status</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/student/interviews" class="nav-link rounded-3 text-white fw-semibold bg-primary"><i class="bi bi-calendar-event me-2"></i> Interviews</router-link>
          </li>
        </ul>
      </div>
      <div class="p-4 border-top">
        <button @click="$store.commit('LOGOUT'); $router.push('/login')" class="btn btn-light w-100 text-start fw-semibold text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</button>
      </div>
    </div>

    
    <div class="flex-grow-1 d-flex flex-column">
      
      <nav class="navbar navbar-light bg-white shadow-sm px-4 py-3">
        <h5 class="mb-0 fw-bold text-dark">My Interviews</h5>
        <div class="ms-auto d-flex align-items-center gap-3">
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border">
            <div class="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">
              <i class="bi bi-person-fill"></i>
            </div>
            <span class="fw-semibold small">{{ $store.state.username }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto">
        
        <h5 class="fw-bold mb-3"><i class="bi bi-calendar2-event text-primary me-2"></i>Upcoming Interviews</h5>
        <div class="card border-0 shadow-sm rounded-4 mb-5">
          <div class="card-body p-0">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Company</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Position</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold text-center">Date & Time</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Location</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Mode</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="iv in upcomingInterviews" :key="iv.id">
                  <td class="px-4 py-3 fw-bold text-dark"><i class="bi bi-building text-muted me-2"></i>{{ iv.company_name }}</td>
                  <td class="px-4 py-3">{{ iv.job_title }}</td>
                  <td class="px-4 py-3 text-center">
                    <div class="fw-semibold">{{ iv.scheduled_date }}</div>
                    <div class="small text-muted">{{ iv.scheduled_time }}</div>
                  </td>
                  <td class="px-4 py-3">{{ iv.location || '-' }}</td>
                  <td class="px-4 py-3">
                    <span v-if="iv.mode === 'online'" class="badge bg-info bg-opacity-10 text-info px-3 py-2"><i class="bi bi-camera-video me-1"></i> Online</span>
                    <span v-else class="badge bg-secondary bg-opacity-10 text-secondary px-3 py-2"><i class="bi bi-geo-alt me-1"></i> In-Person</span>
                  </td>
                </tr>
                <tr v-if="upcomingInterviews.length === 0">
                  <td colspan="5" class="text-center py-4 text-muted">No upcoming interviews</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        
        <h5 class="fw-bold mb-3"><i class="bi bi-check-circle text-success me-2"></i>Interview Results</h5>
        <div class="row g-3">
          <div v-for="iv in completedInterviews" :key="iv.id" class="col-md-6">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <div>
                    <h6 class="fw-bold text-dark mb-1">{{ iv.company_name }}</h6>
                    <p class="text-muted small mb-0">{{ iv.job_title }}</p>
                  </div>
                  <span v-if="iv.result === 'passed'" class="badge bg-success bg-opacity-10 text-success fw-bold rounded-pill px-3 py-2"><i class="bi bi-check-circle me-1"></i> Passed</span>
                  <span v-else class="badge bg-danger bg-opacity-10 text-danger fw-bold rounded-pill px-3 py-2"><i class="bi bi-x-circle me-1"></i> Failed</span>
                </div>
                <div class="border-top pt-3">
                  <small class="text-muted">Interview Date:</small>
                  <p class="small fw-semibold mb-2">{{ iv.scheduled_date }} at {{ iv.scheduled_time }}</p>
                  <small v-if="iv.notes" class="text-muted">Feedback:</small>
                  <p v-if="iv.notes" class="small text-dark">{{ iv.notes }}</p>
                  <p v-else class="small text-muted">-</p>
                </div>
              </div>
            </div>
          </div>
          <div v-if="completedInterviews.length === 0" class="col-12">
            <div class="alert alert-light border-0 rounded-4 text-center py-4">
              <p class="text-muted mb-0">No interview results yet</p>
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
  data() {
    return {
      interviews: []
    }
  },
  computed: {
    upcomingInterviews() {
      return this.interviews.filter(iv => iv.result === 'pending')
    },
    completedInterviews() {
      return this.interviews.filter(iv => iv.result !== 'pending')
    }
  },
  async mounted() {
    try {
      this.interviews = (await api.get('/student/interviews')).data
    } catch(e) {
      console.error("Failed to load interviews:", e)
      alert("Failed to load interviews. Please refresh the page.")
    }
  }
}
</script>

<style scoped>
.font-sans { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
.nav-link:not(.bg-primary):hover { background-color: #f8f9fa; }
</style>
