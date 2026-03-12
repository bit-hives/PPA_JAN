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
            <router-link to="/student/notifications" class="nav-link rounded-3 text-white fw-semibold bg-primary"><i class="bi bi-bell-fill me-2"></i> Alerts & Off-Campus</router-link>
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
        <h5 class="mb-0 fw-bold text-dark">Notifications & Alerts</h5>
        <div class="ms-auto d-flex align-items-center gap-3">
          <button class="btn btn-light rounded-circle p-2 position-relative"><i class="bi bi-bell-fill"></i></button>
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border ms-2">
            <div class="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">
              <i class="bi bi-person-fill"></i>
            </div>
            <span class="fw-semibold small">{{ $store.state.username }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto d-flex flex-column align-items-center">
        <div class="w-100" style="max-width: 800px;">
          
          <div v-for="(n, i) in notifications" :key="i" class="card border-0 shadow-sm rounded-4 mb-3 hover-lift">
            <div class="card-body p-4 d-flex gap-4">
              <div v-if="n.type === 'deadline'" class="bg-warning bg-opacity-10 text-warning rounded-circle d-flex justify-content-center align-items-center fs-3 flex-shrink-0" style="width: 60px; height: 60px;">
                <i class="bi bi-exclamation-triangle-fill"></i>
              </div>
              <div v-else-if="n.type === 'status'" class="bg-info bg-opacity-10 text-info rounded-circle d-flex justify-content-center align-items-center fs-3 flex-shrink-0" style="width: 60px; height: 60px;">
                <i class="bi bi-info-circle-fill"></i>
              </div>
              <div v-else class="bg-primary bg-opacity-10 text-primary rounded-circle d-flex justify-content-center align-items-center fs-3 flex-shrink-0" style="width: 60px; height: 60px;">
                <i class="bi bi-briefcase-fill"></i>
              </div>

              <div>
                <h5 class="fw-bold text-dark mb-1">{{ n.message }}</h5>
                <p class="text-muted small mb-0"><i class="bi bi-clock me-1"></i> System Notification</p>
                
                <div class="mt-2">
                  <span v-if="n.type === 'new_drive'" class="badge border text-dark">New Opportunity</span>
                  <span v-if="n.type === 'status'" class="badge border text-dark">Application Update</span>
                  <span v-if="n.type === 'deadline'" class="badge border text-danger border-danger">Expiring Soon</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="notifications.length === 0" class="text-center py-5 mt-5">
            <div class="bg-white rounded-circle d-inline-flex justify-content-center align-items-center shadow-sm mb-3" style="width: 80px; height: 80px;">
              <i class="bi bi-bell-slash text-muted fs-1"></i>
            </div>
            <h4 class="fw-bold text-dark">All Caught Up!</h4>
            <p class="text-muted">You have no new notifications right now. Enjoy your day.</p>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../axios'
export default {
  data() { return { notifications: [] } },
  async mounted() {
    this.notifications = (await api.get('/student/notifications')).data
  }
}
</script>

<style scoped>
.font-sans { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
.nav-link:not(.bg-primary):hover { background-color: #f8f9fa; }
.hover-lift { transition: transform 0.2s ease, box-shadow 0.2s ease; cursor: default; }
.hover-lift:hover { transform: translateY(-3px); box-shadow: 0 .5rem 1rem rgba(0,0,0,.10)!important; }
</style>
