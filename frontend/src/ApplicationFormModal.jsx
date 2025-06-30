import React, { useRef } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  IconButton,
  Box,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import ApplicationForm from './ApplicationForm';

const ApplicationFormModal = ({
  open,
  onClose,
  onSubmit,
  initialData,
  demoMode,
  applicationId
}) => {
  // Create a ref to access the form component
  const formRef = useRef(null);
  
  // Function to handle the submit button click
  const handleSubmit = () => {
    if (formRef.current) {
      // Manually trigger the form submission
      formRef.current.submitForm();
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
      }}>
        <Box sx={{ typography: 'h6' }}>
          {initialData ? 'Edit Application' : 'Add New Application'}
        </Box>
        <IconButton onClick={onClose} size="small">
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      
      <DialogContent dividers sx={{ p: 3 }}>
        <ApplicationForm 
          ref={formRef}
          onSubmit={(data) => {
            // Ensure we have the required fields with proper validation
            const requiredFields = ['company', 'role', 'status'];
            let isValid = true;
            const missingFields = [];
            
            requiredFields.forEach(field => {
              if (!data[field] || (typeof data[field] === 'string' && data[field].trim() === '')) {
                console.error(`Missing required field: ${field}`);
                missingFields.push(field);
                isValid = false;
              }
            });
            
            if (isValid) {
              console.log('Form is valid, submitting data:', data);
              
              // Log the data format for debugging
              console.log('Data type:', typeof data);
              console.log('Is FormData?', data instanceof FormData);
              
              onSubmit(data);
              onClose();
            } else {
              // Alert is handled in the main App component via toast
              console.error('Form validation failed - missing required fields:', missingFields);
            }
          }}
          initialData={initialData}
          demoMode={demoMode}
          applicationId={applicationId}
          insideModal={true}
        />
      </DialogContent>
      
      <DialogActions sx={{ p: 2, borderTop: '1px solid rgba(0, 0, 0, 0.12)' }}>
        <Button onClick={onClose} variant="outlined">Cancel</Button>
        <Button 
          onClick={handleSubmit} 
          variant="contained" 
          color="primary"
        >
          Submit
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ApplicationFormModal;
