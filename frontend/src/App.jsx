import React, { useState, useEffect, useMemo } from 'react';
import { ThemeProvider, CssBaseline, Box, Snackbar, Alert, CircularProgress, Button } from '@mui/material';
import Sidebar from './Sidebar';
import JobTable from './JobTable';
import ApplicationForm from './ApplicationForm';
import DemoToggle from './DemoToggle';
import Dashboard from './pages/Dashboard';
import VisualizationsPage from './pages/VisualizationsPage';
import Settings from './pages/Settings';
import ExportCSV from './pages/ExportCSV';
import Calendar from './pages/Calendar';
import theme from './theme';
import {
  fetchApplications,
  createApplication,
  updateApplication,
  deleteApplication,
  fetchDemoApplications,
  fetchVisualizations,
  uploadFile,
} from './api';
import ApplicationViewModal from './ApplicationViewModal';
import ShowAllModal from './ShowAllModal';

function App() {
  const [page, setPage] = useState('applications');
  const [applications, setApplications] = useState([]);
  const [selected, setSelected] = useState(null);
  const [demoMode, setDemoMode] = useState(false);
  const [visualData, setVisualData] = useState({ overTime: {}, statusDistribution: {}, calendar: {} });
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });
  const [showForm, setShowForm] = useState(false);
  const [viewModalOpen, setViewModalOpen] = useState(false);
  const [viewedApplication, setViewedApplication] = useState(null);
  const [showAllModalOpen, setShowAllModalOpen] = useState(false);

  // Add state for search, visibleColumns, and table page to control JobTable
  const [search, setSearch] = useState('');
  const [visibleColumns, setVisibleColumns] = useState([
    'company', 'role', 'url', 'status', 'application_date', 'follow_up_required'
  ]);
  const [tablePage, setTablePage] = useState(0);

  // Add filter state for status and follow-up
  const [statusFilter, setStatusFilter] = useState('');
  const [followUpFilter, setFollowUpFilter] = useState('');
  const [error, setError] = useState('');

  // Function to directly load demo data
  const loadDemoData = async () => {
    console.log("Directly loading demo data...");
    setLoading(true);
    try {
      const demoApps = await fetchDemoApplications();
      console.log(`Directly received ${demoApps.length} demo applications`, demoApps);
      setApplications(demoApps);
      setDemoMode(true);
      setToast({ open: true, message: `Loaded ${demoApps.length} demo applications`, severity: 'success' });
    } catch (e) {
      console.error("Error directly loading demo data:", e);
      setToast({ open: true, message: 'Failed to load demo data', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const loadData = async () => {
    setLoading(true);
    try {
      if (demoMode) {
        console.log("Loading demo data in loadData()...");
        try {
          // Explicitly call the demo endpoint
          const demoApps = await fetchDemoApplications();
          console.log(`Received ${demoApps.length} demo applications in loadData()`, demoApps);
          setApplications(demoApps);
          const visualData = await fetchVisualizations(true);
          setVisualData(visualData);
        } catch (error) {
          console.error("Error loading demo data in loadData():", error);
          setToast({ open: true, message: 'Failed to load demo data', severity: 'error' });
        }
      } else {
        console.log("Loading real data in loadData()...");
        try {
          const realApps = await fetchApplications();
          console.log(`Received ${realApps.length} real applications in loadData()`, realApps);
          setApplications(realApps);
          const visualData = await fetchVisualizations(false);
          setVisualData(visualData);
        } catch (error) {
          console.error("Error loading real data in loadData():", error);
          setToast({ open: true, message: 'Failed to load data', severity: 'error' });
        }
      }
    } catch (e) {
      console.error("General error in loadData():", e);
      setToast({ open: true, message: 'Failed to load data', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log("useEffect triggered with demoMode:", demoMode);
    loadData();
    // eslint-disable-next-line
  }, [demoMode]);

  const handleFormSubmit = async (data) => {
    setLoading(true);
    try {
      if (selected) {
        await updateApplication(selected.id, data, demoMode);
        setToast({ open: true, message: 'Application updated!', severity: 'success' });
      } else {
        await createApplication(data, demoMode);
        setToast({ open: true, message: 'Application created!', severity: 'success' });
      }
      setSelected(null);
      loadData();
    } catch (e) {
      setToast({ open: true, message: 'Failed to save application', severity: 'error' });
      console.error('Submit error:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    setLoading(true);
    try {
      await deleteApplication(id, demoMode);
      setToast({ open: true, message: 'Application deleted!', severity: 'success' });
      loadData();
    } catch (e) {
      setToast({ open: true, message: 'Failed to delete application', severity: 'error' });
      console.error('Delete error:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (file) => {
    setLoading(true);
    try {
      await uploadFile(file, demoMode);
      setToast({ open: true, message: 'File uploaded!', severity: 'success' });
      loadData();
    } catch (e) {
      setToast({ open: true, message: 'Failed to upload file', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  // Clear filters handler
  const handleClearFilters = () => {
    setSearch('');
    setVisibleColumns([
      'company', 'role', 'url', 'status', 'application_date', 'follow_up_required'
    ]);
    setTablePage(0); // Reset table to first page
    setStatusFilter(''); // Clear status filter
    setFollowUpFilter(''); // Clear follow-up filter
  };

  // Filter applications before passing to JobTable
  const filteredApplications = useMemo(() => {
    return applications.filter(app => {
      let statusMatch = true;
      let followUpMatch = true;
      if (statusFilter) statusMatch = app.status === statusFilter;
      if (followUpFilter === 'yes') followUpMatch = app.follow_up_required === true;
      if (followUpFilter === 'no') followUpMatch = app.follow_up_required === false;
      return statusMatch && followUpMatch;
    });
  }, [applications, statusFilter, followUpFilter]);

  // Add missing handleView function to open the selected application in view mode
  const handleView = (row) => {
    setViewedApplication(row);
    setViewModalOpen(true);
  };

  const handleCloseViewModal = () => {
    setViewModalOpen(false);
    setViewedApplication(null);
  };

  const handleModalEdit = async (formData, id) => {
    setLoading(true);
    try {
      // Log the incoming parameters
      console.log('handleModalEdit called with:', { 
        formData: formData instanceof FormData ? Object.fromEntries(formData.entries()) : formData,
        id 
      });

      if (!id) {
        throw new Error('Application ID is required');
      }

      const currentApp = applications.find(app => app.id === id);
      if (!currentApp) {
        throw new Error(`Application not found with ID: ${id}`);
      }

      const updatedApp = await updateApplication(id, formData, demoMode);
      console.log('Update response:', updatedApp);
      
      if (!updatedApp || !updatedApp.id) {
        throw new Error('Server returned invalid data after update');
      }
      
      // Update the viewed application immediately
      setViewedApplication(updatedApp);
      
      // Update the applications list immediately
      setApplications(prevApps => {
        const newApps = prevApps.map(app => 
          app.id === updatedApp.id ? updatedApp : app
        );
        console.log('Updated applications list:', newApps);
        return newApps;
      });
      
      setToast({ open: true, message: 'Application updated!', severity: 'success' });
      
      // Refresh data from server in the background
      loadData().catch(error => {
        console.error('Error refreshing data:', error);
      });
      
      return updatedApp;
    } catch (e) {
      console.error('Failed to update:', e);
      const errorDetail = e.response?.data?.detail || 'Unknown error';
      setToast({ 
        open: true, 
        message: `Failed to update application: ${errorDetail}. Please check all required fields.`, 
        severity: 'error' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleModalDelete = async (application) => {
    await handleDelete(application.id);
    setViewModalOpen(false);
  };

  // Define columns for both JobTable and ShowAllModal
  const tableColumns = useMemo(() => [
    { field: 'company', headerName: 'Company', width: 160 },
    { field: 'role', headerName: 'Role', width: 160 },
    { field: 'status', headerName: 'Status', width: 120 },
    { field: 'url', headerName: 'Job Posting', width: 140 },
    { field: 'application_date', headerName: 'Date Applied', width: 120 },
    { field: 'met_with', headerName: 'Met With', width: 140 },
    { field: 'notes', headerName: 'Notes', width: 180 },
    { field: 'resume_file', headerName: 'Resume', width: 120 },
    { field: 'cover_letter_file', headerName: 'Cover Letter', width: 120 },
    { field: 'pros', headerName: 'Pros', width: 140 },
    { field: 'cons', headerName: 'Cons', width: 140 },
    { field: 'salary', headerName: 'Salary', width: 120 },
    { field: 'follow_up_required', headerName: 'Follow Up', width: 120 },
  ], []);

  const handleShowAll = () => {
    setShowAllModalOpen(true);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', height: '100vh' }}>
        <Sidebar
          currentPage={page}
          onNavigate={setPage}
          onShowAll={handleShowAll}  // Add this prop
        />
        <Box sx={{ flexGrow: 1, p: 3 }}>
          <Box sx={{ mb: 2 }}>
            <DemoToggle checked={demoMode} onChange={() => {
              const newDemoMode = !demoMode;
              console.log("Toggling demo mode to:", newDemoMode);
              setDemoMode(newDemoMode);
            }} />
          </Box>
          {loading && <CircularProgress sx={{ m: 2 }} />}
          {!loading && page === 'dashboard' && <Dashboard />}
          {!loading && page === 'applications' && (
            <>
              {showForm && (
                <ApplicationForm onSubmit={handleFormSubmit} initialData={selected} />
              )}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2, mt: showForm ? 4 : 0 }}>
                <Box>
                  <h2 style={{ margin: 0 }}>Applications {demoMode && <span style={{ fontSize: '16px', color: '#FF9800', marginLeft: '10px' }}>(Demo Mode)</span>}</h2>
                </Box>
                <Button variant="contained" color="primary" onClick={() => setShowForm((v) => !v)}>
                  {showForm ? 'Close Form' : 'Add Application'}
                </Button>
              </Box>
              <JobTable
                rows={filteredApplications}
                onRowClick={(params) => setSelected(params.row)}
                onView={handleView}
                onShowAll={handleShowAll}
                onClearFilters={handleClearFilters}
                search={search}
                setSearch={setSearch}
                visibleColumns={visibleColumns}
                setVisibleColumns={setVisibleColumns}
                page={tablePage}
                setPage={setTablePage}
                statusFilter={statusFilter}
                setStatusFilter={setStatusFilter}
                followUpFilter={followUpFilter}
                setFollowUpFilter={setFollowUpFilter}
              />
              <ApplicationViewModal
                open={viewModalOpen}
                onClose={handleCloseViewModal}
                application={viewedApplication}
                onEdit={handleModalEdit}
                onDelete={() => handleModalDelete(viewedApplication)}
              />
            </>
          )}
          {!loading && page === 'visualizations' && <VisualizationsPage data={visualData} />}
          {!loading && page === 'export' && <ExportCSV />}
          {!loading && page === 'calendar' && <Calendar />}
          {!loading && page === 'settings' && <Settings />}
        </Box>
      </Box>
      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({ ...toast, open: false })}>
        <Alert onClose={() => setToast({ ...toast, open: false })} severity={toast.severity} sx={{ width: '100%' }}>
          {toast.message}
        </Alert>
      </Snackbar>

      {/* Show All Modal */}
      <ShowAllModal
        open={showAllModalOpen}
        onClose={() => {
          setShowAllModalOpen(false);
          setError('');
        }}
        rows={applications}
        columns={tableColumns}
        onView={(app) => {
          setViewedApplication(app);
          setViewModalOpen(true);
          setShowAllModalOpen(false);
        }}
        visibleColumns={visibleColumns}
        setVisibleColumns={setVisibleColumns}
        onEdit={handleModalEdit}
        onDelete={(id) => {
          handleDelete(id);
          setShowAllModalOpen(false);
        }}
      />
    </ThemeProvider>
  );
}
export default App;
