// enhancedApi.js - An enhanced API layer with caching for search operations

import axios from 'axios';
import { getApiBase } from './config';
import { 
  createCacheKey, 
  getFromCache, 
  storeInCache, 
  getPendingRequest,
  registerPendingRequest,
  abortRelatedRequests
} from './utils/searchCache';

// Create a cancelable axios instance
const axiosInstance = axios.create();

/**
 * Enhanced fetchApplications with caching, request deduplication, and cancellation
 */
export const fetchApplicationsEnhanced = async (params = {}, useCache = true) => {
  // Process parameters before creating cache key to handle potential event objects
  const processedParams = { ...params };
  
  // Log the incoming params for debugging
  console.log('enhancedApi: Processing parameters:', JSON.stringify(processedParams));
  
  // Ensure search is always a string
  if (processedParams.search === undefined || processedParams.search === null) {
    processedParams.search = '';
  } else if (typeof processedParams.search !== 'string') {
    // Handle event objects (common React issue)
    if (processedParams.search && processedParams.search.target && processedParams.search.target.value !== undefined) {
      processedParams.search = String(processedParams.search.target.value);
    } else {
      console.warn('Search parameter is not a string, converting:', typeof processedParams.search, processedParams.search);
      // If search is an object but not an event, try to get a meaningful string representation
      try {
        if (typeof processedParams.search === 'object') {
          // Try to extract value if it's in a common format
          if (processedParams.search.value !== undefined) {
            processedParams.search = String(processedParams.search.value);
          } else if (processedParams.search.query !== undefined) {
            processedParams.search = String(processedParams.search.query);
          } else if (processedParams.search.toString() !== '[object Object]') {
            processedParams.search = processedParams.search.toString();
          } else {
            processedParams.search = '';
          }
        } else {
          processedParams.search = String(processedParams.search);
        }
      } catch (e) {
        console.error('Error converting search to string:', e);
        processedParams.search = '';
      }
    }
  }
  
  // Handle event objects in statusFilter
  if (processedParams.statusFilter && processedParams.statusFilter.target) {
    if (processedParams.statusFilter.target.value !== undefined) {
      processedParams.statusFilter = processedParams.statusFilter.target.value;
    }
  }
  
  // Handle event objects in followUpFilter
  if (processedParams.followUpFilter) {
    if (processedParams.followUpFilter.target && processedParams.followUpFilter.target.checked !== undefined) {
      processedParams.followUpFilter = processedParams.followUpFilter.target.checked ? 'yes' : '';
    } else if (processedParams.followUpFilter === true) {
      processedParams.followUpFilter = 'yes';
    } else if (processedParams.followUpFilter === false) {
      processedParams.followUpFilter = '';
    }
  }
  
  // Ensure pageSize is set to a default value if not specified
  if (!processedParams.pageSize) {
    processedParams.pageSize = 10;
  }
  
  // Log the processed params for debugging
  console.log('enhancedApi: Processed parameters:', JSON.stringify(processedParams));
  
  const cacheKey = createCacheKey({
    endpoint: processedParams.isDemoMode ? 'demo' : 'applications',
    ...processedParams
  });
  
  // If there's a search term, abort any previous related searches
  if (processedParams.search && processedParams.search.length > 0) {
    abortRelatedRequests(processedParams.search.substring(0, Math.min(2, processedParams.search.length)));
  }
  
  // Check cache first if we're allowed to use it
  if (useCache) {
    const cachedData = getFromCache(cacheKey);
    if (cachedData) {
      console.log('Using cached data for query:', processedParams);
      return cachedData;
    }
  }
  
  // Check if this exact request is already in progress
  const pendingRequest = getPendingRequest(cacheKey);
  if (pendingRequest) {
    console.log('Reusing pending request for query:', processedParams);
    return pendingRequest;
  }
  
  // Create a new request
  const endpoint = processedParams.isDemoMode ? '/demo/applications/' : '/applications/';
  
  // Create a new request with cancellation token
  const controller = new AbortController();
  const fetchPromise = axiosInstance.get(
    `${getApiBase()}${endpoint}`, 
    { 
      params: processedParams,
      signal: controller.signal
    }
  )
  .then(res => {
    const data = res.data;
    console.log('API response:', data); // Debug log
    
    // Store successful result in cache
    const formattedData = { 
      applications: data.data || [], 
      totalCount: data.total || 0 
    };
    console.log('Formatted data:', formattedData); // Debug log
    storeInCache(cacheKey, formattedData);
    return formattedData;
  })
  .catch(error => {
    // Don't cache errors
    if (axios.isCancel(error)) {
      console.log('Request canceled:', processedParams);
      // Return a special value for canceled requests
      return { canceled: true };
    }
    throw error;
  });
  
  // Register this promise so we can deduplicate identical requests
  return registerPendingRequest(cacheKey, fetchPromise);
};

/**
 * Client-side search function for when we have all data locally
 */
export const performClientSideSearch = (applications, searchTerm) => {
  if (!searchTerm || !applications?.length) return applications;
  
  const lowerSearchTerm = searchTerm.toLowerCase();
  
  return applications.filter(app => {
    // Search across all text fields
    return (
      (app.company && app.company.toLowerCase().includes(lowerSearchTerm)) ||
      (app.role && app.role.toLowerCase().includes(lowerSearchTerm)) ||
      (app.status && app.status.toLowerCase().includes(lowerSearchTerm)) ||
      (app.met_with && app.met_with.toLowerCase().includes(lowerSearchTerm)) ||
      (app.notes && app.notes.toLowerCase().includes(lowerSearchTerm)) ||
      (app.pros && app.pros.toLowerCase().includes(lowerSearchTerm)) ||
      (app.cons && app.cons.toLowerCase().includes(lowerSearchTerm)) ||
      (app.salary && app.salary.toLowerCase().includes(lowerSearchTerm)) ||
      (app.url && app.url.toLowerCase().includes(lowerSearchTerm))
    );
  });
};

// Re-export all regular API functions
export * from './api';
