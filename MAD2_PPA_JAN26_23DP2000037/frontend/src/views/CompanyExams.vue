<template>
  <div class="d-flex">
    <nav class="d-flex flex-column p-3 bg-success text-white" style="width:200px;min-height:100vh">
      <h5 class="mb-3">🏢 Company</h5>
      <router-link to="/company/dashboard" class="btn btn-outline-light mb-2 text-start">📊 Dashboard</router-link>
      <router-link to="/company/drives" class="btn btn-outline-light mb-2 text-start">📋 Drives</router-link>
      <router-link to="/company/exams" class="btn btn-outline-light mb-2 text-start">📝 Applicants</router-link>
      <router-link to="/company/history" class="btn btn-outline-light mb-2 text-start">📜 History</router-link>
      <button @click="$store.commit('LOGOUT'); $router.push('/login')" class="btn btn-danger mt-auto">Logout</button>
    </nav>
    <div class="p-4 flex-grow-1">
      <h4>Applicants</h4>
      <div class="mb-3">
        <label class="form-label">Select Drive:</label>
        <select v-model="selectedDrive" @change="loadApplicants" class="form-select" style="max-width:400px">
          <option value="">-- Choose a drive --</option>
          <option v-for="d in drives" :key="d.id" :value="d.id">{{ d.job_title }} ({{ d.applicants }} applicants)</option>
        </select>
      </div>
      <div v-if="selectedDrive">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr><th>Student</th><th>College</th><th>Branch</th><th>GPA</th><th>Applied</th><th>Status</th><th>Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="a in applicants" :key="a.application_id">
              <td>{{ a.student_name }}</td>
              <td>{{ a.college }}</td>
              <td>{{ a.branch }}</td>
              <td>{{ a.gpa }}</td>
              <td>{{ a.applied_at }}</td>
              <td><span class="badge" :class="{
                'bg-primary':a.status==='applied','bg-info':a.status==='shortlisted',
                'bg-warning':a.status==='waitlisted','bg-success':a.status==='selected','bg-danger':a.status==='rejected'
              }">{{ a.status }}</span></td>
              <td>
                <div class="btn-group btn-group-sm">
                  <button @click="updateStatus(a.application_id, 'shortlisted')" class="btn btn-outline-info" :disabled="a.status==='shortlisted'">Shortlist</button>
                  <button @click="updateStatus(a.application_id, 'waitlisted')" class="btn btn-outline-warning" :disabled="a.status==='waitlisted'">Waitlist</button>
                  <button @click="updateStatus(a.application_id, 'selected')" class="btn btn-outline-success" :disabled="a.status==='selected'">Select</button>
                  <button @click="updateStatus(a.application_id, 'rejected')" class="btn btn-outline-danger" :disabled="a.status==='rejected'">Reject</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="!applicants.length" class="text-muted">No applicants for this drive.</p>
      </div>
    </div>
  </div>
</template>
<script>
import api from '../axios'
export default {
  data() { return { drives: [], applicants: [], selectedDrive: '' } },
  async mounted() {
    this.drives = (await api.get('/company/drives')).data
    const q = this.$route.query.drive
    if (q) { this.selectedDrive = parseInt(q); this.loadApplicants() }
  },
  methods: {
    async loadApplicants() {
      if (!this.selectedDrive) return
      this.applicants = (await api.get(`/company/drives/${this.selectedDrive}/applicants`)).data
    },
    async updateStatus(appId, status) {
      await api.post(`/company/applications/${appId}/status`, { status })
      this.loadApplicants()
    }
  }
}
</script>
