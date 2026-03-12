<template>
  <div class="d-flex min-vh-100 bg-light font-sans">
    
    <div class="bg-white shadow-sm d-flex flex-column" style="width: 250px;">
      <div class="p-4 border-bottom text-center">
        <h4 class="fw-bold text-primary mb-0">PlacementPortal</h4>
        <span class="badge bg-primary mt-2">Company Portal</span>
      </div>
      <div class="p-3 flex-grow-1">
        <ul class="nav flex-column gap-2">
          <li class="nav-item">
            <router-link to="/company/dashboard" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-grid-fill me-2"></i> Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/company/drives" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-briefcase-fill me-2"></i> Placement Drives</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/company/interviews" class="nav-link rounded-3 text-white fw-semibold bg-primary"><i class="bi bi-calendar-event me-2"></i> Interviews</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/company/history" class="nav-link rounded-3 text-dark fw-semibold"><i class="bi bi-clock-history me-2"></i> History</router-link>
          </li>
        </ul>
      </div>
      <div class="p-4 border-top">
        <button @click="$store.commit('LOGOUT'); $router.push('/login')" class="btn btn-light w-100 text-start fw-semibold text-danger"><i class="bi bi-box-arrow-right me-2"></i> Logout</button>
      </div>
    </div>

    
    <div class="flex-grow-1 d-flex flex-column">
      
      <nav class="navbar navbar-light bg-white shadow-sm px-4 py-3">
        <h5 class="mb-0 fw-bold text-dark">Interview Management</h5>
        <div class="ms-auto d-flex align-items-center gap-3">
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border">
            <div class="bg-primary text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">{{ $store.state.username.charAt(0).toUpperCase() }}</div>
            <span class="fw-semibold small">{{ $store.state.username }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto">
        <div v-if="msg" class="alert alert-success border-0 shadow-sm rounded-4 mb-4"><i class="bi bi-check-circle-fill me-2"></i> {{ msg }}</div>
        <div v-if="error" class="alert alert-danger border-0 shadow-sm rounded-4 mb-4"><i class="bi bi-exclamation-circle-fill me-2"></i> {{ error }}</div>

        
        <ul class="nav nav-tabs mb-4" role="tablist">
          <li class="nav-item" role="presentation">
            <button class="nav-link active fw-bold" id="scheduled-tab" @click="activeTab = 'scheduled'" type="button" role="tab" aria-selected="true">
              <i class="bi bi-calendar-check me-2"></i> Scheduled Interviews
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link fw-bold" id="completed-tab" @click="activeTab = 'completed'" type="button" role="tab" aria-selected="false">
              <i class="bi bi-check-circle me-2"></i> Completed
            </button>
          </li>
        </ul>

        
        <div v-if="activeTab === 'scheduled'" class="card border-0 shadow-sm rounded-4">
          <div class="card-body p-0">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Student</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Position</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Date</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Time</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Mode</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="iv in scheduledInterviews" :key="iv.id">
                  <td class="px-4 py-3 fw-bold text-dark"><i class="bi bi-person text-muted me-2"></i>{{ iv.student_name }}</td>
                  <td class="px-4 py-3">{{ iv.job_title }}</td>
                  <td class="px-4 py-3">{{ iv.scheduled_date }}</td>
                  <td class="px-4 py-3">{{ iv.scheduled_time }}</td>
                  <td class="px-4 py-3">
                    <span v-if="iv.mode === 'online'" class="badge bg-info bg-opacity-10 text-info px-3 py-2">Online</span>
                    <span v-else class="badge bg-secondary bg-opacity-10 text-secondary px-3 py-2">In-Person</span>
                  </td>
                  <td class="px-4 py-3">
                    <button @click="editInterview(iv)" class="btn btn-sm btn-outline-primary rounded-2 me-2"><i class="bi bi-pencil me-1"></i> Edit</button>
                    <button @click="openResultModal(iv)" class="btn btn-sm btn-outline-success rounded-2"><i class="bi bi-check-lg me-1"></i> Result</button>
                  </td>
                </tr>
                <tr v-if="scheduledInterviews.length === 0">
                  <td colspan="6" class="text-center py-4 text-muted">No scheduled interviews</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        
        <div v-if="activeTab === 'completed'" class="card border-0 shadow-sm rounded-4">
          <div class="card-body p-0">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Student</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Position</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Date</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Result</th>
                  <th class="border-0 px-4 py-3 text-muted fw-semibold">Feedback</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="iv in completedInterviews" :key="iv.id">
                  <td class="px-4 py-3 fw-bold text-dark"><i class="bi bi-person text-muted me-2"></i>{{ iv.student_name }}</td>
                  <td class="px-4 py-3">{{ iv.job_title }}</td>
                  <td class="px-4 py-3">{{ iv.scheduled_date }}</td>
                  <td class="px-4 py-3">
                    <span v-if="iv.result === 'passed'" class="badge bg-success bg-opacity-10 text-success fw-bold rounded-pill px-3 py-2"><i class="bi bi-check-circle me-1"></i> Passed</span>
                    <span v-else class="badge bg-danger bg-opacity-10 text-danger fw-bold rounded-pill px-3 py-2"><i class="bi bi-x-circle me-1"></i> Failed</span>
                  </td>
                  <td class="px-4 py-3 small">{{ iv.notes || '-' }}</td>
                </tr>
                <tr v-if="completedInterviews.length === 0">
                  <td colspan="5" class="text-center py-4 text-muted">No completed interviews</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    
    <div v-if="showEditModal" class="modal d-block" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 rounded-4 shadow-lg">
          <div class="modal-header border-bottom-0 p-4">
            <h5 class="modal-title fw-bold">Edit Interview</h5>
            <button @click="showEditModal = false" type="button" class="btn-close"></button>
          </div>
          <div class="modal-body p-4">
            <div class="mb-3">
              <label class="form-label fw-semibold">Date</label>
              <input v-model="editForm.scheduled_date" type="date" class="form-control bg-light border-0" />
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Time</label>
              <input v-model="editForm.scheduled_time" type="time" class="form-control bg-light border-0" />
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Location</label>
              <input v-model="editForm.location" type="text" class="form-control bg-light border-0" placeholder="e.g., Room 301, Building A" />
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Mode</label>
              <select v-model="editForm.mode" class="form-select bg-light border-0">
                <option value="online">Online</option>
                <option value="in-person">In-Person</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Notes</label>
              <textarea v-model="editForm.notes" class="form-control bg-light border-0" rows="3" placeholder="Any additional notes..."></textarea>
            </div>
          </div>
          <div class="modal-footer border-top-0 p-4">
            <button @click="showEditModal = false" type="button" class="btn btn-light rounded-pill">Cancel</button>
            <button @click="saveInterview" type="button" class="btn btn-primary rounded-pill fw-bold" :disabled="saving"><span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>Save</button>
          </div>
        </div>
      </div>
    </div>

    
    <div v-if="showResultModal" class="modal d-block" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 rounded-4 shadow-lg">
          <div class="modal-header border-bottom-0 p-4">
            <h5 class="modal-title fw-bold">Record Interview Result</h5>
            <button @click="showResultModal = false" type="button" class="btn-close"></button>
          </div>
          <div class="modal-body p-4">
            <div class="mb-3">
              <p class="text-muted">Candidate: <strong>{{ selectedInterview?.student_name }}</strong></p>
              <p class="text-muted">Position: <strong>{{ selectedInterview?.job_title }}</strong></p>
            </div>
            <div class="mb-4">
              <label class="form-label fw-semibold">Interview Result</label>
              <div class="d-flex gap-3">
                <div class="form-check">
                  <input v-model="resultForm.result" type="radio" value="passed" class="form-check-input" id="passed" />
                  <label class="form-check-label" for="passed"><i class="bi bi-check-circle text-success me-2"></i> Passed</label>
                </div>
                <div class="form-check">
                  <input v-model="resultForm.result" type="radio" value="failed" class="form-check-input" id="failed" />
                  <label class="form-check-label" for="failed"><i class="bi bi-x-circle text-danger me-2"></i> Failed</label>
                </div>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Feedback</label>
              <textarea v-model="resultForm.notes" class="form-control bg-light border-0" rows="3" placeholder="Add feedback or reasons..."></textarea>
            </div>
          </div>
          <div class="modal-footer border-top-0 p-4">
            <button @click="showResultModal = false" type="button" class="btn btn-light rounded-pill">Cancel</button>
            <button @click="saveResult" type="button" class="btn btn-success rounded-pill fw-bold" :disabled="saving"><span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>Save Result</button>
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
      interviews: [],
      activeTab: 'scheduled',
      showEditModal: false,
      showResultModal: false,
      msg: null,
      error: null,
      saving: false,
      editForm: {
        id: null,
        scheduled_date: '',
        scheduled_time: '',
        location: '',
        mode: 'online',
        notes: ''
      },
      selectedInterview: null,
      resultForm: {
        result: 'passed',
        notes: ''
      }
    }
  },
  computed: {
    scheduledInterviews() {
      return this.interviews.filter(iv => iv.result === 'pending')
    },
    completedInterviews() {
      return this.interviews.filter(iv => iv.result !== 'pending')
    }
  },
  async mounted() {
    try {
      this.interviews = (await api.get('/company/interviews')).data
    } catch(e) {
      console.error("Failed to load interviews:", e)
      this.error = "Failed to load interviews. Please refresh the page."
    }
  },
  methods: {
    editInterview(iv) {
      this.editForm = {
        id: iv.id,
        scheduled_date: iv.scheduled_date,
        scheduled_time: iv.scheduled_time,
        location: iv.location,
        mode: iv.mode,
        notes: iv.notes
      }
      this.showEditModal = true
    },
    async saveInterview() {
      this.saving = true
      this.error = null
      try {
        await api.put(`/company/interviews/${this.editForm.id}`, {
          scheduled_date: this.editForm.scheduled_date,
          scheduled_time: this.editForm.scheduled_time,
          location: this.editForm.location,
          mode: this.editForm.mode,
          notes: this.editForm.notes
        })
        this.msg = "Interview updated successfully"
        this.showEditModal = false
        this.interviews = (await api.get('/company/interviews')).data
        setTimeout(() => { this.msg = null }, 3000)
      } catch(e) {
        this.error = e.response?.data?.error || "Failed to update interview"
      } finally {
        this.saving = false
      }
    },
    openResultModal(iv) {
      this.selectedInterview = iv
      this.resultForm = {
        result: 'passed',
        notes: ''
      }
      this.showResultModal = true
    },
    async saveResult() {
      this.saving = true
      this.error = null
      try {
        await api.post(`/company/interviews/${this.selectedInterview.id}/result`, {
          result: this.resultForm.result
        })
        
        if (this.resultForm.notes) {
          await api.put(`/company/interviews/${this.selectedInterview.id}`, {
            notes: this.resultForm.notes
          })
        }
        this.msg = `Interview result recorded - Student ${this.resultForm.result === 'passed' ? 'SELECTED' : 'REJECTED'}`
        this.showResultModal = false
        this.interviews = (await api.get('/company/interviews')).data
        setTimeout(() => { this.msg = null }, 3000)
      } catch(e) {
        this.error = e.response?.data?.error || "Failed to save result"
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.font-sans { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
.nav-link:not(.bg-primary):hover { background-color: #f8f9fa; }
.modal { background-color: rgba(0, 0, 0, 0.5); }
.nav-tabs .nav-link.active {
  border-color: #007bff;
  color: #007bff;
  border-bottom: 3px solid #007bff !important;
  background-color: transparent;
}
</style>
