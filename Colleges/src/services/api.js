import axios from 'axios';

// ============================================================
// AXIOS INSTANCE
// ============================================================

const API = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

// ============================================================
// REQUEST INTERCEPTOR
// ============================================================

API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// ============================================================
// RESPONSE INTERCEPTOR
// ============================================================

API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

export default API;

// ============================================================
// AUTH
// ============================================================

export const AuthAPI = {
  register: (data) => API.post('/auth/register', data),

  login: ({ email, password }) =>
    API.post(
      '/auth/token',
      new URLSearchParams({
        username: email,
        password,
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    ),

  me: () => API.get('/auth/me'),

  selectEstablishment: (establishmentId) =>
    API.post(`/auth/select-establishment/${establishmentId}`),

  acceptInvitation: (data) => API.post('/auth/accept-invitation', data),
};

// ============================================================
// ORGANIZATIONS
// ============================================================

export const OrganizationsAPI = {
  getAll: () => API.get('/organizations'),

  getById: (organizationId) => API.get(`/organizations/${organizationId}`),

  create: (data) => API.post('/organizations', data),

  update: (organizationId, data) => API.patch(`/organizations/${organizationId}`, data),

  remove: (organizationId) => API.delete(`/organizations/${organizationId}`),
};

// ============================================================
// SUBSCRIPTIONS
// ============================================================

export const SubscriptionsAPI = {
  getAll: (organizationId) => API.get(`/organizations/${organizationId}/subscriptions`),

  getById: (organizationId, subscriptionId) =>
    API.get(`/organizations/${organizationId}/subscriptions/${subscriptionId}`),

  create: (organizationId, data) =>
    API.post(`/organizations/${organizationId}/subscriptions`, data),

  update: (organizationId, subscriptionId, data) =>
    API.patch(`/organizations/${organizationId}/subscriptions/${subscriptionId}`, data),

  remove: (organizationId, subscriptionId) =>
    API.delete(`/organizations/${organizationId}/subscriptions/${subscriptionId}`),
};

// ============================================================
// ESTABLISHMENTS
// ============================================================

export const EstablishmentsAPI = {
  getAll: (organizationId) => API.get(`/organizations/${organizationId}/establishments`),

  getById: (organizationId, establishmentId) =>
    API.get(`/organizations/${organizationId}/establishments/${establishmentId}`),

  create: (organizationId, data) =>
    API.post(`/organizations/${organizationId}/establishments`, data),

  update: (organizationId, establishmentId, data) =>
    API.patch(`/organizations/${organizationId}/establishments/${establishmentId}`, data),

  remove: (organizationId, establishmentId) =>
    API.delete(`/organizations/${organizationId}/establishments/${establishmentId}`),
};

// ============================================================
// ONBOARDING
// ============================================================

export const OnboardingAPI = {
  submitRequest: (data) => API.post('/onboarding/requests', data),

  listPending: () => API.get('/onboarding/requests/pending'),

  approve: (requestId) => API.post(`/onboarding/requests/${requestId}/approve`),

  reject: (requestId) => API.post(`/onboarding/requests/${requestId}/reject`),
};

// ============================================================
// USERS
// ============================================================

export const UsersAPI = {
  getAll: (establishmentId) => API.get(`/establishments/${establishmentId}/users`),

  getById: (establishmentId, userId) =>
    API.get(`/establishments/${establishmentId}/users/${userId}`),

  create: (establishmentId, data) => API.post(`/establishments/${establishmentId}/users`, data),

  update: (establishmentId, userId, data) =>
    API.patch(`/establishments/${establishmentId}/users/${userId}`, data),

  remove: (establishmentId, userId) =>
    API.delete(`/establishments/${establishmentId}/users/${userId}`),
};

// ============================================================
// ROLES
// ============================================================

export const RolesAPI = {
  getAll: (establishmentId) => API.get(`/establishments/${establishmentId}/roles`),

  getById: (establishmentId, roleId) =>
    API.get(`/establishments/${establishmentId}/roles/${roleId}`),

  create: (establishmentId, data) => API.post(`/establishments/${establishmentId}/roles`, data),

  update: (establishmentId, roleId, data) =>
    API.patch(`/establishments/${establishmentId}/roles/${roleId}`, data),

  remove: (establishmentId, roleId) =>
    API.delete(`/establishments/${establishmentId}/roles/${roleId}`),

  syncAdminPermissions: () => API.post('/establishments/sync-establishment-admin-permissions'),
};

// ============================================================
// USER ROLES
// ============================================================

export const UserRolesAPI = {
  listUserRoles: (establishmentId, userId) =>
    API.get(`/establishments/${establishmentId}/users/${userId}/roles`),

  assign: (establishmentId, userId, roleId) =>
    API.post(`/establishments/${establishmentId}/users/${userId}/roles/${roleId}`),

  remove: (establishmentId, userId, roleId) =>
    API.delete(`/establishments/${establishmentId}/users/${userId}/roles/${roleId}`),
};

// ============================================================
// ROLE PERMISSIONS
// ============================================================

export const RolePermissionsAPI = {
  listRolePermissions: (establishmentId, roleId) =>
    API.get(`/establishments/${establishmentId}/roles/${roleId}/permissions`),

  assign: (establishmentId, roleId, permissionId) =>
    API.post(`/establishments/${establishmentId}/roles/${roleId}/permissions/${permissionId}`),

  remove: (establishmentId, roleId, permissionId) =>
    API.delete(`/establishments/${establishmentId}/roles/${roleId}/permissions/${permissionId}`),
};

// ============================================================
// ACADEMIC YEARS
// ============================================================

export const AcademicYearsAPI = {
  getAll: (establishmentId) => API.get(`/establishments/${establishmentId}/academic-years`),

  getById: (establishmentId, academicYearId) =>
    API.get(`/establishments/${establishmentId}/academic-years/${academicYearId}`),

  create: (establishmentId, data) =>
    API.post(`/establishments/${establishmentId}/academic-years`, data),

  update: (establishmentId, academicYearId, data) =>
    API.patch(`/establishments/${establishmentId}/academic-years/${academicYearId}`, data),

  remove: (establishmentId, academicYearId) =>
    API.delete(`/establishments/${establishmentId}/academic-years/${academicYearId}`),
};

// ============================================================
// LEVELS
// ============================================================

export const LevelsAPI = {
  getAll: () => API.get('/levels'),

  getById: (levelId) => API.get(`/levels/${levelId}`),

  create: (data) => API.post('/levels', data),

  update: (levelId, data) => API.patch(`/levels/${levelId}`, data),

  remove: (levelId) => API.delete(`/levels/${levelId}`),
};

// ============================================================
// CLASSES
// ============================================================

export const ClassesAPI = {
  getAll: (establishmentId) => API.get(`/establishments/${establishmentId}/classes`),

  getById: (establishmentId, classId) =>
    API.get(`/establishments/${establishmentId}/classes/${classId}`),

  create: (establishmentId, data) => API.post(`/establishments/${establishmentId}/classes`, data),

  update: (establishmentId, classId, data) =>
    API.patch(`/establishments/${establishmentId}/classes/${classId}`, data),

  remove: (establishmentId, classId) =>
    API.delete(`/establishments/${establishmentId}/classes/${classId}`),
};

// ============================================================
// STUDENTS
// ============================================================

export const StudentsAPI = {
  getAll: (establishmentId) => API.get(`/establishments/${establishmentId}/students`),

  getById: (establishmentId, studentId) =>
    API.get(`/establishments/${establishmentId}/students/${studentId}`),

  create: (establishmentId, data) => API.post(`/establishments/${establishmentId}/students`, data),

  update: (establishmentId, studentId, data) =>
    API.patch(`/establishments/${establishmentId}/students/${studentId}`, data),

  remove: (establishmentId, studentId) =>
    API.delete(`/establishments/${establishmentId}/students/${studentId}`),
};

// ============================================================
// GUARDIANS
// ============================================================

export const GuardiansAPI = {
  getAll: (establishmentId) => API.get(`/establishments/${establishmentId}/guardians`),

  getById: (establishmentId, guardianId) =>
    API.get(`/establishments/${establishmentId}/guardians/${guardianId}`),

  create: (establishmentId, data) => API.post(`/establishments/${establishmentId}/guardians`, data),

  update: (establishmentId, guardianId, data) =>
    API.patch(`/establishments/${establishmentId}/guardians/${guardianId}`, data),

  remove: (establishmentId, guardianId) =>
    API.delete(`/establishments/${establishmentId}/guardians/${guardianId}`),
};

// ============================================================
// STUDENT GUARDIANS
// ============================================================

export const StudentGuardiansAPI = {
  createLink: (establishmentId, studentId, data) =>
    API.post(`/establishments/${establishmentId}/students/${studentId}/guardians`, data),

  listGuardians: (establishmentId, studentId) =>
    API.get(`/establishments/${establishmentId}/students/${studentId}/guardians`),

  deleteLink: (establishmentId, studentId, guardianId) =>
    API.delete(`/establishments/${establishmentId}/students/${studentId}/guardians/${guardianId}`),
};

// ============================================================
// ENROLLMENTS
// ============================================================

export const EnrollmentsAPI = {
  getAll: (establishmentId) => API.get(`/establishments/${establishmentId}/enrollments`),

  getById: (establishmentId, enrollmentId) =>
    API.get(`/establishments/${establishmentId}/enrollments/${enrollmentId}`),

  create: (establishmentId, data) =>
    API.post(`/establishments/${establishmentId}/enrollments`, data),

  update: (establishmentId, enrollmentId, data) =>
    API.patch(`/establishments/${establishmentId}/enrollments/${enrollmentId}`, data),

  remove: (establishmentId, enrollmentId) =>
    API.delete(`/establishments/${establishmentId}/enrollments/${enrollmentId}`),
};

// ============================================================
// SUBJECTS
// ============================================================

export const SubjectsAPI = {
  getAll: () => API.get('/subjects'),

  getById: (subjectId) => API.get(`/subjects/${subjectId}`),

  create: (data) => API.post('/subjects', data),

  update: (subjectId, data) => API.patch(`/subjects/${subjectId}`, data),

  remove: (subjectId) => API.delete(`/subjects/${subjectId}`),
};

// ============================================================
// CURRICULUMS
// ============================================================

export const CurriculumsAPI = {
  getAll: (establishmentId) => API.get(`/establishments/${establishmentId}/curriculums`),

  getById: (establishmentId, curriculumId) =>
    API.get(`/establishments/${establishmentId}/curriculums/${curriculumId}`),

  create: (establishmentId, data) =>
    API.post(`/establishments/${establishmentId}/curriculums`, data),

  update: (establishmentId, curriculumId, data) =>
    API.patch(`/establishments/${establishmentId}/curriculums/${curriculumId}`, data),

  remove: (establishmentId, curriculumId) =>
    API.delete(`/establishments/${establishmentId}/curriculums/${curriculumId}`),
};

// ============================================================
// CLASS CURRICULUM
// ============================================================

export const ClassCurriculumAPI = {
  get: (establishmentId, classId) =>
    API.get(`/establishments/${establishmentId}/classes/${classId}/curriculum`),

  assign: (establishmentId, classId, curriculumId) =>
    API.post(`/establishments/${establishmentId}/classes/${classId}/curriculum/${curriculumId}`),

  remove: (establishmentId, classId) =>
    API.delete(`/establishments/${establishmentId}/classes/${classId}/curriculum`),
};

// ============================================================
// CURRICULUM SUBJECTS
// ============================================================

export const CurriculumSubjectsAPI = {
  listCurriculumSubjects: (establishmentId, curriculumId) =>
    API.get(`/establishments/${establishmentId}/curriculums/${curriculumId}/subjects`),

  addSubject: (establishmentId, curriculumId, subjectId, data) =>
    API.post(
      `/establishments/${establishmentId}/curriculums/${curriculumId}/subjects/${subjectId}`,
      data
    ),

  removeSubject: (establishmentId, curriculumId, subjectId) =>
    API.delete(
      `/establishments/${establishmentId}/curriculums/${curriculumId}/subjects/${subjectId}`
    ),
};

// ============================================================
// TEACHER ASSIGNMENTS
// ============================================================

export const TeacherAssignmentsAPI = {
  assignTeacher: (establishmentId, classId, curriculumSubjectId, userId) =>
    API.post(
      `/establishments/${establishmentId}/classes/${classId}/curriculum-subjects/${curriculumSubjectId}/teachers/${userId}`
    ),

  listClassAssignments: (establishmentId, classId) =>
    API.get(`/establishments/${establishmentId}/classes/${classId}/teacher-assignments`),

  listTeacherAssignments: (establishmentId, userId) =>
    API.get(`/establishments/${establishmentId}/teachers/${userId}/assignments`),

  remove: (establishmentId, assignmentId) =>
    API.delete(`/establishments/${establishmentId}/teacher-assignments/${assignmentId}`),
};

// ============================================================
// ATTENDANCE
// ============================================================

export const AttendanceAPI = {
  create: (establishmentId, data) =>
    API.post(`/establishments/${establishmentId}/attendance`, data),

  getByClass: (establishmentId, classId, attendanceDate) =>
    API.get(`/establishments/${establishmentId}/classes/${classId}/attendance`, {
      params: attendanceDate ? { attendance_date: attendanceDate } : undefined,
    }),

  getByStudent: (establishmentId, studentId) =>
    API.get(`/establishments/${establishmentId}/students/${studentId}/attendance`),

  getById: (establishmentId, attendanceId) =>
    API.get(`/establishments/${establishmentId}/attendance/${attendanceId}`),

  update: (establishmentId, attendanceId, data) =>
    API.patch(`/establishments/${establishmentId}/attendance/${attendanceId}`, data),

  remove: (establishmentId, attendanceId) =>
    API.delete(`/establishments/${establishmentId}/attendance/${attendanceId}`),
};

// ============================================================
// EVALUATIONS
// ============================================================

export const EvaluationsAPI = {
  create: (establishmentId, data) =>
    API.post(`/establishments/${establishmentId}/evaluations`, data),

  getByClass: (establishmentId, classId, period) =>
    API.get(`/establishments/${establishmentId}/classes/${classId}/evaluations`, {
      params: period ? { period } : undefined,
    }),

  getById: (establishmentId, evaluationId) =>
    API.get(`/establishments/${establishmentId}/evaluations/${evaluationId}`),

  remove: (establishmentId, evaluationId) =>
    API.delete(`/establishments/${establishmentId}/evaluations/${evaluationId}`),
};

// ============================================================
// GRADES
// ============================================================

export const GradesAPI = {
  create: (establishmentId, data) => API.post(`/establishments/${establishmentId}/grades`, data),

  getByEvaluation: (establishmentId, evaluationId) =>
    API.get(`/establishments/${establishmentId}/evaluations/${evaluationId}/grades`),

  getByStudent: (establishmentId, studentId) =>
    API.get(`/establishments/${establishmentId}/students/${studentId}/grades`),

  getById: (establishmentId, gradeId) =>
    API.get(`/establishments/${establishmentId}/grades/${gradeId}`),

  update: (establishmentId, gradeId, data) =>
    API.patch(`/establishments/${establishmentId}/grades/${gradeId}`, data),

  remove: (establishmentId, gradeId) =>
    API.delete(`/establishments/${establishmentId}/grades/${gradeId}`),
};

// ============================================================
// REPORT CARDS
// ============================================================

export const ReportCardsAPI = {
  create: (establishmentId, data) =>
    API.post(`/establishments/${establishmentId}/report-cards`, data),

  getById: (establishmentId, reportCardId) =>
    API.get(`/establishments/${establishmentId}/report-cards/${reportCardId}`),

  getByStudent: (establishmentId, studentId, academicYearId) =>
    API.get(`/establishments/${establishmentId}/students/${studentId}/report-cards`, {
      params: {
        academic_year_id: academicYearId,
      },
    }),
};

// ============================================================
// FEE TYPES
// ============================================================

export const FeeTypesAPI = {
  getAll: (establishmentId) => API.get(`/establishments/${establishmentId}/fee-types`),

  getById: (establishmentId, feeTypeId) =>
    API.get(`/establishments/${establishmentId}/fee-types/${feeTypeId}`),

  create: (establishmentId, data) => API.post(`/establishments/${establishmentId}/fee-types`, data),

  update: (establishmentId, feeTypeId, data) =>
    API.patch(`/establishments/${establishmentId}/fee-types/${feeTypeId}`, data),

  remove: (establishmentId, feeTypeId) =>
    API.delete(`/establishments/${establishmentId}/fee-types/${feeTypeId}`),
};

// ============================================================
// PAYMENTS
// ============================================================

export const PaymentsAPI = {
  create: (establishmentId, data) => API.post(`/establishments/${establishmentId}/payments`, data),

  getById: (establishmentId, paymentId) =>
    API.get(`/establishments/${establishmentId}/payments/${paymentId}`),

  remove: (establishmentId, paymentId) =>
    API.delete(`/establishments/${establishmentId}/payments/${paymentId}`),

  getByStudent: (establishmentId, studentId) =>
    API.get(`/establishments/${establishmentId}/students/${studentId}/payments`),

  getByFeeType: (establishmentId, feeTypeId) =>
    API.get(`/establishments/${establishmentId}/fee-types/${feeTypeId}/payments`),

  getFinancialSummary: (establishmentId, studentId) =>
    API.get(`/establishments/${establishmentId}/students/${studentId}/financial-summary`),
};

// ============================================================
// RECEIPTS
// ============================================================

export const ReceiptsAPI = {
  create: (establishmentId, data) => API.post(`/establishments/${establishmentId}/receipts`, data),

  getById: (establishmentId, receiptId) =>
    API.get(`/establishments/${establishmentId}/receipts/${receiptId}`),

  getByPayment: (establishmentId, paymentId) =>
    API.get(`/establishments/${establishmentId}/payments/${paymentId}/receipt`),

  remove: (establishmentId, receiptId) =>
    API.delete(`/establishments/${establishmentId}/receipts/${receiptId}`),
};

// ============================================================
// DASHBOARD
// ============================================================

export const DashboardAPI = {
  getEstablishmentDashboard: (establishmentId) =>
    API.get(`/establishments/${establishmentId}/dashboard`),

  getTeacherDashboard: (establishmentId, teacherId) =>
    API.get(`/establishments/${establishmentId}/teachers/${teacherId}/dashboard`),
};
