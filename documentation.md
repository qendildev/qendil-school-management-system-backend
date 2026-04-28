# Qendil School Management System Documentation

Welcome to the full documentation of the Qendil School Management System. This guide provides a comprehensive overview of how to use the system, starting from registration to managing various school operations.

---

## 1. Developer & Testing Tools

To explore and test the API, the frontend team can use the following built-in and external tools:

### Interactive API Documentation (Swagger)
The system comes with built-in interactive API documentation. This allows you to explore all available endpoints, see required parameters, and test requests directly.
- **Swagger UI**: `https://qendil-backend.onrender.com/api/docs/`
- **API Schema**: `https://qendil-backend.onrender.com/api/schema/`

### Testing with Postman / Insomnia
For testing outside of Swagger:
1.  **Authorization**: Set the type to `Bearer Token`.
2.  **Token**: Paste the `access` token received from the login endpoint.
3.  **Headers**: Ensure `Content-Type: application/json` is set.

---

## 2. Frontend Integration Guide (JWT Authentication)

The system uses JSON Web Tokens (JWT) for secure authentication. 

### Authentication Flow
1.  **Login**: Send a `POST` request to `/api/v1/auth/login/` with `email` (or `username`) and `password`.
2.  **Tokens**: On success, the backend returns:
    - `access`: Short-lived token for authenticated requests.
    - `refresh`: Longer-lived token to regenerate the access token.
3.  **Storage**: The frontend should store these tokens (e.g., in `localStorage`, `sessionStorage`, or secure HttpOnly cookies).
4.  **Authenticated Requests**: For every subsequent request to a protected endpoint (e.g., dashboard, profiles), include the access token in the header:
    ```http
    Authorization: Bearer <your_access_token>
    ```

### Handling Token Expiration
- If a request returns a **401 Unauthorized** error, it means the `access` token has expired.
- Use the `refresh` token to call `/api/v1/auth/token/refresh/` to get a new `access` token without forcing the user to log in again.

---

## 3. Getting Started: Registration & Roles

The system uses a secure authentication system based on JWT (JSON Web Tokens).

### User Registration
- **Role-Based Registration**: Users can register with roles such as `student`, `teacher`, `admin`, or `parent`.
- **Fields Required**: Email, Username, Password, First Name, and Last Name.
- **Process**:
    1. Navigate to the registration page.
    2. Fill in the required details and select your role.
    3. Upon successful registration, you can log in to the system.

### Login & Security
- **Secure Login**: Use your email/username and password to obtain an access token.
- **JWT Tokens**: Upon successful login, the system returns an `access` and `refresh` token.
    - `access`: Used for authenticating requests (shorter lifespan).
    - `refresh`: Used to obtain a new access token when it expires.
- **How to Use Tokens**: For every authenticated request, include the access token in the header:
    ```http
    Authorization: Bearer <your_access_token>
    ```
- **Profile Management**: Once logged in, users can view and update their profile information (name, phone, avatar).
- **Password Recovery**: If you forget your password, use the "Forgot Password" feature to receive a reset link via email.

---

## 2. Dashboard Access

After logging in, you can access your role-specific dashboard. Based on your role, you should navigate to:

- **Admin Dashboard**: `/api/v1/dashboard/admin/`
- **Teacher Dashboard**: `/api/v1/dashboard/teacher/`
- **Student Dashboard**: `/api/v1/dashboard/student/`
- **Parent Dashboard**: `/api/v1/dashboard/parent/`
- **Accountant Dashboard**: `/api/v1/dashboard/accountant/`

These dashboards provide a summary of relevant statistics and quick actions.

---

## 2. Admission Management

Before a student is officially enrolled, they go through the Admission module.

- **Admission Request**: Prospective students or parents can submit an admission form with personal details, previous school history, and documents.
- **Review Process**: Admins can review pending admissions, approve them, or reject them.
- **Conversion**: Approved admissions can be "Converted to Student," which automatically creates a student profile and links it to a user account.

---

## 3. Student Management

The core of the system is the Student module.

- **Student Profiles**: Detailed profiles including admission number, roll number, date of birth, address, and medical records.
- **Academic History**: Tracks previous schools and grades completed.
- **Documents**: Store and manage student documents like birth certificates, previous transcripts, etc.
- **Health Records**: Track student height, weight, allergies, and medical history.

---

## 4. Staff & Teacher Management

Manage your school's employees and teaching staff.

- **Departments**: Organize staff into departments (e.g., Mathematics, Science, Administration).
- **Staff Profiles**: Comprehensive details including designation, joining date, qualifications, and experience.
- **Payroll**: Manage monthly salaries, allowances, deductions, and payment status for all staff members.

---

## 5. Academic Management (Classes, Subjects, Sections)

Organize your school's structure and curriculum.

- **Classes & Sections**: Create classes (e.g., Grade 1, Grade 2) and divide them into sections (e.g., Section A, Section B).
- **Subject Management**: Define subjects (Theory/Practical) and assign codes.
- **Subject Teachers**: Assign specific teachers to subjects within a particular class and section.
- **Curriculum**: Upload and manage lesson plans, syllabi, and study materials for each subject.

---

## 6. Operational Systems

### Attendance Tracking
- **Student Attendance**: Mark daily attendance for students in each section.
- **Staff Attendance**: Track the presence of teachers and administrative staff.

### Fee Management
- **Fee Categories**: Define different types of fees (Tuition, Transport, Library).
- **Fee Structure**: Set up fee amounts for different classes and academic years.
- **Payments**: Record payments made by students, track installments, and issue receipts.

### Homework & Assignments
- Teachers can create homework assignments for their classes.
- Students can view and submit their work through the system.

---

## 7. Support & Communication

- **Library Management**: Track books, issues, and returns.
- **Notices & Events**: Publish school-wide notices and manage upcoming events on the calendar.
- **Discipline Tracking**: Record and monitor student disciplinary actions.
- **Activity Logs**: Admins can monitor system activities for security and auditing purposes.

---

## 8. Full System Flow Summary

1.  **Setup**: Admin sets up Academic Years, Classes, Sections, and Subjects.
2.  **Staff Onboarding**: Admin registers teachers and staff, assigning them to departments.
3.  **Admissions**: Parents/Students apply; Admin reviews and approves.
4.  **Enrollment**: Approved applicants are converted to Students and assigned to a Class/Section.
5.  **Daily Operations**:
    - Teachers mark attendance and upload curriculum materials.
    - Teachers assign homework.
    - Fee department manages student payments.
6.  **Monitoring**: Admins use the Dashboard and Activity Logs to oversee the entire school ecosystem.

---

*This documentation is designed to help you navigate and utilize the Qendil School Management System effectively. For specific API technical details, please refer to the API endpoint documentation.*
