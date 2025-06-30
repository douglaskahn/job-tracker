import React, { useState } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, Box, Chip,
  Grid, Paper, Link, Divider, IconButton, Tooltip, Alert, CircularProgress,
  TextField, MenuItem, FormControlLabel, Checkbox
} from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import CloseIcon from '@mui/icons-material/Close';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import VisibilityIcon from '@mui/icons-material/Visibility';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import { format } from 'date-fns';
import config from './config';
import { updateApplication, uploadFile } from './api';

const statusColors = {
  'Not Yet Applied': 'default',
  'Applied': 'warning',
  'Interviewing': 'orange',
  'Offer': 'success',
  'Rejected': 'error',
  'No Longer Listed': 'default',
  'Decided not to apply': 'secondary',
  'Declined Offer': 'default',
  'Accepted': 'primary',
  'Applied / No Longer Listed': 'default',
};

const statuses = [
  'Not Yet Applied',
  'Applied',
  'Interviewing',
  'Offer',
  'Rejected',
  'No Longer Listed',
  'Decided not to apply',
  'Declined Offer',
  'Accepted',
  'Applied / No Longer Listed',
];

const FileLink = ({ file, label }) => {
  if (!file) return <Typography color="text.secondary">No {label} uploaded</Typography>;
  
  // Handle both full URLs and local file paths
  const fileUrl = file.startsWith('http') ? file : `${config.api.baseURL}/uploads/${file}`;
  
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
      <Link href={fileUrl} target="_blank" rel="noopener noreferrer">
        <IconButton size="small" color="primary">
          <FileDownloadIcon />
        </IconButton>
      </Link>
      <Link
        href={fileUrl}
        target="_blank"
        rel="noopener noreferrer"
        sx={{ textDecoration: 'none' }}
      >
        <Typography>{label}</Typography>
      </Link>
      <Tooltip title="Preview">
        <IconButton 
          size="small" 
          color="primary" 
          component={Link}
          href={fileUrl}
          target="_blank"
        >
          <VisibilityIcon />
        </IconButton>
      </Tooltip>
    </Box>
  );
};

export default function ApplicationViewModal({ open, onClose, application, onEdit, onDelete, demoMode = false }) {
  const [deleteConfirm, setDeleteConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [editedData, setEditedData] = useState({
    company: '',
    role: '',
    status: '',
    url: '',
    application_date: '',
    met_with: '',
    notes: '',
    pros: '',
    cons: '',
    salary: '',
    follow_up_required: false,
  });
  const [isSaving, setIsSaving] = useState(false);
  const [resumeFile, setResumeFile] = useState(null);
  const [coverLetterFile, setCoverLetterFile] = useState(null);

  // Initialize or update editedData when application changes
  React.useEffect(() => {
    if (application) {
      console.log('Updating modal with application data:', application);
      setEditedData({
        company: application.company || '',
        role: application.role || '',
        status: application.status || '',
        url: application.url || '',
        application_date: application.application_date || '',
        met_with: application.met_with || '',
        notes: application.notes || '',
        pros: application.pros || '',
        cons: application.cons || '',
        salary: application.salary || '',
        follow_up_required: application.follow_up_required || false,
      });
    }
  }, [application, application?.updated_at]); // Add updated_at to dependencies

  // Reset edit mode when modal closes
  React.useEffect(() => {
    if (!open) {
      setIsEditMode(false);
      setDeleteConfirm(false);
      setIsDeleting(false);
      setIsSaving(false);
    }
  }, [open]);

  // Reset files when modal closes
  React.useEffect(() => {
    if (!open) {
      setResumeFile(null);
      setCoverLetterFile(null);
    }
  }, [open]);

  if (!application) return null;

  const handleDelete = async () => {
    if (!deleteConfirm) {
      setDeleteConfirm(true);
      return;
    }
    
    try {
      setIsDeleting(true);
      await onDelete();
    } catch (error) {
      console.error('Failed to delete application:', error);
    } finally {
      setIsDeleting(false);
      setDeleteConfirm(false);
    }
  };

  const validateStateUpdate = (newData, action) => {
    console.log(`State validation (${action}):`, {
      previousState: editedData,
      newState: newData,
      changes: Object.entries(newData).reduce((acc, [key, value]) => {
        if (editedData[key] !== value) {
          acc[key] = {
            from: editedData[key],
            to: value,
            isEmpty: value === '',
            wasEmpty: editedData[key] === ''
          };
        }
        return acc;
      }, {})
    });
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;
    
    // First log the individual field change
    console.log(`Field '${name}' changing:`, { 
      oldValue: editedData[name],
      newValue,
      isEmpty: newValue === '',
      wasEmpty: editedData[name] === ''
    });

    // Create new state
    const newState = {
      ...editedData,
      [name]: newValue
    };

    // Validate state update
    validateStateUpdate(newState, 'handleChange');

    // Update state
    setEditedData(newState);
  };

  const handleFileChange = (e) => {
    const { name, files } = e.target;
    if (name === 'resume_file') setResumeFile(files[0]);
    if (name === 'cover_letter_file') setCoverLetterFile(files[0]);
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      
      // First, handle the data update
      const dataToUpdate = {
        company: editedData.company,
        role: editedData.role,
        status: editedData.status,
        url: editedData.url || null,
        application_date: editedData.application_date || null,
        met_with: editedData.met_with || null,
        notes: editedData.notes || null,
        pros: editedData.pros || null,
        cons: editedData.cons || null,
        salary: editedData.salary || null,
        follow_up_required: editedData.follow_up_required
      };

      // Validate required fields
      if (!dataToUpdate.company || !dataToUpdate.role || !dataToUpdate.status) {
        throw new Error('Missing required fields. Please fill in company, role, and status.');
      }
      
      // Send the data update
      console.log('Sending update request:', { data: dataToUpdate, applicationId: application.id });
      const updatedData = await onEdit(dataToUpdate, application.id);
      
      if (!updatedData || !updatedData.id) {
        console.error('Invalid update response:', updatedData);
        throw new Error('Server returned invalid data after update');
      }
      
      // Then handle any file uploads if needed
      if (resumeFile || coverLetterFile) {
        if (resumeFile) {
          await uploadFile(application.id, 'resume', resumeFile, demoMode);
        }
        if (coverLetterFile) {
          await uploadFile(application.id, 'cover_letter', coverLetterFile, demoMode);
        }
      }
      
      console.log('Update successful:', updatedData);
      
      // Update local state with new data
      setEditedData({
        company: updatedData.company || '',
        role: updatedData.role || '',
        status: updatedData.status || '',
        url: updatedData.url || '',
        application_date: updatedData.application_date || '',
        met_with: updatedData.met_with || '',
        notes: updatedData.notes || '',
        pros: updatedData.pros || '',
        cons: updatedData.cons || '',
        salary: updatedData.salary || '',
        follow_up_required: updatedData.follow_up_required || false,
      });
      
      // Reset form state
      setIsEditMode(false);
      setResumeFile(null);
      setCoverLetterFile(null);
      
      // Return the updated data
      return updatedData;
    } catch (error) {
      console.error('Failed to save changes:', error);
      // Show error alert within the modal
      const errorDetail = error.response?.data?.detail;
      const errorMessage = errorDetail || error.message || 'Failed to save changes';
      console.error('Save error details:', {
        error: error,
        response: error.response?.data
      });
      alert(`Failed to save: ${errorMessage}`);
      throw error; // Re-throw to propagate the error
    } finally {
      setIsSaving(false);
    }
  };

  const handleEdit = () => {
    // Ensure we have all required fields when entering edit mode
    setEditedData({
      company: application.company || '',
      role: application.role || '',
      status: application.status || '',
      url: application.url || '',
      application_date: application.application_date || '',
      met_with: application.met_with || '',
      notes: application.notes || '',
      pros: application.pros || '',
      cons: application.cons || '',
      salary: application.salary || '',
      follow_up_required: application.follow_up_required || false,
    });
    setIsEditMode(true);
  };

  const handleCancelEdit = () => {
    setIsEditMode(false);
    setEditedData({
      company: application.company,
      role: application.role,
      status: application.status,
      url: application.url || '',
      application_date: application.application_date || '',
      met_with: application.met_with || '',
      notes: application.notes || '',
      pros: application.pros || '',
      cons: application.cons || '',
      salary: application.salary || '',
      follow_up_required: application.follow_up_required || false,
    });
  };

  const formatDate = (date) => {
    if (!date) return 'N/A';
    try {
      return format(new Date(date), 'MMM d, yyyy');
    } catch (e) {
      return date;
    }
  };

  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      maxWidth="md" 
      fullWidth
      PaperProps={{ 
        sx: { 
          minHeight: '80vh',
          maxHeight: '90vh'
        } 
      }}
    >
      <DialogTitle sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        borderBottom: '1px solid rgba(0, 0, 0, 0.12)',
        pb: 1
      }}>          <Box sx={{ typography: 'h6' }}>Application Details</Box>
        <IconButton onClick={onClose} size="small">
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          {/* Header Section */}
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'flex-start',
              mb: 2,
              width: '100%'
            }}>
              <Box>
                {isEditMode ? (
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                      name="company"
                      label="Company"
                      value={editedData.company}
                      onChange={handleChange}
                      required
                      fullWidth
                    />
                    <TextField
                      name="role"
                      label="Role"
                      value={editedData.role}
                      onChange={handleChange}
                      required
                      fullWidth
                    />
                    <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                      <TextField
                        select
                        name="status"
                        label="Status"
                        value={editedData.status}
                        onChange={handleChange}
                        required
                        fullWidth
                      >
                        {statuses.map((status) => (
                          <MenuItem key={status} value={status}>
                            {status}
                          </MenuItem>
                        ))}
                      </TextField>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={editedData.follow_up_required}
                            onChange={handleChange}
                            name="follow_up_required"
                          />
                        }
                        label="Follow Up Required"
                      />
                    </Box>
                  </Box>
                ) : (
                  <>
                    <Typography variant="h5" sx={{ mb: 1 }}>{application.company}</Typography>
                    <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>{application.role}</Typography>
                    <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                      <Chip 
                        label={application.status} 
                        color={statusColors[application.status] || 'default'} 
                        sx={{ fontWeight: 'bold' }}
                      />
                      {application.follow_up_required && (
                        <Chip 
                          label="Follow Up Required" 
                          color="warning" 
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>
                  </>
                )}
              </Box>
              <Box>
                {isEditMode ? (
                  <>
                    <Tooltip title="Save Changes">
                      <IconButton onClick={handleSave} color="primary" disabled={isDeleting || isSaving}>
                        {isSaving ? <CircularProgress size={20} /> : <SaveIcon />}
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Cancel Edit">
                      <IconButton onClick={handleCancelEdit} color="default" disabled={isDeleting}>
                        <CloseIcon />
                      </IconButton>
                    </Tooltip>
                  </>
                ) : (
                  <>
                    <Tooltip title="Edit Application">
                      <IconButton onClick={handleEdit} color="primary" disabled={isDeleting}>
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title={deleteConfirm ? "Click again to confirm delete" : "Delete Application"}>
                      <IconButton 
                        onClick={handleDelete} 
                        color={deleteConfirm ? "error" : "default"}
                        disabled={isDeleting}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Tooltip>
                  </>
                )}
              </Box>
            </Box>          {deleteConfirm && (
            <Grid item xs={12}>
              <Alert 
                severity="warning"
                onClose={() => !isDeleting && setDeleteConfirm(false)}
                sx={{ mb: 2 }}
                action={isDeleting && <CircularProgress size={20} />}
              >
                {isDeleting 
                  ? "Deleting application..." 
                  : "Click the delete button again to permanently remove this application"}
              </Alert>
            </Grid>
          )}

          {/* Key Details Section */}
          <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
            <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
              <Paper elevation={0} sx={{ p: 2, backgroundColor: 'background.default', height: '100%' }}>
                <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 'bold' }}>
                  Key Details
                </Typography>
                {isEditMode ? (
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                      name="application_date"
                      label="Application Date"
                      type="date"
                      value={editedData.application_date}
                      onChange={handleChange}
                      InputLabelProps={{ shrink: true }}
                      fullWidth
                    />
                    <TextField
                      name="url"
                      label="Job Posting URL"
                      value={editedData.url}
                      onChange={handleChange}
                      fullWidth
                    />
                    <TextField
                      name="salary"
                      label="Salary"
                      value={editedData.salary}
                      onChange={handleChange}
                      fullWidth
                    />
                    <TextField
                      name="met_with"
                      label="Met With"
                      value={editedData.met_with}
                      onChange={handleChange}
                      fullWidth
                    />
                  </Box>
                ) : (
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <AccessTimeIcon color="action" fontSize="small" />
                      <Typography variant="body2">
                        <strong>Applied:</strong> {formatDate(application.application_date)}
                      </Typography>
                    </Box>
                    {application.url && (
                      <Link 
                        href={application.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        sx={{ 
                          display: 'flex',
                          alignItems: 'center',
                          gap: 1,
                          textDecoration: 'none'
                        }}
                      >
                        <Typography variant="body2">View Job Posting</Typography>
                      </Link>
                    )}
                    {application.salary && (
                      <Typography variant="body2">
                        <strong>Salary:</strong> {application.salary}
                      </Typography>
                    )}
                    {application.met_with && (
                      <Typography variant="body2">
                        <strong>Met With:</strong> {application.met_with}
                      </Typography>
                    )}
                  </Box>
                )}
              </Paper>
            </Box>

            {/* Documents Section */}
            <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
              <Paper elevation={0} sx={{ p: 2, backgroundColor: 'background.default', height: '100%' }}>
                <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 'bold' }}>
                  Documents
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {isEditMode ? (
                    <>
                      <Box>
                        <input
                          accept=".pdf,.doc,.docx,.rtf,.txt"
                          style={{ display: 'none' }}
                          id="resume-file"
                          type="file"
                          name="resume_file"
                          onChange={handleFileChange}
                        />
                        <label htmlFor="resume-file">
                          <Button variant="outlined" component="span">
                            Upload Resume
                          </Button>
                        </label>
                        {(resumeFile || application.resume_file) && (
                          <Typography variant="body2" sx={{ mt: 1 }}>
                            Current: {resumeFile ? resumeFile.name : application.resume_file}
                          </Typography>
                        )}
                      </Box>
                      <Box>
                        <input
                          accept=".pdf,.doc,.docx,.rtf,.txt"
                          style={{ display: 'none' }}
                          id="cover-letter-file"
                          type="file"
                          name="cover_letter_file"
                          onChange={handleFileChange}
                        />
                        <label htmlFor="cover-letter-file">
                          <Button variant="outlined" component="span">
                            Upload Cover Letter
                          </Button>
                        </label>
                        {(coverLetterFile || application.cover_letter_file) && (
                          <Typography variant="body2" sx={{ mt: 1 }}>
                            Current: {coverLetterFile ? coverLetterFile.name : application.cover_letter_file}
                          </Typography>
                        )}
                      </Box>
                    </>
                  ) : (
                    <>
                      <FileLink file={application.resume_file} label="Resume" />
                      <FileLink file={application.cover_letter_file} label="Cover Letter" />
                    </>
                  )}
                </Box>
              </Paper>
            </Box>
          </Box>

          {/* Notes Section */}
          <Box sx={{ width: '100%' }}>
            <Paper elevation={0} sx={{ p: 2, backgroundColor: 'background.default' }}>
              <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 'bold' }}>
                Notes & Evaluation
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {isEditMode ? (
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                      name="notes"
                      label="Notes"
                      value={editedData.notes}
                      onChange={handleChange}
                      multiline
                      rows={3}
                      fullWidth
                    />
                    <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
                      <TextField
                        name="pros"
                        label="Pros"
                        value={editedData.pros}
                        onChange={handleChange}
                        multiline
                        rows={2}
                        fullWidth
                        sx={{ flex: '1 1 300px', minWidth: 0 }}
                      />
                      <TextField
                        name="cons"
                        label="Cons"
                        value={editedData.cons}
                        onChange={handleChange}
                        multiline
                        rows={2}
                        fullWidth
                        sx={{ flex: '1 1 300px', minWidth: 0 }}
                      />
                    </Box>
                  </Box>
                ) : (
                  <>
                    <Box>
                      <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                        {application.notes || 'No notes added'}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
                      <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                        <Typography variant="subtitle2" color="success.main" sx={{ mb: 1 }}>
                          Pros
                        </Typography>
                        <Typography variant="body2">
                          {application.pros || 'None listed'}
                        </Typography>
                      </Box>
                      <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
                        <Typography variant="subtitle2" color="error.main" sx={{ mb: 1 }}>
                          Cons
                        </Typography>
                        <Typography variant="body2">
                          {application.cons || 'None listed'}
                        </Typography>
                      </Box>
                    </Box>
                  </>
                )}
              </Box>
            </Paper>
          </Box>

          {/* History Section - Placeholder for future implementation */}
          <Box sx={{ width: '100%' }}>
            <Paper elevation={0} sx={{ p: 2, backgroundColor: 'background.default' }}>
              <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 'bold' }}>
                History
              </Typography>
              <Typography color="text.secondary" variant="body2">
                History tracking will be implemented in a future update
              </Typography>
            </Paper>
          </Box>
        </Box>
        </Box>
      </DialogContent>

      <DialogActions sx={{ p: 2, borderTop: '1px solid rgba(0, 0, 0, 0.12)' }}>
        <Button onClick={onClose} variant="outlined">Close</Button>
      </DialogActions>
    </Dialog>
  );
}
