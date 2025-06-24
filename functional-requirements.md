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
  - **Show/Hide Columns**: Users can customize which fields are shown in the table.
  - **Resizable Columns**: Users can adjust column widths.
  - **Sortable Columns**: All key fields, including `company`, `role`, `status`, `application_date`, `follow_up_required`.
  - **Filterable Columns**: Status dropdown, follow-up checkbox, etc.
  - **Search Bar**: Live search that filters content as you type.
  - **Sticky Header**: Table headers remain visible while scrolling.
  - **Follow-Up Indicator**: Orange dot with glow for follow-up-required rows.

### Modals & Detail Views

- **View Modal:** Clicking “View” opens a modal with full application details, including file links.
- **Edit in Modal:** Users can edit all fields directly in the modal.
- **Delete in Modal:** Users can delete a record from the modal, with a confirmation prompt.
- **Logs/History:** Modal includes a "Logs" section showing all changes in status, create date, application date, etc.
- **Show All Modal/View:** Button to display all records at once in a modal or expanded view.

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

### High Priority
- **Accessibility & Usability:** Keyboard navigation, screen reader support, aria-labels, and focus states for all controls. (Required for multi-user/public release.)
- **Mobile Responsiveness:** 
  - Mobile-optimized table/list view
  - Touch-friendly forms and modals
  - Responsive navigation
  - Cross-device testing
  - Estimated effort: 4-7 days

### Medium Priority
- **Bulk Actions**
- **Reminders & Calendar Integration**
- **Job Listing URL Parsing**
- **Multi-user Support**
- **Audit Trail/Change Log**

### Lower Priority
- **Column Customization Persistence**
- **API Security**
- **Native Mobile Apps** (iOS/Android)
  - Consider React Native for initial mobile app
  - Evaluate native Swift development based on usage
  - Requires separate mobile development effort

---

## Frontend Setup

- **Framework:** Use [Vite](https://vitejs.dev/) for all React frontend development.
- **Rationale:** Create React App is deprecated and no longer maintained. Vite offers faster development, modern tooling, and better long-term support.

- **Initial Setup (for new contributors):**
  ```bash
  npm create vite@latest frontend -- --template react
  cd frontend
  npm install
  npm install @mui/material @mui/icons-material @mui/x-data-grid axios
  ```

- **Note:**  
  The frontend has already been initialized and dependencies installed in this repository.  
  New contributors should only run the above commands if setting up the project from scratch.

- **Dependencies:**  
  - `@mui/material`  
  - `@mui/icons-material`  
  - `@mui/x-data-grid`  
  - `axios`
- **Do not use Create React App for new projects.**

## Vite + React Project Best Practices

- All React source code should be in the `src/` directory.
- The entry point should be `src/main.jsx`.
- The main component should be `src/App.jsx`.
- `index.html` should be at the project root and reference `/src/main.jsx`.
- Only configuration, public, and node_modules folders should be at the root.
- Use only one version of React and ReactDOM.
- Use the official `@vitejs/plugin-react` for Vite + React projects.
- Do not manually edit `package-lock.json`—let npm manage it.
- After changing dependencies, always delete `node_modules` and `package-lock.json` and run `npm install`.
- For MUI, always install `@emotion/react` and `@emotion/styled` as peer dependencies.
- If you see errors like `import_react3` or blank screens, always:
  1. Delete `node_modules` and `package-lock.json`.
  2. Run `npm install`.
  3. Check for duplicate or mismatched React versions.
  4. Ensure all file paths in imports and `index.html` are correct.
- After updating dependencies, always restart the dev server.

---

## Frontend File Structure & Import Conventions

- All React source code is in the `frontend/src/` directory.
- Main entry point: `src/main.jsx` (referenced in `index.html`)
- Main app component: `src/App.jsx`
- Pages: `src/pages/` (e.g., `Dashboard.jsx`, `VisualizationsPage.jsx`, `Settings.jsx`, `ExportCSV.jsx`, `Calendar.jsx`)
- Components: `src/` (e.g., `Sidebar.jsx`, `JobTable.jsx`, `ApplicationForm.jsx`, `Visualizations.jsx`, etc.)
- Use relative imports within `src/` (e.g., `import Sidebar from './Sidebar'`)
- Do not use absolute imports or paths outside `src/` for React code.
- All new pages/components should be placed in `src/pages/` or `src/` as appropriate.

## Troubleshooting Broken Imports or Blank Screens

- If you see blank screens or import errors:
  1. Check that all import paths match the file structure and use relative paths.
  2. Ensure all files referenced in imports exist in the correct location.
  3. Do not manually edit `package-lock.json`. If you did, delete `node_modules` and `package-lock.json`, then run `npm install`.
  4. Ensure only one version of React and ReactDOM is installed.
  5. Restart the Vite dev server after any dependency or file structure changes.
  6. For MUI, ensure `@emotion/react` and `@emotion/styled` are installed.
  7. For charts, install `chart.js` and `react-chartjs-2`.

---

## 10. Local Development & Configuration Notes

### FastAPI Backend
- **CORS:** Ensure `allow_origins` in CORS middleware includes your frontend dev URL (e.g., `http://localhost:5173`).
- **Database:** Uses a local SQLite file (e.g., `jobtracker.db`). Path is relative to the project root. To reset, delete the file and restart the backend.
  
  **Important Database Notes:**
  - Multiple database files may exist:
    - `/jobtracker.db` - Main application database
    - `/frontend/jobtracker.db` - Development database used by frontend
    - Files with spaces (e.g., `jobtracker 2.db`) should be avoided
  - Database file permissions:
    - Ensure read/write permissions for the application user
    - For development: `chmod 666 jobtracker.db`
    - For production: proper file permissions based on deployment user
  - SQLite access:
    - Use absolute paths when accessing via command line
    - Example: `sqlite3 "/full/path/to/jobtracker.db"`
    - Always use proper quoting for paths with spaces
  - Database synchronization:
    - Frontend and backend may have separate database files during development
    - Document which database file is authoritative
    - Consider adding database path to configuration

- **Uploads:** Uploaded files are saved to the `uploads/` directory. Ensure this folder exists and is writable.
- **Environment Variables:** If any secrets, API keys, or config values are needed, document them and use a `.env` file (with `python-dotenv` if needed).
- **Port:** Backend runs on port `8000` by default. Change with the `--port` flag if needed.

### React Frontend
- **API Base URL:** All API calls should point to the backend dev server (e.g., `http://localhost:8000`). This is set in `frontend/src/api.js`.
- **Port:** Frontend runs on port `5173` by default (Vite). Change with the `--port` flag if needed.
- **Proxy (optional):** If using a Vite proxy for API calls, document the config in `vite.config.js`.

### General
- **Dependencies:** Install Python and Node dependencies with `pip install -r requirements.txt` and `npm install`.
- **Dev Scripts:** Start backend with `uvicorn app.main:app --reload` and frontend with `npm run dev` from the `frontend/` folder.
- **File Upload Limits:** Max file size is 5MB per file. Allowed types: `.pdf`, `.doc`, `.docx`, `.rtf`, `.txt`.
- **Demo Mode:** Demo data endpoints are available at `/demo/applications/`.
- **Resetting State:** To clear the database, delete `jobtracker.db`. To clear uploads, delete files in `uploads/`.

---

## 11. Clarifications & Future Enhancements

- **Notifications/Reminders:** Not required for MVP; mark as "Future Enhancement."
- **User Accounts:** Not required for MVP; mark as "Future Enhancement."
- **Accessibility:** Not a current focus for MVP.
- **Audit Trail:** Not required for MVP. For future: consider tracking changes to applications (who/when/what changed), e.g., a simple change log per application, viewable in the modal.
- **Error Handling:** All user-facing errors and confirmations should use toast/snackbar feedback.
- **Column Customization Persistence:** Not required for MVP; "Saved Views" can be a future enhancement.
- **File Download/View:** Uploaded resume and cover letter should appear as "See Resume" and "See Cover Letter" links in the modal and/or table if present.
- **API Security:** No API keys or rate limiting for MVP. CORS enabled for local dev. Note future need for token-based auth if multi-user or public.

### Known Technical Limitations

#### Spreadsheet Import Sorting
The current implementation relies on checking for a specific `created_at` timestamp ("2025-06-20T02:58:17") to identify records from the initial spreadsheet import. This approach has several limitations:

1. **Scalability Issues:**
   - Won't work for multiple imports (each would need its own timestamp check)
   - Requires modifying code for each new import
   - Hard-coded timestamp creates technical debt

2. **Recommended Future Solution:**
   - Add an `import_batch_id` column to the database
   - When importing, generate a unique batch ID
   - Store the original row order as `import_order` within each batch
   - Sort using these dedicated fields instead of timestamp checks
   - This approach will scale to multiple imports and maintain proper ordering

Example Schema Update:
```sql
ALTER TABLE applications ADD COLUMN import_batch_id VARCHAR(36);
ALTER TABLE applications ADD COLUMN import_order INTEGER;
```

This would allow for proper sorting regardless of import time and support multiple imports while maintaining original order within each import batch.

---

## 12. API Design Patterns & Data Updates

### Separation of Concerns

The API follows these patterns for cleaner, more maintainable code:

1. **Data Updates vs File Uploads**
   - Data updates use JSON endpoints (PATCH /applications/{id})
   - File uploads use dedicated multipart/form-data endpoints (POST /applications/{id}/files)
   - This separation simplifies validation and error handling

2. **Endpoint Structure**
```
PATCH /applications/{id}
  - Updates application data
  - Accepts JSON body
  - Returns updated application

POST /applications/{id}/files/{type}
  - Handles file uploads (resume/cover letter)
  - Accepts multipart/form-data
  - Returns file metadata
```

3. **Empty Field Handling**
   - NULL values in database represent unset fields
   - Empty strings in requests clear fields (set to NULL)
   - Required fields cannot be cleared
   - Optional fields can be explicitly cleared by sending null or empty string

Example Update Request:
```json
PATCH /applications/123
{
  "salary": null,        // Clear the salary field
  "notes": "",          // Clear the notes field
  "company": "Acme",    // Update required field
  "pros": "Great team"  // Update optional field
}
```

This design:
- Separates data concerns from file handling
- Makes validation more straightforward
- Provides clear semantics for field updates
- Reduces complexity in state management
- Follows REST best practices

---

## Mobile Responsiveness Requirements

### Current Mobile Support
- Material-UI responsive components
- Collapsible sidebar for small screens
- Responsive grid layout
- Flexible container widths

### Mobile Enhancements Needed
1. **Table/List View**
   - Card view for mobile screens
   - Horizontal scrolling for table mode
   - Touch-friendly controls
   - Optimized column visibility defaults

2. **Navigation**
   - Bottom navigation bar for mobile
   - Swipe gestures for common actions
   - Quick action FAB (Floating Action Button)
   - Compact header design

3. **Forms and Modals**
   - Full-screen modals on mobile
   - Native file picker integration
   - Touch-friendly form controls
   - Keyboard avoidance for inputs

4. **Performance**
   - Image optimization for mobile
   - Lazy loading for long lists
   - Mobile-specific bundle optimization
   - Offline support consideration

5. **Testing Requirements**
   - Test on iOS/Android devices
   - Test on various screen sizes
   - Touch interaction testing
   - Mobile network conditions testing

---

## Mobile Responsiveness Implementation Plan

### Phase 1: Core Mobile Updates (1-2 Days)
1. **Table/List View**
   ```jsx
   // JobTable.jsx
   const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
   
   return isMobile ? (
     <MobileJobList items={rows} onView={handleView} />
   ) : (
     <DataGrid {...props} />
   );
   ```
   - Create mobile card view component
   - Implement touch-friendly sorting
   - Add pull-to-refresh
   - Optimize for small screens

2. **Form/Modal Updates**
   ```jsx
   // ApplicationViewModal.jsx
   const fullScreen = useMediaQuery(theme.breakpoints.down('sm'));
   
   <Dialog
     fullScreen={fullScreen}
     {...props}
   >
   ```
   - Full-screen modals on mobile
   - Touch-optimized form controls
   - Mobile-friendly file upload
   - Bottom sheet for actions

### Phase 2: Navigation & Layout (2-3 Days)
1. **Mobile Navigation**
   ```jsx
   // App.jsx
   const MobileNav = () => (
     <BottomNavigation>
       <BottomNavigationAction label="Jobs" icon={<WorkIcon />} />
       <BottomNavigationAction label="Add" icon={<AddIcon />} />
       <BottomNavigationAction label="Stats" icon={<ChartIcon />} />
     </BottomNavigation>
   );
   ```
   - Bottom navigation bar
   - Floating action button for new applications
   - Swipe gestures for common actions

2. **Responsive Layout**
   - Adjust padding/margins for mobile
   - Optimize touch targets
   - Improve table/list spacing
   - Add mobile-specific animations

### Phase 3: Polish & Testing (1-2 Days)
1. **Performance**
   - Lazy loading for long lists
   - Image/asset optimization
   - Touch feedback improvements

2. **Testing**
   - Cross-device testing
   - Touch interaction testing
   - Responsive layout validation
   - Performance benchmarking

Total Effort: 4-7 Days

### Implementation Notes
1. Use existing MUI components where possible
2. Leverage CSS Grid/Flexbox for layouts
3. Follow iOS/Android touch guidelines
4. Test on actual devices, not just emulators
5. Consider slow network conditions
6. Ensure keyboard accessibility remains

### Success Metrics
1. Smooth scrolling (60fps)
2. Sub-100ms touch response
3. Proper rendering across devices
4. No horizontal scrolling
5. All features accessible on mobile

This plan focuses on making the web app mobile-friendly without creating a native app, using our existing React/MUI stack.

---

## iOS Mobile App Requirements

### Architecture Options

1. **React Native Approach**
   - Leverages existing React/JavaScript codebase
   - Estimated 60-70% code reuse from web version
   - Same tech stack (JavaScript/React)
   - Requires minimal team retraining
   
   **Components to Reuse:**
   - Data models and validation logic
   - API integration code
   - State management
   - Business logic
   - Form handling
   
   **New Components Needed:**
   - Native navigation
   - Mobile-specific UI components
   - Device API integration
   - Offline storage logic

2. **Native Swift Approach**
   - Complete separate codebase
   - Native iOS development
   - Requires iOS development expertise
   - Higher performance and better iOS integration
   
   **New Development Required:**
   - Complete UI rebuild in SwiftUI
   - New data layer in Swift
   - New API client implementation
   - New state management solution
   - All business logic reimplemented

### Implementation Complexity Analysis

1. **React Native Path**
   ```
   Project Structure:
   /job-tracker
     /frontend             # Existing web frontend
     /backend             # Existing FastAPI backend
     /mobile
       /src
         /components      # Mobile-specific React components
         /navigation     # React Navigation setup
         /screens        # Mobile screen components
         /utils         # Shared utilities with web
   ```
   
   **Development Time Estimate:** 2-3 months
   - Week 1-2: Setup and basic navigation
   - Week 3-4: Core features port
   - Week 5-6: Mobile-specific features
   - Week 7-8: Testing and refinement

2. **Native Swift Path**
   ```
   Project Structure:
   /job-tracker
     /frontend            # Existing web frontend
     /backend            # Existing FastAPI backend
     /ios
       /JobTracker
         /Models         # Swift data models
         /Views         # SwiftUI views
         /ViewModels    # Swift view models
         /Services      # API and data services
         /Utils        # iOS utilities
   ```
   
   **Development Time Estimate:** 4-6 months
   - Month 1: Setup and architecture
   - Month 2: Core feature implementation
   - Month 3: iOS-specific features
   - Month 4: Testing and App Store prep

### Mobile-Specific Features

1. **Data Management**
   - Offline data storage using Core Data or SQLite
   - Background sync capabilities
   - Conflict resolution for offline changes
   - Efficient data pagination

2. **iOS Integration**
   - Push notifications for follow-ups
   - Calendar integration for interviews
   - Document picker for files
   - Share extension for job URLs
   - Spotlight search integration
   - Home screen quick actions
   - iOS widgets for status overview

3. **Security Requirements**
   - Keychain integration for credentials
   - Biometric authentication
   - App transport security
   - Data encryption at rest
   - Privacy policy compliance
   - App Store guidelines compliance

4. **UI/UX Requirements**
   - Native iOS UI patterns
   - Dark mode support
   - Dynamic type support
   - VoiceOver accessibility
   - Haptic feedback
   - Gesture navigation

### API Modifications Needed

1. **Mobile Optimization**
   ```json
   {
     "endpoints": {
       "GET /applications": {
         "additions": ["pagination", "delta updates"],
         "modifications": ["reduced payload size", "binary optimizations"]
       }
     }
   }
   ```

2. **New Mobile Endpoints**
   ```json
   {
     "new_endpoints": {
       "POST /sync": "Batch synchronization",
       "GET /notifications": "Push notification settings",
       "POST /offline-changes": "Bulk offline changes upload"
     }
   }
   ```

### Development Approach Recommendation

**Recommended: React Native First**
1. Maintain single codebase initially
2. Leverage existing team expertise
3. Faster time to market
4. Share business logic
5. Option to move to native later

**Future Native Swift Considerations**
- Consider native rewrite after market validation
- When performance becomes critical
- When deeper iOS integration needed
- When team has iOS expertise

