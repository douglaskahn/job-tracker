# Job Application Tracker – Requirements

**Note**: This file documents the functional and technical requirements for the project.  
For Python dependencies, see `requirements.txt`.

## 1. Project Overview

The Job Application Tracker is a web-based system that helps users record, track, and manage their job search. Users can enter details about each application, upload associated documents, and monitor progress through various stages.

### Key Goals

- Track job application details and status
- Upload and view resume and cover letter files
- Search, filter, sort, and paginate applications
- Visualize progress through charts and a calendar view
- Provide a demo mode for showcasing the app with example data

---

## 2. Core Features

### 📝 Job Application Management (CRUD)

- Add, view, edit, and delete job applications
- Required fields: `company`, `role`, `status`
- Optional fields: `url`, `application_date`, `met_with`, `notes`, `resume_file`, `cover_letter_file`, `pros`, `cons`, `salary`, `follow_up_required`

### 📂 File Uploads

- Accepts `.pdf`, `.doc`, `.docx`, `.rtf`, `.txt` for `resume_file` and `cover_letter_file`
- Uploaded via `multipart/form-data`
- Stored in a server-side folder (e.g., `uploads/`)
- File paths saved in the database and linked in the UI
- **File Size Limits**: 5MB per file (enforced on both front end and back end)
- **Duplicate File Names**: Files will be renamed with a timestamp-based convention (e.g., `resume_acme_20250617.pdf`)
- **Validation**: MIME type and file extension validation will be enforced

### 📅 Date Handling

- Field: `application_date`
- Format: `YYYY-MM-DD`
- Optional for users; records without dates should appear at the end of date-based sorts
- Missing `application_date` values will remain blank and will not be defaulted
- Future support for tracking `status_change_date` for calendar visualization

---

## 3. API Requirements

### Endpoints

- `POST /applications/` – Create new application (multipart with file uploads)
- `GET /applications/` – List applications with query parameters for search, filter, sort, and pagination
- `GET /applications/{id}` – Retrieve full detail for a specific application
- `PUT /applications/{id}` – Update application data
- `DELETE /applications/{id}` – Delete an application

### Formats

- JSON for all text fields
- `multipart/form-data` when uploading files
- No authentication for MVP (to be added in future versions)

---

## 4. Front-End Requirements

### General UI

- Built with React and Material UI
- Responsive design for desktop, tablet, and mobile
- Skeleton loaders while data loads
- Toast notifications for success and error states

### Sidebar Navigation

- Persistent on desktop; toggleable/collapsible on smaller screens
- Items include:
  1. **Dashboard** – Main job application table view
  2. **Visualizations**
     - Applications Over Time 📈
     - Status Distribution 📊
     - Calendar View by Status Change Date 📅
  3. **Export CSV** 📤
  4. **Settings** ⚙️ *(includes Demo Data Toggle)*

- **Styling**:
  - Use MUI icons: `Dashboard`, `BarChart`, `CalendarMonth`, `Download`, `Settings`
  - Highlight active menu item with a distinct color or underline
  - Ensure collapsible behavior for smaller screens

### Job Table Design

- Use **MUI DataGrid** or similar table component with the following capabilities:
  - **Resizable Columns** – Users can adjust column widths
  - **Show/Hide Columns** – Users can customize which fields are shown
  - **Sortable Columns** – Including `company`, `role`, `status`, `application_date`, `follow_up_required`
  - **Filterable Columns** – Status dropdown, follow-up checkbox, etc.
  - **Paginated View** – 10 applications per page
  - **Sticky Header** – Table headers remain visible while scrolling
  - **Color-coded Rows by Status**:
    - See **Status-to-Color Mapping** below
  - **Follow-Up Indicator** – Small orange dot with glow when `follow_up_required = true`

### Demo Data Toggle

- **Purpose**: Populate the app with example/demo job applications for presentation purposes
- **Behavior**:
  - When toggled on, the app will display a predefined set of demo data
  - Demo data will not be saved to the database
  - All features (search, filter, visualizations) will work with demo data
- **Implementation**:
  - Use a local JSON file or mock API to provide demo data
  - Add a toggle button in the settings or sidebar

---

## 5. Database Requirements

### Table: `applications`

| Field                | Type     | Notes                              |
| -------------------- | -------- | ---------------------------------- |
| id                   | int      | Primary key, auto-increment        |
| company              | str      | Required                           |
| role                 | str      | Required                           |
| status               | str      | Required                           |
| url                  | str      | Optional                           |
| application\_date    | date     | Optional                           |
| met\_with            | str      | Optional                           |
| notes                | text     | Optional                           |
| pros                 | text     | Optional                           |
| cons                 | text     | Optional                           |
| salary               | str      | Optional                           |
| follow\_up\_required | bool     | Optional (default: false)          |
| resume\_file         | str      | Optional (stores filename or path) |
| cover\_letter\_file  | str      | Optional (stores filename or path) |
| created\_at          | datetime | Auto-generated                     |
| updated\_at          | datetime | Auto-managed                       |
| status\_change\_date | datetime | Tracks last status update          |

---

## 6. Status-to-Color Mapping

| Status                  | Color                |
| ----------------------- | -------------------- |
| Not Yet Applied         | White (gray border)  |
| Applied                 | Yellow              |
| Interviewing            | Orange              |
| Offer                  | Green               |
| Rejected                | Red                 |
| No Longer Listed        | Gray                |
| Decided not to apply    | Brown               |
| Declined Offer          | Black               |
| Accepted                | Dark Orange         |
| Applied / No Longer Listed | Light Gray         |

- Use Tailwind utility classes (e.g., `bg-red-500`, `bg-yellow-400`) or MUI theme tokens for consistent styling.
- Ensure charts, filters, and table rows reflect these colors.

---

## 7. Visualizations

### Features:

- 📈 **Applications Over Time**
  - Line or bar chart showing number of applications submitted over time.
  - Statuses represented with color or shape encoding.

- 🟠 **Status Distribution**
  - Pie or bar chart showing the proportion or count of applications in each status category.

- 🗓️ **Calendar View by Status Change Date**
  - Calendar interface that plots applications on the date their status last changed.
  - Hovering over a date shows application details.
  - Clicking on a calendar item can open its detail modal or navigate to the full application view.

### Technical Notes

- Frontend charting libraries under consideration: Chart.js, Recharts, or D3.js.
- FastAPI endpoints will return pre-aggregated data using `pandas`.

---

## 8. Future Enhancements

- 🔔 **Reminders & Calendar Integration** – Email notifications and reminders for follow-ups
- 🔍 **Job Listing URL Parsing** – Auto-extract `company` and `role` from pasted job links
- 👥 **Multi-user Support** – Logins and private job boards
- 📊 **Exports** – Export full application history to `.xlsx`

