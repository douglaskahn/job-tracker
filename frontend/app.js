// Fetch and display job applications
async function fetchJobApplications() {
    try {
        const response = await fetch('http://localhost:8000/applications');
        const applications = await response.json();
        displayJobApplications(applications);
    } catch (error) {
        console.error('Error fetching job applications:', error);
    }
}

// Display job applications in the list
function displayJobApplications(applications) {
    const jobList = document.getElementById('job-list');
    jobList.innerHTML = applications.map(app => `
        <div class="border-b py-2">
            <h3 class="font-bold">${app.role}</h3>
            <p>${app.company}</p>
            <button class="text-blue-500" onclick="openModal(${app.id})">View Details</button>
        </div>
    `).join('');
}

// Open the modal
function openModal(applicationId) {
    const modal = document.getElementById('modal');
    modal.classList.remove('hidden');
    // Fetch and display application details (placeholder)
    document.getElementById('modal-content').innerHTML = `<p>Details for application ID: ${applicationId}</p>`;
}

// Close the modal
function closeModal() {
    const modal = document.getElementById('modal');
    modal.classList.add('hidden');
}

// Placeholder functions for adding, editing, and deleting applications
function addApplication() {
    console.log('Add application');
}

function editApplication(applicationId) {
    console.log('Edit application:', applicationId);
}

function deleteApplication(applicationId) {
    console.log('Delete application:', applicationId);
}

// Toggle the visibility of the application form
document.getElementById('toggle-form').addEventListener('click', () => {
    const form = document.getElementById('application-form');
    form.classList.toggle('hidden');
});

// Handle form submission
document.getElementById('application-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('company', document.getElementById('company').value);
    formData.append('role', document.getElementById('role').value);
    formData.append('job_url', document.getElementById('job-url').value);
    formData.append('status', document.getElementById('status').value);
    formData.append('application_date', document.getElementById('application-date').value);
    formData.append('met_with', document.getElementById('met-with').value);
    formData.append('notes', document.getElementById('notes').value);
    formData.append('follow_up', document.getElementById('follow-up').checked);
    formData.append('pros', document.getElementById('pros').value);
    formData.append('cons', document.getElementById('cons').value);
    formData.append('salary', document.getElementById('salary').value);
    formData.append('resume', document.getElementById('resume').files[0]);
    formData.append('cover_letter', document.getElementById('cover-letter').files[0]);

    try {
        const response = await fetch('http://localhost:8000/applications/', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Failed to submit application');
        }

        alert('Application submitted successfully!');
        document.getElementById('application-form').reset();
        document.getElementById('application-form').classList.add('hidden');
        fetchJobApplications();
    } catch (error) {
        console.error('Error submitting application:', error);
        alert('Failed to submit application. Please try again.');
    }
});

// Event listeners
document.getElementById('close-modal').addEventListener('click', closeModal);

// Initialize the app
fetchJobApplications();
