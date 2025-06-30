/**
 * config.js
 * Centralized configuration for the Job Tracker application
 */

// Determine environment
const isDevelopment = import.meta.env.DEV || process.env.NODE_ENV === 'development';
// Read API base URL from environment variable or use default
const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8005';

// Debug logging
console.log('Config.js DEBUG:', {
  isDevelopment,
  'import.meta.env.VITE_API_BASE': import.meta.env.VITE_API_BASE,
  'apiBase': apiBase
});

const config = {
  // API configuration
  api: {
    baseURL: isDevelopment ? apiBase : window.location.origin,
    endpoints: {
      applications: '/applications',
      search: '/search',
      upload: '/upload',
      visualizations: '/visualizations',
      demo: {
        baseURL: isDevelopment ? `${apiBase}/demo` : `${window.location.origin}/demo`,
        applications: '/applications',
        search: '/search',
        visualizations: '/visualizations'
      }
    }
  },
  
  // Application defaults
  defaultPageSize: 10,
  pageSizeOptions: [10, 25, 50, 100],
  defaultSortField: 'created_at',
  defaultSortDirection: 'desc',
  
  // Status options for job applications
  statusOptions: [
    'Applied',
    'Rejected',
    'Phone Screen',
    'Technical Interview',
    'On-site Interview',
    'Offer',
    'Accepted',
    'Withdrawn'
  ],
  
  // Status colors for visualization
  statusColors: {
    'Applied': '#3498db',
    'Rejected': '#e74c3c',
    'Phone Screen': '#f39c12',
    'Technical Interview': '#9b59b6',
    'On-site Interview': '#2ecc71',
    'Offer': '#1abc9c',
    'Accepted': '#27ae60',
    'Withdrawn': '#7f8c8d'
  },
  
  // File upload configuration
  upload: {
    maxFileSize: 5 * 1024 * 1024, // 5MB
    allowedTypes: [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain'
    ],
    fileTypeLabels: {
      'application/pdf': 'PDF',
      'application/msword': 'DOC',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'DOCX',
      'text/plain': 'TXT'
    }
  }
};

export default config;