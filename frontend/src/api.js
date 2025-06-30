import axios from 'axios';
import config from './config';

// Use the baseURL from config instead of hardcoding
const API_BASE = config.api.baseURL;

export const fetchApplications = async () => {
  const res = await axios.get(`${API_BASE}/applications/`);
  return res.data;
};

export const createApplication = async (data, isDemoMode = false) => {
  try {
    // If data is FormData, set the correct headers for file upload
    const isFormData = (typeof FormData !== 'undefined') && data instanceof FormData;
    const axiosConfig = isFormData ? { headers: { 'Content-Type': 'multipart/form-data' } } : {};
    const endpoint = isDemoMode 
      ? `${API_BASE}/demo/applications/` 
      : `${API_BASE}/applications/`;
    
    console.log('Creating application with isDemoMode:', isDemoMode);
    console.log('Endpoint:', endpoint);
    
    // Log the form data we're sending
    if (isFormData) {
      console.log('Form data entries:');
      for (let pair of data.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
      }
    } else {
      console.log('Data:', data);
    }
    
    console.log('About to send POST request to:', endpoint);
    const res = await axios.post(endpoint, data, axiosConfig);
    console.log('Create application response:', res.data);
    return res.data;
  } catch (error) {
    console.error('Error creating application:', error);
    console.error('Error response data:', error.response?.data);
    console.error('Error response status:', error.response?.status);
    console.error('Error response headers:', error.response?.headers);
    throw error;
  }
};

export const updateApplication = async (id, data, isDemoMode = false) => {
  try {
    // Validate inputs
    if (!id) throw new Error('Application ID is required');
    if (!data) throw new Error('Update data is required');

    const endpoint = isDemoMode 
      ? `${API_BASE}/demo/applications/${id}` 
      : `${API_BASE}/applications/${id}`;

    console.log('Sending PATCH request:', {
      url: endpoint,
      data
    });

    const res = await axios.patch(endpoint, data);

    if (!res.data || !res.data.id) {
      console.error('Invalid response data:', res.data);
      throw new Error('Server returned invalid data');
    }

    console.log('Update response:', res.data);
    return res.data;
  } catch (error) {
    console.error('API update error:', error.response?.data || error.message);
    throw error;
  }
};

export const deleteApplication = async (id, isDemoMode = false) => {
  const endpoint = isDemoMode 
    ? `${API_BASE}/demo/applications/${id}/` 
    : `${API_BASE}/applications/${id}/`;
  await axios.delete(endpoint);
};

export const uploadFile = async (applicationId, fileType, file, isDemoMode = false) => {
  if (!['resume', 'cover_letter'].includes(fileType)) {
    throw new Error('Invalid file type. Must be "resume" or "cover_letter"');
  }

  const formData = new FormData();
  formData.append('file', file);
  
  console.log(`Uploading ${fileType} for application ${applicationId}`);
  
  const endpoint = isDemoMode
    ? `${API_BASE}/demo/applications/${applicationId}/files/${fileType}`
    : `${API_BASE}/applications/${applicationId}/files/${fileType}`;

  const res = await axios.post(
    endpoint,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );
  
  return res.data;
};

export const fetchDemoApplications = async () => {
  console.log("Fetching demo applications from:", `${API_BASE}/demo/applications/`);
  try {
    const res = await axios.get(`${API_BASE}/demo/applications/`);
    console.log("Demo applications response:", res.data);
    return res.data;
  } catch (error) {
    console.error("Error fetching demo applications:", error);
    throw error;
  }
};

export const fetchVisualizations = async (isDemoMode = false) => {
  const endpoint = isDemoMode 
    ? `${API_BASE}/demo/visualizations/` 
    : `${API_BASE}/visualizations/`;
  const res = await axios.get(endpoint);
  return res.data;
};
