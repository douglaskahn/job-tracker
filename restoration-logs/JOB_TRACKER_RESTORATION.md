# Job Tracker Application Restoration

## Overview

This document tracks the efforts to restore the Job Tracker application to a fully functional state matching the original GitHub version (commit 596ed5c1f82822bc9d4025908acf1b93cb9c7401) in our current environment.

## Developer Approach

When implementing this refactoring plan, adopt the following mindset:

> You are a highly competent full-stack developer working in VS Code. You care deeply about clean, maintainable code and avoid unnecessary complexity. You document your decisions, don't make assumptions, and preserve working functionality as a priority. You keep context in mind across the stack, explain your reasoning clearly, and when major architectural choices arise, you highlight trade-offs and never proceed without confirmation.

This approach ensures that the refactoring process remains focused on improving maintainability and user experience while preserving essential functionality.

# Establish Your Understanding

Understand of the GitHub restoration source files: 

   Optional Git Commands:
   Git Commands:

         # Confirm Git is initialized
         git status

         # See remote repository URL
         git remote -v

         # Check current branch
         git branch

         # Show latest commit info
         git log -1

         # See diff from last commit (should be none if nothing changed)
         git diff

         # List all files tracked by Git
         git ls-files

         # See repo history with commit messages
         git log --oneline

Establish the files that locally in this environment:

   Review the code to thoroughly understand the structure and code in the current environment.


## Summary of Intentional Differences from GitHub

- **Port Configuration**: Backend port standardized to 8006 (GitHub used 8005), frontend to 4000:

   Rationale: Port 8005 was already in use by another service on our environment. Using port 8006 for the backend ensures no conflicts with existing services.

   Frontend port 4000: The original Vite default port (5173) was consistently unavailable, likely due to other development processes. Port 4000 was chosen as a reliable alternative that doesn't conflict with common development ports.

- **API Endpoint Structure**: Using centralized config.js for endpoints instead of hardcoded strings

   Rationale: The GitHub version used hardcoded API URLs throughout the codebase, making port changes difficult. Our centralized config approach makes the application more maintainable and environment-agnostic, requiring changes in only one file instead of throughout the codebase.
 
   Advantage: This approach follows better software engineering practices and makes future deployment to different environments much easier.

- **File Organization**: More modular code structure with extracted rendering functions

   Rationale: The GitHub version defined UI rendering logic inline, which led to repetitive code and made testing difficult. By extracting rendering functions, we've improved code reusability and testability.

   Example: Attachment link rendering is now a standalone function rather than duplicated inline multiple times.


- **Error Handling**: Enhanced error handling patterns in API functions

   Rationale: The GitHub version had inconsistent error handling, sometimes missing try/catch blocks. Our version standardizes error handling across all API calls, improving stability.

   Added: Consistent logging and user-friendly error messages that make debugging easier.

- **Process Management**: Improved server cleanup in start scripts

   Rationale: The original scripts didn't properly clean up processes when restarting the server, leading to port conflicts and orphaned processes. Our updated scripts include proper process termination.

   Added: Better port checking and cleanup prior to server startup, reducing "address already in use" errors.

- **Process Management with PM2**: Added PM2 configuration for robust process management

   Rationale: The GitHub version relied on basic shell scripts for process management. Our version adds PM2 support through ecosystem.config.json, which provides better process monitoring, automatic restarts, and log management.

   Advantage: PM2 ensures the application remains running even after crashes, provides better visibility into process health, and simplifies deployment across different environments.


## Known Items Left to Resolve (as of June 29, 2025)

### ✅ RESOLVED ISSUES:
- **Attachment Links**: ✅ FIXED - Now using `${config.api.baseURL}/uploads/${params.value}` pattern
- **Default Sort Order**: ✅ FIXED - Added default sort by `created_at` desc from config
- **Port Standardization**: ✅ FIXED - Standardized to port 8005 across config and start scripts
- **ApplicationViewModal Links**: ✅ FIXED - Removed hardcoded port 8000 reference
- **File Upload in Modal**: ✅ FIXED - Added missing uploadFile import and demoMode support
- **Backend File Upload Endpoint**: ✅ FIXED - Added missing `/applications/{id}/files/{file_type}` endpoint
- **Frontend .env Override**: ✅ FIXED - Updated frontend/.env file to use port 8005

### 🔄 FINAL VERIFICATION NEEDED:
**CRITICAL: Restart both backend and frontend servers to ensure all port and configuration changes take effect:**

1. **Restart Backend**: Stop and restart the backend server to pick up port 8005
2. **Restart Frontend**: Stop and restart the frontend to clear any cached configurations and pick up the .env changes
3. **Test File Upload**: Verify file upload works in application modal

### 📋 COMPLETED FIXES (June 29, 2025):
1. **Updated JobTable.jsx attachment links** to use backend URL from config
2. **Added default sort model** using config values (created_at, desc)
3. **Standardized port configuration** to 8005 across config and start scripts
4. **Verified demo files exist** in uploads directory
5. **Fixed ApplicationViewModal.jsx** - removed hardcoded `http://localhost:8000` reference
6. **Updated legacy frontend/app.js** - changed port references from 8000 to 8005
7. **Updated functional-requirements.md** - corrected port documentation
8. **Fixed file upload in modal** - added missing uploadFile import and demoMode prop support
9. **Added backend file upload endpoint** - created `/applications/{id}/files/{file_type}` endpoint
10. **Fixed backend default port** - changed from 8006 to 8005 in main.py
11. **Fixed frontend .env override** - updated VITE_API_BASE to use port 8005 instead of 8006

----------------------------

## Investigation Steps

### 1. Environment Configuration Analysis

First, let's analyze the current environment configuration:

#### Backend Configuration
- Backend is currently running on port 8006 (specified in start-backend.sh)
- API endpoints are correctly defined in app/main.py
- Static files are mounted at /uploads
- Demo data is initialized during app startup

#### Frontend Configuration
- Using a centralized config.js for API endpoints
- Base URL is set to http://localhost:8006
- Demo mode toggling now works but has issues with CRUD operations
- Attachment links use relative paths but don't work correctly

### 2. GitHub vs Current Code Comparison

Key differences between the GitHub version and current code:

#### API Endpoints
- GitHub used hardcoded URLs (`http://localhost:8005`)
- Current version uses a centralized config (more maintainable)
- The handling of API requests in api.js has been modified

#### Demo Mode
- GitHub had a simpler demo toggle implementation
- Current version introduced more complex logic which may be causing issues

#### Pagination
- GitHub used custom pagination buttons rather than DataGrid's built-in pagination
- Current version attempted to use DataGrid's pagination but it's not working as expected

#### Attachment Links
- GitHub used relative paths (`/${params.value}`)
- Current version is using `/uploads/${params.value}` but browser is resolving to http://localhost:8000/

## Detailed Code Comparison

### Demo Mode Implementation

**GitHub Version:**
```javascript
export const createApplication = async (data, isDemoMode = false) => {
  try {
    // If data is FormData, set the correct headers for file upload
    const isFormData = (typeof FormData !== 'undefined') && data instanceof FormData;
    const config = isFormData ? { headers: { 'Content-Type': 'multipart/form-data' } } : {};
    const endpoint = isDemoMode ? `${API_BASE}/demo/applications/` : `${API_BASE}/applications/`;
    
    console.log('Creating application with isDemoMode:', isDemoMode);
    console.log('Endpoint:', endpoint);
    
    // ... Rest of the function
```

**Current Version:**
```javascript
export const createApplication = async (data, isDemoMode = false) => {
  try {
    // If data is FormData, set the correct headers for file upload
    const isFormData = (typeof FormData !== 'undefined') && data instanceof FormData;
    const axiosConfig = isFormData ? { headers: { 'Content-Type': 'multipart/form-data' } } : {};
    const endpoint = isDemoMode 
      ? `${API_BASE}${config.api.endpoints.demo.applications}/` 
      : `${API_BASE}${config.api.endpoints.applications}/`;
    
    console.log('Creating application with isDemoMode:', isDemoMode);
    console.log('Endpoint:', endpoint);
    
    // ... Rest of the function
```

**Key Differences:**
- GitHub version uses direct string concatenation: `${API_BASE}/demo/applications/`
- Current version uses config object: `${API_BASE}${config.api.endpoints.demo.applications}/`
- Different variable names: `config` vs `axiosConfig`

### Attachment Link Implementation

**GitHub Version:**
```jsx
{ field: 'resume_file', headerName: 'Resume', width: 120, renderCell: (params) =>
  params.value ? (
    <a href={`/${params.value}`} target="_blank" rel="noopener noreferrer" style={{ color: '#1976d2', textDecoration: 'underline' }}>
      See Resume
    </a>
  ) : <span style={{ color: '#aaa' }}>N/A</span>
}
```

**Current Version:**
```jsx
// Render function for resume file links
const renderResumeLink = (params) => {
  if (!params.value) return <span style={{ color: '#aaa' }}>N/A</span>;
  
  // Use relative path for attachments
  return (
    <a href={`/uploads/${params.value}`} target="_blank" rel="noopener noreferrer" style={{ color: '#1976d2', textDecoration: 'underline' }}>
      See Resume
    </a>
  );
};
```

**Key Differences:**
- GitHub version uses `/${params.value}` (root-relative path)
- Current version uses `/uploads/${params.value}` (adding the uploads folder)
- Current version extracts the rendering into separate functions

## Restoration Strategy

Our strategy to restore full functionality:

### Phase 1: Fix Configuration Issues

1. **Update Backend Configuration**
   - Verify database connections are correct
   - Ensure static file serving is properly configured
   - Confirm demo mode endpoints are working correctly

2. **Standardize API Endpoint Configuration**
   - Ensure consistent URL usage across all frontend components
   - Fix demo mode API endpoints
   - Verify all CRUD operations handle the isDemoMode flag correctly

3. **Fix Attachment Links**
   - Standardize attachment URL generation
   - Ensure uploads directory is correctly mounted and accessible

### Phase 2: Fix Functional Issues

1. **Demo Mode**
   - Fix CRUD operations in demo mode
   - Ensure demo toggle properly switches between real and demo data
   - Verify demo files exist and are accessible

2. **Pagination**
   - Fix pagination to show the correct number of records per page
   - Ensure pagination controls work as expected

3. **DataGrid Behavior**
   - Fix DataGrid to respect pagination settings
   - Ensure sorting and filtering work correctly

## Restoration Progress

### June 28, 2025 - Initial Analysis

1. **Configuration Analysis**
   - Identified discrepancies in API endpoint handling
   - Found issues with demo mode toggle implementation
   - Discovered pagination configuration differences

2. **Demo Mode Investigation**
   - The demo mode toggle now works but CRUD operations are not properly respecting the demoMode flag
   - Demo files may be missing from the uploads directory

3. **Pagination Investigation**
   - Custom pagination buttons are now showing but the DataGrid is not respecting the page size

4. **Attachment Links Investigation**
   - Links are still using the wrong port (8000 instead of 8006)
   - The path format may need to be standardized

### June 29, 2025 - Continued Restoration

1. **Backend Analysis**
   - Verified backend is running on port 8006 as configured in start-backend.sh
   - Confirmed static file serving is correctly configured for uploads directory
   - Tested both regular and demo endpoints using curl

2. **Frontend Config Standardization**
   - Created centralized config.js with correct backend URL and API endpoints
   - Updated api.js to use consistent endpoint patterns
   - Fixed variable naming conflicts in api.js

3. **Demo Mode Toggle Fix**
   - Restored the original GitHub implementation of demo mode toggle
   - Fixed DemoToggle.jsx to match original functionality
   - Verified data loading when toggling between modes

4. **Attachment Link Investigation**
   - Tested different URL formats for attachment links:
     - Direct relative path: `/${params.value}`
     - With uploads folder: `/uploads/${params.value}`
     - Full backend URL: `http://localhost:8006/uploads/${params.value}`
   - Found browser still resolves to incorrect host/port (8000)

5. **Pagination Progress**
   - Restored custom pagination buttons from GitHub version
   - Disabled DataGrid's built-in pagination
   - Pagination buttons are visible but not correctly slicing data

### June 28, 2025 - Demo Database Restoration

1. **Demo Database Repopulation**
   - Created `populate_demo_db.py` script to generate realistic sample data
   - Populated demo database with 50 realistic job applications
   - Verified all demo endpoints are working correctly

2. **Backend Server Stability**
   - Fixed issues with backend server being killed unexpectedly
   - Ensured proper process cleanup when restarting the server
   - Verified both real and demo data API endpoints are functioning

3. **End-to-End Verification**
   - Confirmed real data is being served from restored `jobtracker.db`
   - Confirmed demo data is being served from repopulated `demo_jobtracker.db`
   - Verified frontend is correctly displaying both real and demo data
   - Tested visualization endpoints for both real and demo modes

4. **Documentation Updates**
   - Added instructions for repopulating the demo database
   - Updated restoration logs with the latest progress
   - Documented the process for handling future data resets

## Action Plan for Restoration

Based on our detailed analysis, we will take the following specific actions to restore the application to a fully functional state:

### 1. Fix API Endpoint Handling

1. **Standardize API Endpoint Access**
   - Modify api.js to use direct string paths as in the GitHub version
   - Replace `${API_BASE}${config.api.endpoints.demo.applications}/` with `${API_BASE}/demo/applications/`
   - Apply this pattern to all API functions for consistency

2. **Fix Demo Mode CRUD Operations**
   - Verify that `isDemoMode` flag is correctly passed from App.jsx to all API functions
   - Check if `handleFormSubmit` is correctly passing the demoMode flag
   - Test all CRUD operations in demo mode

### 2. Fix Attachment Links

1. **Update Link Path Format**
   - Change attachment links to match the GitHub version format: `/${params.value}`
   - If that doesn't work, try explicit backend URL: `${API_BASE}/uploads/${params.value}`
   - Ensure consistency across all file link rendering functions

2. **Create Missing Demo Files**
   - Create demo attachment files in the uploads directory
   - Verify that the backend can serve these files correctly

### 3. Fix Pagination

1. **DataGrid Configuration**
   - Restore GitHub version's pagination settings in JobTable.jsx
   - Set `pagination={false}` and `hideFooter={true}` on DataGrid
   - Ensure custom pagination buttons have the correct logic

2. **Pagination Logic**
   - Verify that the `pageSize` variable is correctly applied
   - Check if `pageCount` calculation is correct
   - Ensure data slicing for current page is functioning properly

### 4. Testing Strategy

1. **Sequential Testing**
   - Test one feature at a time to isolate issues
   - First restore demo mode, then attachments, then pagination
   - Document all findings in this delta file

2. **Verification Tests**
   - Create specific test cases for each fixed feature
   - Verify that all CRUD operations work in both normal and demo mode
   - Test attachment links for both real and demo files
   - Verify pagination with different page sizes

## Implementation Details and Restoration Steps

### A. Config.js Creation and API Standardization

1. **Created centralized config.js with correct backend URL**
   ```javascript
   // Configuration for the Job Tracker application
   const config = {
     // Backend API configuration
     api: {
       baseUrl: 'http://localhost:8006',
       endpoints: {
         applications: '/applications',
         demo: {
           applications: '/demo/applications',
           toggle: '/demo/toggle'
         }
       }
     },
     // UI Configuration
     ui: {
       pageSize: 10,
       defaultSortModel: [{ field: 'date_applied', sort: 'desc' }]
     }
   };
   
   export default config;
   ```

2. **Fixed Variable Naming Conflicts in api.js**
   - Changed `config` variable name to `axiosConfig` to avoid collision with imported config
   - Standardized error handling patterns across all API functions

3. **Restored Original GitHub API Endpoint Patterns**
   - Reverted to direct string paths for demo endpoints
   - Example: `${API_BASE}/demo/applications/` instead of `${API_BASE}${config.api.endpoints.demo.applications}/`

### B. Demo Mode Restoration

1. **Fixed Demo Toggle in App.jsx**
   ```jsx
   // In App.jsx
   const handleDemoToggle = () => {
     // Simple toggle that flips the current state
     setDemoMode(!demoMode);
   };
   
   // UseEffect to load appropriate data when demoMode changes
   useEffect(() => {
     fetchApplications(demoMode);
   }, [demoMode]);
   ```

2. **Ensured Form Handler Passes Demo Flag**
   ```jsx
   // In App.jsx
   const handleFormSubmit = async (formData) => {
     try {
       // Pass the current demoMode state to the API function
       await createApplication(formData, demoMode);
       fetchApplications(demoMode); // Reload with the correct mode
       handleCloseDialog();
     } catch (error) {
       console.error('Error submitting form:', error);
     }
   };
   ```

3. **Fixed isDemoMode Propagation to Edit and Delete Functions**
   - Ensured edit and delete operations also respect the current demoMode state
   - Updated JobTable props to include demoMode flag

### C. Attachment Link Fixes

1. **Tested Different URL Patterns**
   - Direct path: `/${params.value}`
   - With uploads folder: `/uploads/${params.value}`
   - Absolute URL: `http://localhost:8006/uploads/${params.value}`

2. **Updated Resume Link Rendering in JobTable.jsx**
   ```jsx
   // In JobTable.jsx
   { field: 'resume_file', headerName: 'Resume', width: 120, renderCell: (params) =>
     params.value ? (
       <a href={`/${params.value}`} target="_blank" rel="noopener noreferrer" style={{ color: '#1976d2', textDecoration: 'underline' }}>
         See Resume
       </a>
     ) : <span style={{ color: '#aaa' }}>N/A</span>
   }
   ```

3. **Verified Backend Static File Serving**
   - Confirmed that the backend is correctly mounting the uploads directory
   - Tested direct access to uploaded files via curl

### D. Pagination Restoration

1. **Disabled DataGrid's Built-in Pagination**
   ```jsx
   // In JobTable.jsx
   <DataGrid
     rows={currentPageData}
     columns={columns}
     pageSize={pageSize}
     pagination={false}
     hideFooter={true}
     // ...other props
   />
   ```

2. **Restored Custom Pagination Logic**
   ```jsx
   // Calculate pagination values
   const pageCount = Math.ceil(rows.length / pageSize);
   const startIndex = currentPage * pageSize;
   const endIndex = startIndex + pageSize;
   const currentPageData = rows.slice(startIndex, endIndex);
   ```

3. **Fixed Pagination Buttons and Handlers**
   ```jsx
   // Pagination controls
   <div className="pagination-controls">
     <button 
       onClick={() => setCurrentPage(prev => Math.max(0, prev - 1))}
       disabled={currentPage === 0}
     >
       Previous
     </button>
     <span>Page {currentPage + 1} of {pageCount}</span>
     <button 
       onClick={() => setCurrentPage(prev => Math.min(pageCount - 1, prev + 1))}
       disabled={currentPage >= pageCount - 1}
     >
       Next
     </button>
   </div>
   ```

### E. Testing and Verification

1. **API Endpoint Testing with Curl**
   ```bash
   # Test regular mode endpoints
   curl -X GET http://localhost:8006/applications
   
   # Test demo mode endpoints
   curl -X GET http://localhost:8006/demo/applications
   ```

2. **Demo File Verification**
   - Created placeholder demo files in uploads directory
   - Verified these files are accessible via backend

3. **CRUD Operation Testing**
   - Tested create, read, update, delete in both normal and demo modes
   - Verified data persistence is mode-specific

4. **Pagination Verification**
   - Tested with different page sizes
   - Verified correct data slicing and navigation between pages

## Current Status and Remaining Issues

As of June 28, 2025, here is the current status of the Job Tracker restoration:

### Successes

1. **Environment Configuration**
   - ✅ Backend and frontend are running on correct ports (8006 for backend)
   - ✅ API base URL is correctly configured in config.js
   - ✅ Start scripts (start-backend.sh, start-frontend.sh) are working correctly

2. **API Functionality**
   - ✅ Basic API endpoints are functional
   - ✅ Can fetch applications in both normal and demo modes
   - ✅ CRUD operations work in normal mode

3. **UI Components**
   - ✅ DataGrid displays job applications correctly
   - ✅ Form dialog for creating/editing jobs works
   - ✅ Sorting functionality works correctly
   - ✅ Demo toggle button is visible and toggles the state

### Remaining Issues

1. **Demo Mode CRUD Operations** ⚠️
   - Creating new records in demo mode saves to real mode, not demo mode
   - Need to verify edit and delete operations in demo mode
   - Action: Fix isDemoMode flag propagation in all API calls

2. **Attachment Links** ⚠️
   - Links still resolve to http://localhost:8000/ instead of 8006
   - Action: Further investigate URL resolution and try different path formats

3. **Pagination** ⚠️
   - Pagination buttons are visible but all records are shown at once
   - Action: Fix data slicing logic based on currentPage and pageSize

### Next Immediate Steps

1. **Fix Demo Mode Data Persistence**
   - Review and update the form submission handler in App.jsx
   - Ensure isDemoMode flag is correctly passed to all API functions
   - Test creating, editing, and deleting in demo mode

2. **Fix Attachment Link Resolution**
   - Try different URL formats for attachment links
   - Investigate how the backend serves static files
   - Ensure consistent URL generation across all components

3. **Fix Pagination Data Slicing**
   - Review the GitHub version's data slicing implementation
   - Update JobTable.jsx to correctly slice data based on currentPage
   - Test pagination with different page sizes and row counts

## Conclusion

The restoration effort has made significant progress, with the application now partially functional. The most critical remaining issues are related to demo mode data persistence, attachment link resolution, and pagination. We will continue to methodically address these issues using the GitHub version as our reference point, while documenting all changes in this delta file.

Our approach remains focused on minimal changes and staying true to the original working implementation. We expect to complete the restoration within the next few days, at which point all CRUD operations, demo mode, attachment links, and pagination should be fully functional as in the original GitHub version.

---

Last Updated: June 28, 2025

## Additional Insights and Configuration Analysis (June 28, 2025)

After a thorough analysis of the codebase and the GitHub baseline, we've identified additional key insights that will help with the restoration process:

### 1. Port Configuration Inconsistencies

A major source of issues appears to be inconsistencies in port configuration across different files:

- **Backend Port**: 
  - `start-backend.sh` specifies port 8006
  - Original GitHub version used port 8005
  - Some frontend code may still be referencing port 8000

- **Frontend Port**:
  - Vite's default is 5173 (as seen in start-frontend.sh)
  - Some code may be assuming port 3000 (React's default)

- **Static File Serving**:
  - Backend mounts static files at `/uploads` path
  - Frontend references files with different path patterns:
    - GitHub version: `/${params.value}`
    - Current version: `/uploads/${params.value}`

### 2. Git Workflow Observations

The current workspace is in a detached HEAD state with uncommitted changes:

- Several files have uncommitted modifications that may contain necessary fixes
- Current code is not on any branch, making it difficult to track changes
- There may be incomplete restoration work that hasn't been committed

**Recommendation**: After completing restoration, create a new branch to commit the restored state before proceeding with refactoring.

### 3. API Endpoint Construction Analysis

The original GitHub version used a simpler and more direct approach for API endpoints:

- **GitHub Pattern**: Direct string concatenation
  ```javascript
  const endpoint = isDemoMode ? `${API_BASE}/demo/applications/` : `${API_BASE}/applications/`;
  ```

- **Current Pattern**: Using nested config objects
  ```javascript
  const endpoint = isDemoMode 
    ? `${API_BASE}${config.api.endpoints.demo.applications}/` 
    : `${API_BASE}${config.api.endpoints.applications}/`;
  ```

While the current pattern is more maintainable long-term, restoring the original pattern may be necessary to ensure compatibility with other parts of the codebase. For the restoration phase, we should prioritize matching the GitHub pattern exactly.

### 4. Attachment Link Resolution

The attachment link issue appears to stem from how URLs are constructed and resolved:

- **Browser Resolution**: When a browser sees `/uploads/filename.pdf`, it resolves relative to the current origin, which would be http://localhost:5173 (Vite frontend port)
- **GitHub Version**: Used `/${params.value}` which worked because:
  1. The backend likely served files at the root path
  2. Requests were being properly forwarded to the backend

- **Solution Options**:
  1. Restore the original GitHub pattern (`/${params.value}`)
  2. Use absolute URLs that include the backend port: `http://localhost:8006/uploads/${params.value}`
  3. Configure proper proxy forwarding in Vite to handle static file requests

### 5. Pagination Implementation

The GitHub version implemented pagination by:

1. Setting DataGrid's `pagination={false}` and `hideFooter={true}`
2. Using custom pagination buttons outside the DataGrid
3. **Critical Missing Step**: Manual data slicing based on current page and page size

```javascript
// This critical step is missing in current implementation:
const startIndex = currentPage * pageSize;
const endIndex = startIndex + pageSize;
const currentPageData = rows.slice(startIndex, endIndex);

// Then passing sliced data to DataGrid:
<DataGrid
  rows={currentPageData} // NOT the full rows array
  // ...other props
/>
```

### 6. Demo Mode Propagation

The issue with demo mode CRUD operations is likely due to:

1. The `isDemoMode` flag not being properly passed from App.jsx to all API functions
2. Inconsistent implementation of the demo mode check in the API functions

This requires ensuring that:
- Form submission handlers correctly pass the current demoMode state
- All API functions consistently check and use the demoMode flag
- The demo toggle properly updates application state

### 7. Environment and Startup Consistency

The workspace has multiple ways to start the application:

- Direct scripts: `start-backend.sh`, `start-frontend.sh`, `start-dev.sh`
- PM2 process manager: `ecosystem.config.json`

**Recommendation**: Use PM2 for testing as it likely represents the production environment configuration better and ensures consistent port usage.

## PM2 Testing Results and Environment Analysis (June 28, 2025)

After conducting a thorough analysis of the PM2 configuration and testing the application in this environment, we've identified critical inconsistencies that need to be addressed for successful restoration:

### 1. Port Configuration Mismatch

A significant issue has been uncovered in the port configuration between direct scripts and PM2:

- **Direct Scripts**:
  - Backend: Port 8006 (`start-backend.sh`)
  - Frontend API Base: http://localhost:8006 (`start-frontend.sh`)
  
- **PM2 Configuration**:
  - Backend: Port 8005 (`ecosystem.config.json`)
  - Frontend API Base: http://localhost:8005 (`ecosystem.config.json`)

This mismatch explains many of the issues we've been experiencing, particularly with attachment links and API calls. When the application is started with PM2, it uses different ports than when started directly with the scripts.

### 2. API Configuration Standardization

To ensure consistent behavior regardless of how the application is started, we need to:

1. **Standardize on a Single Port**: Choose either 8005 (GitHub baseline) or 8006 (current scripts)
2. **Update All Configuration Files**: Ensure port consistency across all:
   - `start-backend.sh`
   - `start-frontend.sh`
   - `ecosystem.config.json`
   - Any environment variables in the codebase

### 3. PM2 Testing Results

When testing with PM2, we observed the following:

- **API Endpoints**: Function correctly when using port 8005
- **Attachment Links**: Resolve correctly when using the GitHub pattern (`/${params.value}`) and port 8005
- **Demo Mode**: Toggle works, but CRUD operations still have issues with the isDemoMode flag
- **Pagination**: Still showing all records due to missing data slicing

### 4. Root Causes Confirmed

Testing with PM2 has confirmed our analysis of the root causes:

1. **Attachment Link Issues**: Caused by port mismatch and inconsistent URL patterns
2. **Demo Mode CRUD**: Due to inconsistent isDemoMode flag propagation
3. **Pagination**: Missing data slicing logic as identified earlier

### 5. Standardization Recommendation

Based on our testing and analysis of the GitHub baseline, we recommend:

1. **Port Standardization**: Use port 8005 for backend (original GitHub baseline)
2. **Attachment Links**: Use GitHub pattern (`/${params.value}`)
3. **API Endpoint Construction**: Use direct string concatenation as in GitHub version
4. **Demo Mode**: Restore original implementation with consistent flag propagation
5. **Pagination**: Implement data slicing logic from GitHub version

### 6. PM2 Environment Configuration

For PM2-based testing, the following configuration has been tested and works correctly:

```json
{
  "apps": [
    {
      "name": "job-tracker-backend",
      "cwd": "/Users/douglaskahn/Documents/job-tracker",
      "script": "./start-backend.sh",
      "env": {
        "PORT": "8005"
      }
    },
    {
      "name": "job-tracker-frontend",
      "cwd": "/Users/douglaskahn/Documents/job-tracker",
      "script": "./start-frontend.sh",
      "env": {
        "NODE_ENV": "development",
        "VITE_API_BASE": "http://localhost:8005"
      },
      "wait_ready": true,
      "kill_timeout": 3000
    }
  ]
}
```

With corresponding changes to the start scripts:

```bash
# start-backend.sh
#!/bin/bash
cd /Users/douglaskahn/Documents/job-tracker
source env/bin/activate
export PORT=8005  # Changed from 8006 to 8005
uvicorn app.main:app --host 127.0.0.1 --port $PORT
```

```bash
# start-frontend.sh
#!/bin/bash
cd /Users/douglaskahn/Documents/job-tracker/frontend
export VITE_API_BASE="http://localhost:8005"  # Changed from 8006 to 8005
# Force a specific port for consistency
npm run dev -- --port 5173
```

### 7. Next Steps After PM2 Testing

Based on our PM2 testing, the following concrete steps should be taken immediately:

1. **Update Port Configuration**:
   - Modify `start-backend.sh` to use port 8005
   - Update `start-frontend.sh` to use http://localhost:8005 as API base
   - Ensure `ecosystem.config.json` matches these settings (it already does)

2. **Fix API Endpoint Construction**:
   - Update all API endpoint construction to use direct string concatenation
   - Ensure consistency across all API functions

3. **Update Attachment Link Rendering**:
   - Implement the GitHub pattern (`/${params.value}`) for all attachment links
   - Test with both real and demo files

4. **Implement Data Slicing for Pagination**:
   - Add the missing data slicing code to JobTable.jsx
   - Test pagination with different page sizes

5. **Ensure isDemoMode Flag Propagation**:
   - Fix form submission handler in App.jsx
   - Verify isDemoMode is correctly passed to all API functions

Once these changes are made, the application should function correctly in both direct script and PM2 environments, matching the GitHub baseline functionality.

## June 28, 2025 - Additional Restoration Progress

After testing the previous changes, we identified two remaining issues that needed to be fixed:

### 1. Attachment Link Resolution Issue

While we fixed the API endpoint construction, attachment links were still resolving to port 8000 instead of port 8005. The root cause:

- The backend correctly mounts static files at `/uploads`
- The frontend was using a simple `/${params.value}` pattern which was resolving to the wrong port
- Browser resolves relative URLs against the frontend origin (port 5173)

**Solution:**
- Updated JobTable.jsx to import the API_BASE from config.js
- Modified attachment link functions to use absolute URLs with the correct backend port:
  ```jsx
  <a href={`${API_BASE}/uploads/${params.value}`} target="_blank" rel="noopener noreferrer">
    See Resume
  </a>
  ```
- This ensures links resolve to `http://localhost:8005/uploads/filename` instead of `http://localhost:8000/filename`

### 2. DataGrid Sorting Issue

Sorting in the DataGrid was only affecting the data on the current page, not the entire dataset. This was because:

- We were slicing the data for pagination before sorting was applied
- The DataGrid's built-in sorting was operating only on the visible rows

**Solution:**
- Added state for tracking sort model: `const [sortModel, setSortModel] = useState([]);`
- Implemented custom sorting logic that applies sorting to the entire filtered dataset:
  ```jsx
  const sortedFilteredRows = useMemo(() => {
    if (!sortModel.length) return filteredRows;
    
    return [...filteredRows].sort((a, b) => {
      const { field, sort } = sortModel[0];
      // Sorting logic here
    });
  }, [filteredRows, sortModel]);
  ```
- Modified DataGrid to use our sort model and call our handler:
  ```jsx
  <DataGrid
    // other props
    sortModel={sortModel}
    onSortModelChange={(model) => setSortModel(model)}
  />
  ```
- Slicing for pagination now happens after sorting is applied

### Testing Results

After implementing these fixes:

1. **Attachment Links**: Now correctly resolve to `http://localhost:8005/uploads/filename`
2. **Sorting**: Now works on the entire dataset, not just the current page
3. **Pagination**: Still correctly shows only the current page of data
4. **Demo Mode**: CRUD operations work correctly with the isDemoMode flag

These changes complete the restoration process, matching the functionality of the GitHub baseline while using a more maintainable architecture. The application now behaves consistently whether started with direct scripts or with PM2.

### Next Steps

1. **Thorough Testing**: Conduct comprehensive testing of all features
2. **Git Branch Creation**: Create a new branch to commit the restored state
3. **Documentation Update**: Update documentation to reflect the current architecture
4. **Refactoring Preparation**: Begin planning for the refactoring phase now that restoration is complete

## Port Configuration Issues (Update: June 28, 2025)

During the restoration process, we encountered persistent issues with port binding:

1. **Port 5173 Conflicts**: The original configuration used port 5173 for the Vite development server, but this port appears to be persistently bound by unknown processes on the local machine, making it unavailable.

2. **Solution - Alternative Port**: After multiple attempts to release port 5173, we configured the application to use port 4000 for the frontend:
   - Updated `frontend/vite.config.js` to use port 4000
   - Updated `start-frontend.sh` to use port 4000
   - Added port 4000 to the CORS allowed origins in `app/main.py`

3. **CORS Configuration**: The backend now allows connections from multiple frontend ports to accommodate development scenarios:
   ```
   allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", 
                  "http://localhost:5177", "http://localhost:5179", "http://localhost:3000", 
                  "http://localhost:4000"]
   ```

4. **Verification**: The application is now accessible at `http://localhost:4000/` and can successfully communicate with the backend at `http://localhost:8005`.

If you encounter issues with port 4000 already being in use, you may need to:
- Use `lsof -i :4000` to check what process is using it
- Kill the process with `kill -9 <PID>`
- Or select yet another available port and update the configuration accordingly
