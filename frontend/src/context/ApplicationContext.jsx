/**
 * ApplicationContext.js
 * Centralized state management for job applications using React Context
 */

import React, { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';
import config from '../config';
import { 
  fetchApplications, 
  createApplication, 
  updateApplication, 
  deleteApplication, 
  fetchDemoApplications 
} from '../api';

// Create the context
const ApplicationContext = createContext();

// Custom hook to use the application context
export const useApplicationContext = () => {
  const context = useContext(ApplicationContext);
  if (!context) {
    throw new Error('useApplicationContext must be used within an ApplicationProvider');
  }
  return context;
};

// Provider component
export const ApplicationProvider = ({ children }) => {
  // Core application state
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [demoMode, setDemoMode] = useState(false);
  
  // UI state
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [followUpFilter, setFollowUpFilter] = useState(false);
  const [sortModel, setSortModel] = useState([
    { field: config.defaultSortField, sort: config.defaultSortDirection }
  ]);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });
  
  // Function to load applications based on current state
  const loadApplications = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const fetchFunction = demoMode ? fetchDemoApplications : fetchApplications;
      const result = await fetchFunction();
      
      setApplications(result);
      setLoading(false);
    } catch (err) {
      console.error('Error loading applications:', err);
      setError('Failed to load applications. Please try again.');
      setLoading(false);
      setToast({
        open: true,
        message: 'Failed to load applications',
        severity: 'error'
      });
    }
  }, [demoMode]);
  
  // Load applications on initial render or when demo mode changes
  useEffect(() => {
    loadApplications();
  }, [demoMode, loadApplications]);
  
  // CRUD operations
  const addApplication = useCallback(async (data) => {
    setLoading(true);
    try {
      const newApplication = await createApplication(data, demoMode);
      setApplications(prev => [...prev, newApplication]);
      setToast({
        open: true,
        message: 'Application added successfully',
        severity: 'success'
      });
      return newApplication;
    } catch (error) {
      console.error('Error adding application:', error);
      setToast({
        open: true,
        message: 'Failed to add application',
        severity: 'error'
      });
      throw error;
    } finally {
      setLoading(false);
    }
  }, [demoMode]);
  
  const updateApplicationItem = useCallback(async (id, data) => {
    setLoading(true);
    try {
      const updatedApplication = await updateApplication(id, data, demoMode);
      setApplications(prev => 
        prev.map(app => app.id === id ? updatedApplication : app)
      );
      setToast({
        open: true,
        message: 'Application updated successfully',
        severity: 'success'
      });
      return updatedApplication;
    } catch (error) {
      console.error('Error updating application:', error);
      setToast({
        open: true,
        message: 'Failed to update application',
        severity: 'error'
      });
      throw error;
    } finally {
      setLoading(false);
    }
  }, [demoMode]);
  
  const removeApplication = useCallback(async (id) => {
    setLoading(true);
    try {
      await deleteApplication(id, demoMode);
      setApplications(prev => prev.filter(app => app.id !== id));
      setToast({
        open: true,
        message: 'Application deleted successfully',
        severity: 'success'
      });
    } catch (error) {
      console.error('Error deleting application:', error);
      setToast({
        open: true,
        message: 'Failed to delete application',
        severity: 'error'
      });
      throw error;
    } finally {
      setLoading(false);
    }
  }, [demoMode]);
  
  // Filter applications on the client side
  const filteredApplications = useMemo(() => {
    // Ensure applications is an array before filtering
    if (!Array.isArray(applications)) {
      console.warn('Applications is not an array:', applications);
      return [];
    }
    
    return applications.filter(app => {
      // Status filter
      if (statusFilter !== 'all' && app.status !== statusFilter) {
        return false;
      }
      
      // Follow-up filter
      if (followUpFilter && !app.follow_up_required) {
        return false;
      }
      
      // Search term filter (case insensitive)
      if (searchTerm) {
        const searchLower = searchTerm.toLowerCase();
        return (
          (app.company && app.company.toLowerCase().includes(searchLower)) ||
          (app.role && app.role.toLowerCase().includes(searchLower)) ||
          (app.status && app.status.toLowerCase().includes(searchLower)) ||
          (app.notes && app.notes.toLowerCase().includes(searchLower)) ||
          (app.url && app.url.toLowerCase().includes(searchLower))
        );
      }
      
      return true;
    });
  }, [applications, statusFilter, followUpFilter, searchTerm]);
  
  // Close toast handler
  const handleCloseToast = () => {
    setToast(prev => ({ ...prev, open: false }));
  };
  
  // Context value
  const value = {
    // Data
    applications,
    filteredApplications,
    loading,
    error,
    demoMode,
    
    // CRUD operations
    loadApplications,
    addApplication,
    updateApplication: updateApplicationItem,
    deleteApplication: removeApplication,
    
    // UI state
    searchTerm,
    setSearchTerm,
    statusFilter,
    setStatusFilter,
    followUpFilter,
    setFollowUpFilter,
    sortModel,
    setSortModel,
    
    // Demo mode
    setDemoMode,
    
    // Toast
    toast,
    setToast,
    handleCloseToast
  };
  
  return (
    <ApplicationContext.Provider value={value}>
      {children}
    </ApplicationContext.Provider>
  );
};

export default ApplicationContext;
