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
            <router-link to="/company/drives" class="nav-link rounded-3 text-white fw-semibold bg-success"><i class="bi bi-briefcase-fill me-2"></i> My Drives</router-link>
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
        <h5 class="mb-0 fw-bold text-dark">My Placement Drives</h5>
        <div class="ms-auto d-flex align-items-center gap-3">
          <button @click="creating = !creating" class="btn btn-success rounded-pill px-4 fw-semibold shadow-sm">
            <i class="bi" :class="creating ? 'bi-x-lg' : 'bi-plus-lg'"></i> {{ creating ? 'Cancel Posting' : 'Post New Drive' }}
          </button>
          <div class="d-flex align-items-center gap-2 bg-light px-3 py-1 rounded-pill border ms-2">
            <div class="bg-success text-white rounded-circle d-flex justify-content-center align-items-center fw-bold" style="width: 32px; height: 32px;">
              <i class="bi bi-building"></i>
            </div>
            <span class="fw-semibold small">{{ username }}</span>
          </div>
        </div>
      </nav>

      
      <div class="p-4 flex-grow-1 overflow-auto">
        
        <div v-if="creating" class="card border-0 shadow-sm rounded-4 mb-4">
          <div class="card-body p-4">
            <h5 class="fw-bold mb-4"><i class="bi bi-building-add text-success me-2"></i>Post a New Placement Drive</h5>
            <form @submit.prevent="createDrive">
              <div class="row g-3">
                <div class="col-md-6 form-floating">
                  <input v-model="form.job_title" class="form-control bg-light border-0" id="jt" placeholder="Job Title" required />
                  <label for="jt" class="ms-2">Job Title</label>
                </div>
                <div class="col-md-6 form-floating">
                  <input v-model="form.deadline" type="date" class="form-control bg-light border-0" id="dl" required />
                  <label for="dl" class="ms-2">Application Deadline</label>
                </div>
                
                <div class="col-12">
                  <label class="form-label text-muted small fw-bold mb-1">Job Description</label>
                  <textarea v-model="form.job_description" class="form-control bg-light border-0" rows="3" placeholder="Enter roles, responsibilities, and perks..."></textarea>
                </div>

                <div class="col-12 mt-4"><h6 class="fw-bold text-muted border-bottom pb-2">Eligibility Criteria</h6></div>

                <div class="col-md-4 form-floating">
                  <input v-model="form.eligibility_branch" class="form-control bg-light border-0" id="eb" placeholder="e.g. CSE, IT" />
                  <label for="eb" class="ms-2">Eligible Branches</label>
                </div>
                <div class="col-md-4 form-floating">
                  <input v-model.number="form.eligibility_gpa" type="number" step="0.1" class="form-control bg-light border-0" id="eg" placeholder="Min. GPA" />
                  <label for="eg" class="ms-2">Minimum GPA Base</label>
                </div>
                <div class="col-md-4 form-floating">
                  <input v-model.number="form.eligibility_year" type="number" class="form-control bg-light border-0" id="ey" placeholder="Passing Year" />
                  <label for="ey" class="ms-2">Target Passing Year</label>
                </div>
              </div>
              <div class="mt-4 text-end">
                <button type="submit" class="btn btn-success fw-bold px-5 rounded-pill shadow-sm">Submit for Approval</button>
              </div>
            </form>
          </div>
        </div>

        
        <div v-if="!creating && drives.length === 0" class="text-center py-5">
          <div class="bg-white rounded-circle d-inline-flex justify-content-center align-items-center shadow-sm mb-3" style="width: 80px; height: 80px;">
            <i class="bi bi-briefcase text-muted fs-1"></i>
          </div>
          <h4 class="fw-bold text-dark">No Drives Posted Yet</h4>
          <p class="text-muted">Start hiring by posting your first placement drive.</p>
          <button @click="creating = true" class="btn btn-success rounded-pill px-4 mt-2">Post New Drive</button>
        </div>

        <div v-for="d in drives" :key="d.id" class="card border-0 shadow-sm rounded-4 mb-4 overflow-hidden">
          <div class="card-header bg-white border-bottom-0 pt-4 pb-0 px-4 d-flex justify-content-between align-items-start">
            <div>
              <h4 class="fw-bold text-dark mb-1">{{ d.job_title }}</h4>
              <p class="text-muted small mb-0"><i class="bi bi-calendar3 me-1"></i> Posted: {{ d.created_at.split(' ')[0] }} | <i class="bi bi-calendar-x me-1 ms-2"></i> Deadline: {{ d.deadline ? d.deadline.split(' ')[0] : 'None' }}</p>
            </div>
            <span v-if="d.status === 'approved'" class="badge bg-success bg-opacity-10 text-success rounded-pill px-3 py-2">Active</span>
            <span v-else-if="d.status === 'pending'" class="badge bg-warning bg-opacity-10 text-warning rounded-pill px-3 py-2">Pending Admin Approval</span>
            <span v-else class="badge bg-secondary bg-opacity-10 text-secondary rounded-pill px-3 py-2">Closed</span>
          </div>
          <div class="card-body px-4 pb-4">
            <div class="row mt-3">
              <div class="col-md-3">
                <div class="bg-light rounded-3 p-3 text-center">
                  <div class="text-muted small fw-semibold">Applicants</div>
                  <h3 class="fw-bold text-dark mb-0 mt-1">{{ d.applicants.length }}</h3>
                </div>
              </div>
              <div class="col-md-9 pt-2">
                <h6 class="fw-bold text-dark">Requirements</h6>
                <div class="d-flex gap-2 flex-wrap">
                  <span class="badge border text-dark fw-normal"><i class="bi bi-mortarboard me-1"></i> {{ d.eligibility_branch || 'Any Branch' }}</span>
                  <span class="badge border text-dark fw-normal"><i class="bi bi-journal-bookmark me-1"></i> Min GPA: {{ d.eligibility_gpa || 'N/A' }}</span>
                  <span class="badge border text-dark fw-normal"><i class="bi bi-calendar-check me-1"></i> Year: {{ d.eligibility_year || 'Any' }}</span>
                </div>
              </div>
            </div>

            <div v-if="d.applicants.length > 0" class="mt-4 pt-3 border-top">
              <h6 class="fw-bold text-dark mb-3">Recent Applicants</h6>
              <table class="table table-hover align-middle">
                <tbody>
                  <tr v-for="a in d.applicants" :key="a.id">
                    <td>
                      <div class="fw-semibold text-dark">{{ a.student_name }}</div>
                      <div class="text-muted small">Applied: {{ a.applied_at.split(' ')[0] }}</div>
                    </td>
                    <td class="text-end">
                      <select v-model="a.status" @change="updateStatus(a.id, a.status)" class="form-select form-select-sm d-inline-block w-auto bg-light border-0 shadow-sm rounded-3">
                        <option value="applied">Applied</option>
                        <option value="shortlisted">Shortlisted</option>
                        <option value="selected">Selected</option>
                        <option value="rejected">Rejected</option>
                      </select>
                      <button v-if="a.status === 'applied' || a.status === 'shortlisted'" @click="openInterviewModal(a, d.id, d.job_title)" class="btn btn-sm btn-outline-primary rounded-2 ms-2">
                        <i class="bi bi-calendar-event me-1"></i> Schedule Interview
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="text-end mt-3" v-if="d.status === 'approved'">
              <button @click="closeDrive(d.id)" class="btn btn-outline-danger btn-sm rounded-pill px-4 fw-semibold shadow-sm"><i class="bi bi-x-circle me-1"></i> Stop Applications / Close Drive</button>
            </div>
          </div>
        </div>

      </div>
    </div>

    
    <div v-if="showInterviewModal" class="modal d-block" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 rounded-4 shadow-lg">
          <div class="modal-header border-bottom-0 p-4">
            <h5 class="modal-title fw-bold">Schedule Interview</h5>
            <button @click="showInterviewModal = false" type="button" class="btn-close"></button>
          </div>
          <div class="modal-body p-4">
            <div class="mb-3 p-3 bg-light rounded-3">
              <small class="text-muted">Candidate</small>
              <p class="fw-bold text-dark mb-0">{{ interviewForm.student_name }}</p>
              <small class="text-muted">Position: {{ interviewForm.job_title }}</small>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Date</label>
              <input v-model="interviewForm.scheduled_date" type="date" class="form-control bg-light border-0" />
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Time</label>
              <input v-model="interviewForm.scheduled_time" type="time" class="form-control bg-light border-0" />
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Location</label>
              <input v-model="interviewForm.location" type="text" class="form-control bg-light border-0" placeholder="e.g., Room 301, Building A" />
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Mode</label>
              <select v-model="interviewForm.mode" class="form-select bg-light border-0">
                <option value="online">Online</option>
                <option value="in-person">In-Person</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Notes (Optional)</label>
              <textarea v-model="interviewForm.notes" class="form-control bg-light border-0" rows="2" placeholder="Any additional details..."></textarea>
            </div>
          </div>
          <div class="modal-footer border-top-0 p-4">
            <button @click="showInterviewModal = false" type="button" class="btn btn-light rounded-pill">Cancel</button>
            <button @click="scheduleInterview" type="button" class="btn btn-success rounded-pill fw-bold">Schedule Interview</button>
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
      drives: [], 
      creating: false, 
      form: { job_title:'', job_description:'', eligibility_branch:'', eligibility_gpa:null, eligibility_year:null, deadline:null }, 
      username: this.$store.state.username,
      showInterviewModal: false,
      interviewForm: {
        application_id: null,
        student_name: '',
        job_title: '',
        scheduled_date: '',
        scheduled_time: '',
        location: '',
        mode: 'online',
        notes: ''
      }
    } 
  },
  async mounted() { this.load() },
  methods: {
    async load() { this.drives = (await api.get('/company/drives')).data },
    async createDrive() {
      try {
        const payload = { ...this.form }
        if (payload.deadline) {
          payload.deadline = new Date(payload.deadline).toISOString()
        }
        await api.post('/company/drives', payload)
        this.creating = false
        this.form = { job_title:'', job_description:'', eligibility_branch:'', eligibility_gpa:null, eligibility_year:null, deadline:null }
        this.load()
      } catch(e) { alert(e.response?.data?.error || 'Failed to post drive') }
    },
    async closeDrive(id) {
      if(confirm('Are you sure you want to close this drive?')) {
        await api.post(`/company/drives/${id}/close`)
        this.load()
      }
    },
    async updateStatus(appId, newStatus) {
      await api.post(`/company/applications/${appId}/status`, { status: newStatus })
      this.load()
    },
    openInterviewModal(applicant, driveId, jobTitle) {
      this.interviewForm = {
        application_id: applicant.id,
        student_name: applicant.student_name,
        job_title: jobTitle,
        scheduled_date: '',
        scheduled_time: '',
        location: '',
        mode: 'online',
        notes: ''
      }
      this.showInterviewModal = true
    },
    async scheduleInterview() {
      try {
        await api.post('/company/interviews', {
          application_id: this.interviewForm.application_id,
          scheduled_date: this.interviewForm.scheduled_date,
          scheduled_time: this.interviewForm.scheduled_time,
          location: this.interviewForm.location,
          mode: this.interviewForm.mode,
          notes: this.interviewForm.notes
        })
        alert('Interview scheduled successfully!')
        this.showInterviewModal = false
        this.load()
      } catch(e) { alert(e.response?.data?.error || 'Failed to schedule interview') }
    }
  }
}
</script>

<style scoped>
.font-sans { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
.nav-link:not(.bg-success):hover { background-color: #f8f9fa; }
</style>
