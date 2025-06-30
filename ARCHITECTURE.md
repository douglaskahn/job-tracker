# Job Tracker Application Architecture

This document outlines the key components and functionality of the Job Tracker application to help prevent inadvertent breaking changes. For a complete list of functional requirements, please refer to [functional-requirements.md](functional-requirements.md).

## Key Components

### Backend

- **app/main.py**: Main FastAPI application entry point with route definitions
- **app/models.py**: SQLAlchemy models for the database
- **app/schemas.py**: Pydantic schemas for request/response validation
- **app/crud.py**: CRUD operations for the main application data
- **app/demo_crud.py**: CRUD operations for demo data
- **app/database.py**: Database connection setup

### Frontend

- **src/App.jsx**: Main React component with application state
- **src/JobTable.jsx**: Table component for displaying job applications
- **src/api.js**: API client for communicating with the backend
- **src/config.js**: Configuration for API base URL
- **src/ShowAllModal.jsx**: Modal for displaying all records
- **src/ApplicationViewModal.jsx**: Modal for viewing/editing a single application

## Application Architecture

### Frontend-Backend Communication Flow

1. The frontend (**App.jsx**) initializes by fetching configuration from the backend
2. User interactions trigger API calls defined in **api.js**
3. The backend processes requests through routes in **main.py**
4. Data is retrieved or modified via CRUD operations in **crud.py** or **demo_crud.py**
5. Results are returned to the frontend and displayed in the UI

### State Management

- **App.jsx** contains the main application state
- State is passed down to child components via props
- API calls update the central state in App.jsx
- Modal interactions (view, edit, delete) update the central state
- The application uses controlled components for form inputs

### Environment Configuration

- Frontend uses **.env** files for environment variables
- Backend uses command-line arguments and environment variables
- PM2 manages environment variables through **ecosystem.config.json**
- Dynamic configuration is fetched from the **/api/config** endpoint

## Critical Functionality

### Server-Side Pagination, Sorting, and Filtering

The application uses server-side pagination, sorting, and filtering to handle large datasets efficiently:

1. `loadData()` in App.jsx sends pagination, sorting, and filtering parameters to the backend
2. The backend API endpoints in app/crud.py and app/demo_crud.py process these parameters
3. The JobTable component displays the current page of data with pagination controls

**IMPORTANT**: Any changes to `handleShowAll`, `loadData`, or pagination logic must preserve the server-side nature of these operations.

### "Show All" Functionality

The "Show All" button should display ALL records, not just the current page. This requires:

1. Fetching all records from the API without pagination
2. Displaying them in the ShowAllModal component
3. Reloading the paginated data when the modal is closed

### DataGrid Configuration

The DataGrid component has specific configuration that must be preserved:

1. `hideFooter={true}` and `hideFooterPagination={true}` to hide the built-in pagination
2. Custom pagination buttons below the table
3. `pagination={false}` to disable the built-in pagination

### API Communication

The frontend communicates with the backend through functions in api.js:

1. `fetchApplications()` for real data
2. `fetchDemoApplications()` for demo data
3. These functions pass query parameters for server-side operations

## Common Issues and Solutions

### Issue: "Show All" only shows current page

Solution: Make sure `handleShowAll` fetches ALL records without pagination.

```jsx
const handleShowAll = async () => {
  // Fetch all records with a large page_size
  const allParams = { page_size: 1000 };
  const allRecords = await fetchApplications(allParams);
  setApplications(allRecords.data);
  setShowAllModalOpen(true);
};
```

### Issue: Pagination buttons missing or not working

Solution: Ensure the custom pagination controls in JobTable.jsx are preserved:

```jsx
<Box>
  <Tooltip title="Go to first page"><span><Button size="small" onClick={() => setPage(0)} disabled={page === 0}>First</Button></span></Tooltip>
  <Tooltip title="Previous page"><span><Button size="small" onClick={() => setPage(Math.max(0, page - 1))} disabled={page === 0}>Prev</Button></span></Tooltip>
  <Tooltip title="Next page"><span><Button size="small" onClick={() => setPage(Math.min(pageCount - 1, page + 1))} disabled={page >= pageCount - 1}>Next</Button></span></Tooltip>
  <Tooltip title="Go to last page"><span><Button size="small" onClick={() => setPage(pageCount - 1)} disabled={page >= pageCount - 1}>Last</Button></span></Tooltip>
  <span style={{ marginLeft: 16 }}>Page {page + 1} of {pageCount}</span>
</Box>
```

### Issue: DataGrid footer showing

Solution: Make sure these props are set on the DataGrid:

```jsx
pagination={false}
hideFooter={true}
hideFooterPagination={true}
```

And include this in the sx prop:

```jsx
'& .MuiDataGrid-footerContainer': { display: 'none' }
```

## Development Guidelines

1. Always test pagination, sorting, and "Show All" functionality after making changes
2. Preserve server-side operations for better performance with large datasets
3. Keep the DataGrid configuration consistent
4. Reload paginated data after modal operations
5. Test with both real and demo data

By following these guidelines and preserving the critical functionality described above, we can prevent recurring issues and maintain a stable application.

## Process Management with PM2

The Job Tracker application uses PM2 (Process Manager 2) to manage the backend and frontend processes. This ensures reliable operation and easy management of the application services.

### PM2 Configuration

- **ecosystem.config.json**: Contains the PM2 configuration for both frontend and backend services
- **start-dev.sh**: Script to start both backend and frontend services using PM2
- **start-backend.sh**: Script to start only the backend service

### Key PM2 Commands

- `npx pm2 start ecosystem.config.json`: Start all services defined in the ecosystem config
- `npx pm2 stop all`: Stop all running services
- `npx pm2 restart all`: Restart all services
- `npx pm2 logs`: View logs from all services
- `npx pm2 logs job-tracker-frontend`: View logs from the frontend service only
- `npx pm2 logs job-tracker-backend`: View logs from the backend service only
- `npx pm2 monit`: Open a monitoring dashboard for all services

### PM2 Benefits

1. **Process Reliability**: Automatically restarts services if they crash
2. **Consolidated Management**: Manages both frontend and backend from a single tool
3. **Unified Logging**: Centralized logs for easier debugging
4. **Environment Variables**: Manages environment variables for different services
5. **Startup Scripts**: Simplifies starting the application with proper configuration

### Important Notes

- PM2 is installed locally in the project via `package.json`
- Always use `npx pm2` to ensure you're using the project's version of PM2
- The ecosystem.config.json file should not be modified without testing
- When starting the application, always use the provided scripts (start-dev.sh or start-backend.sh)

## Troubleshooting Common Issues

### Backend Issues

1. **Database Connection Problems**
   - Check that the database file exists and has proper permissions
   - Verify the database path in `app/database.py`
   - If using SQLite, ensure the path is accessible to the application

2. **API Endpoint Errors**
   - Check the backend logs: `npx pm2 logs job-tracker-backend`
   - Verify that the endpoint exists in `app/main.py`
   - Confirm that request parameters match the expected format

3. **File Upload Issues**
   - Ensure the `uploads` directory exists and has write permissions
   - Check file size limits in both frontend and backend
   - Verify that the file type is supported

### Frontend Issues

1. **API Connection Errors**
   - Verify the API base URL in `src/config.js`
   - Check that the backend is running: `npx pm2 status`
   - Inspect network requests in browser developer tools

2. **DataGrid/Table Problems**
   - Ensure `hideFooter={true}` and `hideFooterPagination={true}` are set
   - Verify that pagination buttons are correctly implemented
   - Check that sortingMode and paginationMode are set correctly

3. **Modal and Form Issues**
   - Ensure data is being properly passed to modals
   - Verify that form submission includes all required fields
   - Check for proper handling of file uploads in forms

### Environment Setup Issues

1. **Missing Dependencies**
   - Run `npm install` in the project root
   - Check that all Python dependencies are installed: `pip install -r requirements.txt`

2. **PM2 Problems**
   - Ensure PM2 is installed: `npm list pm2`
   - Check PM2 logs for errors: `npx pm2 logs`
   - Restart PM2 processes if needed: `npx pm2 restart all`

3. **Port Conflicts**
   - Verify that ports 8005 (backend) and 5173 (frontend) are available
   - Check if other processes are using these ports: `lsof -i :8005` or `lsof -i :5173`
   - Modify port settings in start scripts if needed

Remember to run the `test_critical_functionality.sh` script after making changes to verify that key functionality is still working correctly.
