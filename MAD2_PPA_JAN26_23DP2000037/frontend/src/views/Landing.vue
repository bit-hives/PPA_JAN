<template>
  <div class="min-vh-100 d-flex flex-column">
    <nav class="navbar navbar-dark bg-primary px-4">
      <span class="navbar-brand fw-bold">🎓 Placement Portal</span>
      <div>
        <router-link to="/login" class="btn btn-outline-light me-2">Login</router-link>
        <router-link to="/register/student" class="btn btn-light">Register</router-link>
      </div>
    </nav>
    <div class="flex-grow-1 d-flex align-items-center justify-content-center bg-light">
      <div class="text-center">
        <h1 class="display-4 fw-bold mb-3">Campus Placement Portal</h1>
        <p class="lead text-muted mb-4">Connecting Students, Companies & Institutions for seamless campus recruitment.</p>
        <div class="row justify-content-center g-4 mb-5">
          <div class="col-md-3">
            <div class="card shadow-sm p-4 text-center">
              <i class="bi bi-people-fill text-primary fs-1"></i>
              <h5 class="mt-2">For Students</h5>
              <p class="text-muted small">Browse drives, apply, track your placement journey</p>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card shadow-sm p-4 text-center">
              <i class="bi bi-building text-success fs-1"></i>
              <h5 class="mt-2">For Companies</h5>
              <p class="text-muted small">Post drives, manage applicants, schedule exams</p>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card shadow-sm p-4 text-center">
              <i class="bi bi-shield-check text-danger fs-1"></i>
              <h5 class="mt-2">For Admin</h5>
              <p class="text-muted small">Oversee the entire placement process</p>
            </div>
          </div>
        </div>
        <router-link to="/register/student" class="btn btn-primary btn-lg me-3">Get Started as Student</router-link>
        <router-link to="/register/company" class="btn btn-outline-primary btn-lg">Register as Company</router-link>
      </div>
    </div>
  </div>
</template>
