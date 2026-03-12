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
            <router-link to="/admin/dashboard" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-grid-fill me-2"></i> Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/students" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-person-lines-fill me-2"></i> Students</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/companies" class="nav-link rounded-3 text-white fw-semibold bg-primary"><i class="bi bi-building-fill me-2"></i> Companies</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/drives" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-briefcase-fill me-2"></i> Drives</router-link>
          </li>
        </ul>
      </div>
      <div class="p-4 border-top">
        <button @click="$store.commit('LOGOUT'); $router.push('/login')" class="btn btn-light w-100 text-start fw-semibold text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</button>
      </div>
    </div>

    
    <div class="flex-grow-1 d-flex flex-column">
      
      <nav class="navbar navbar-light bg-white shadow-sm px-4 py-3">
        <h5 class="mb-0 fw-bold text-dark">Company Management</h5>
        <div class="ms-auto d-flex align-items-center gap-3">
          <div class="input-group" style="width: 250px;">
            <span class="input-group-text bg-light border-0"><i class="bi bi-search"></i></span>
            <input v-model="search" @keyup="load" type="text" class="form-control bg-light border-0" placeholder="Search Companies...">
          </div>
          <button class="btn btn-light rounded-circle p-2 position-relative"><i class="bi bi-bell-fill"></i></button>
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border">
            <div class="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">A</div>
            <span class="fw-semibold small">Admin ID: {{ $store.state.username }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto">
        <div class="card border-0 shadow-sm rounded-4">
          <div class="card-body p-0">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold uppercase" style="font-size: 0.85rem;">Company Info</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold uppercase" style="font-size: 0.85rem;">Sector</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold uppercase" style="font-size: 0.85rem;">Status</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold uppercase" style="font-size: 0.85rem;">Drives</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold uppercase text-end" style="font-size: 0.85rem;">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="c in companies" :key="c.id">
                  <td class="px-4 py-3">
                    <div class="d-flex align-items-center gap-3">
                      <div class="bg-success bg-opacity-10 text-success rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 40px; height: 40px;">
                        <i class="bi bi-building"></i>
                      </div>
                      <div>
                        <div class="fw-bold text-dark">{{ c.name || 'Unknown' }}</div>
                        <div class="text-muted small"><a :href="c.website" target="_blank" class="text-decoration-none">{{ c.website }}</a></div>
                      </div>
                    </div>
                  </td>
                  <td class="px-4 py-3"><span class="badge bg-light text-dark border">{{ c.sector || 'N/A' }}</span></td>
                  <td class="px-4 py-3">
                    <span class="badge bg-success bg-opacity-10 text-success">Active / Approved</span>
                  </td>
                  <td class="px-4 py-3">{{ c.drives || 0 }}</td>
                  <td class="px-4 py-3 text-end">
                    <div>
                      <button @click="toggleActive(c)" class="btn btn-sm rounded-pill fw-semibold" :class="c.is_active ? 'btn-outline-secondary' : 'btn-success'">
                        {{ c.is_active ? 'Deactivate Login' : 'Activate Login' }}
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="companies.length === 0">
                  <td colspan="5" class="text-center py-5 text-muted">No companies found.</td>
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
  data() { return { companies: [], search: '' } },
  async mounted() { this.load() },
  methods: {
    async load() { this.companies = (await api.get('/admin/companies', { params: { q: this.search } })).data },
    async update(id, action) { await api.post(`/admin/companies/${id}/approve`, { action }); this.load() },
    async toggleActive(c) { await api.post(`/admin/users/${c.user_id}/deactivate`); this.load() }
  }
}
</script>

<style scoped>
.font-sans { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
.nav-link:not(.bg-primary):hover { background-color: #f8f9fa; }
.uppercase { text-transform: uppercase; letter-spacing: 0.5px; }
</style>
