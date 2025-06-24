import React, { useState } from 'react';
import { TextField, Button, MenuItem, Box, Checkbox, FormControlLabel } from '@mui/material';

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

const ApplicationForm = ({ onSubmit, initialData }) => {
  const [form, setForm] = useState(initialData || {
    company: '',
    role: '',
    status: '',
    url: '',
    application_date: '',
    met_with: '',
    notes: '',
    resume_file: '',
    cover_letter_file: '',
    follow_up_required: false,
    pros: '',
    cons: '',
    salary: '',
    // order_number, created_at, updated_at, id are system fields and should NOT be included
  });
  const [resumeFile, setResumeFile] = useState(null);
  const [coverLetterFile, setCoverLetterFile] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === 'checkbox') {
      setForm({ ...form, [name]: checked });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleFileChange = (e) => {
    const { name, files } = e.target;
    if (name === 'resume_file') setResumeFile(files[0]);
    if (name === 'cover_letter_file') setCoverLetterFile(files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Create FormData object
    const formData = new FormData();
    
    // First add required fields - these must be present with non-empty values
    formData.append('company', form.company || 'Untitled Company');
    formData.append('role', form.role || 'Untitled Role');
    formData.append('status', form.status || 'Not Yet Applied');
    
    // Add optional fields only if they have values
    if (form.url && form.url.trim()) formData.append('url', form.url);
    if (form.met_with && form.met_with.trim()) formData.append('met_with', form.met_with);
    if (form.notes && form.notes.trim()) formData.append('notes', form.notes);
    if (form.pros && form.pros.trim()) formData.append('pros', form.pros);
    if (form.cons && form.cons.trim()) formData.append('cons', form.cons);
    if (form.salary && form.salary.trim()) formData.append('salary', form.salary);
    
    // Handle application_date carefully - skip if empty
    if (form.application_date && form.application_date.trim()) {
      formData.append('application_date', form.application_date);
    }
    
    // Add boolean fields
    formData.append('follow_up_required', form.follow_up_required || false);
    
    // Add files only if they're selected
    if (resumeFile) {
      formData.append('resume_file', resumeFile);
    }
    if (coverLetterFile) {
      formData.append('cover_letter_file', coverLetterFile);
    }

    // Submit the form
    onSubmit(formData);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{
      background: '#fafbfc',
      borderRadius: 2,
      boxShadow: 2,
      p: 4,
      maxWidth: 800,
      mx: 'auto',
      mt: 4,
    }} encType="multipart/form-data">
      <h2 style={{ marginTop: 0, marginBottom: 24, textAlign: 'center' }}>Add New Application</h2>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField label="Company" name="company" value={form.company} onChange={handleChange} required fullWidth />
        <TextField label="Role" name="role" value={form.role} onChange={handleChange} required fullWidth />
      </Box>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField label="Job Posting URL" name="url" value={form.url} onChange={handleChange} fullWidth />
        <TextField select label="Status" name="status" value={form.status} onChange={handleChange} required fullWidth>
          {statuses.map((status) => (
            <MenuItem key={status} value={status}>{status}</MenuItem>
          ))}
        </TextField>
      </Box>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField label="Application Date" name="application_date" type="date" value={form.application_date} onChange={handleChange} slotProps={{ inputLabel: { shrink: true } }} fullWidth />
        <TextField label="Met With (Name/Role)" name="met_with" value={form.met_with} onChange={handleChange} fullWidth />
      </Box>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField label="Notes" name="notes" value={form.notes} onChange={handleChange} multiline rows={2} fullWidth />
      </Box>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Button variant="outlined" component="label" fullWidth>
          Upload Resume (PDF, DOC, DOCX)
          <input type="file" name="resume_file" hidden onChange={handleFileChange} accept=".pdf,.doc,.docx" />
        </Button>
        {resumeFile && <span style={{ alignSelf: 'center' }}>Selected: {resumeFile.name}</span>}
        <Button variant="outlined" component="label" fullWidth>
          Upload Cover Letter (PDF, DOC, DOCX)
          <input type="file" name="cover_letter_file" hidden onChange={handleFileChange} accept=".pdf,.doc,.docx" />
        </Button>
        {coverLetterFile && <span style={{ alignSelf: 'center' }}>Selected: {coverLetterFile.name}</span>}
      </Box>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <FormControlLabel
          control={<Checkbox checked={form.follow_up_required} onChange={handleChange} name="follow_up_required" />}
          label="Follow Up Required"
        />
      </Box>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField label="Pros" name="pros" value={form.pros} onChange={handleChange} multiline rows={2} fullWidth />
        <TextField label="Cons" name="cons" value={form.cons} onChange={handleChange} multiline rows={2} fullWidth />
        <TextField label="Salary" name="salary" value={form.salary} onChange={handleChange} fullWidth />
      </Box>
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
        <Button type="submit" variant="contained" size="large">Submit Application</Button>
      </Box>
    </Box>
  );
};

export default ApplicationForm;
