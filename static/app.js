// Global variables
let currentVehicleId = null;
let vehicles = [];
let entries = [];

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadVehicles();
    
    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('entryDate').value = today;
    
    // Form submissions
    document.getElementById('addVehicleForm').addEventListener('submit', handleAddVehicle);
    document.getElementById('editVehicleForm').addEventListener('submit', handleEditVehicle);
    document.getElementById('addEntryForm').addEventListener('submit', handleAddEntry);
    document.getElementById('editEntryForm').addEventListener('submit', handleEditEntry);
    document.getElementById('generatePdfForm').addEventListener('submit', handleGeneratePdf);
});

// API calls
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API call error:', error);
        showMessage('An error occurred. Please try again.', 'error');
        throw error;
    }
}

// Vehicle functions
async function loadVehicles() {
    vehicles = await apiCall('/api/vehicles');
    displayVehicles();
}

function displayVehicles() {
    const vehicleList = document.getElementById('vehicleList');
    
    if (vehicles.length === 0) {
        vehicleList.innerHTML = '<div class="no-data">No vehicles added yet. Click "Add New Vehicle" to get started.</div>';
        return;
    }
    
    vehicleList.innerHTML = vehicles.map(vehicle => `
        <div class="vehicle-card ${currentVehicleId === vehicle.id ? 'active' : ''}" 
             onclick="selectVehicle(${vehicle.id})">
            <h3>${vehicle.name}</h3>
            <p>Default Rate: ₹${vehicle.default_rate.toFixed(2)}/km</p>
            <p style="font-size: 12px; color: #999;">Created: ${new Date(vehicle.created_at).toLocaleDateString()}</p>
        </div>
    `).join('');
}

async function selectVehicle(vehicleId) {
    currentVehicleId = vehicleId;
    const vehicle = vehicles.find(v => v.id === vehicleId);
    
    document.getElementById('vehicleTitle').textContent = `${vehicle.name} - Details`;
    document.getElementById('vehicleDetails').classList.remove('hidden');
    
    // Set default rate for new entries
    document.getElementById('rate').value = vehicle.default_rate;
    
    displayVehicles();
    await loadEntries();
}

async function handleAddVehicle(e) {
    e.preventDefault();
    
    const data = {
        name: document.getElementById('vehicleName').value,
        default_rate: parseFloat(document.getElementById('defaultRate').value)
    };
    
    const result = await apiCall('/api/vehicles', 'POST', data);
    showMessage(result.message, 'success');
    closeModal('addVehicleModal');
    document.getElementById('addVehicleForm').reset();
    await loadVehicles();
}

function showEditVehicleModal() {
    if (!currentVehicleId) return;
    
    const vehicle = vehicles.find(v => v.id === currentVehicleId);
    document.getElementById('editVehicleName').value = vehicle.name;
    document.getElementById('editDefaultRate').value = vehicle.default_rate;
    
    document.getElementById('editVehicleModal').style.display = 'block';
}

async function handleEditVehicle(e) {
    e.preventDefault();
    
    const data = {
        name: document.getElementById('editVehicleName').value,
        default_rate: parseFloat(document.getElementById('editDefaultRate').value)
    };
    
    const result = await apiCall(`/api/vehicles/${currentVehicleId}`, 'PUT', data);
    showMessage(result.message, 'success');
    closeModal('editVehicleModal');
    await loadVehicles();
    await selectVehicle(currentVehicleId);
}

async function deleteVehicle() {
    if (!currentVehicleId) return;
    
    if (!confirm('Are you sure you want to delete this vehicle? All entries will be deleted as well.')) {
        return;
    }
    
    const result = await apiCall(`/api/vehicles/${currentVehicleId}`, 'DELETE');
    showMessage(result.message, 'success');
    
    currentVehicleId = null;
    document.getElementById('vehicleDetails').classList.add('hidden');
    await loadVehicles();
}

// Entry functions
async function loadEntries() {
    if (!currentVehicleId) return;
    
    entries = await apiCall(`/api/vehicles/${currentVehicleId}/entries`);
    displayEntries();
    displayStats();
}

function displayEntries() {
    const tbody = document.getElementById('entriesBody');
    
    if (entries.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="no-data">No entries yet. Click "Add Entry" to get started.</td></tr>';
        return;
    }
    
    tbody.innerHTML = entries.map(entry => `
        <tr>
            <td>${new Date(entry.date).toLocaleDateString()}</td>
            <td>${entry.route_name}</td>
            <td>${entry.km_driven.toFixed(2)}</td>
            <td>₹${entry.rate.toFixed(2)}</td>
            <td>₹${entry.amount.toFixed(2)}</td>
            <td>₹${entry.extra.toFixed(2)}</td>
            <td><strong>₹${entry.total_amount.toFixed(2)}</strong></td>
            <td class="actions">
                <button class="btn btn-small btn-secondary" onclick="showEditEntryModal(${entry.id})">Edit</button>
                <button class="btn btn-small btn-danger" onclick="deleteEntry(${entry.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function displayStats() {
    if (entries.length === 0) {
        document.getElementById('statsSection').innerHTML = '';
        return;
    }
    
    const totalKm = entries.reduce((sum, e) => sum + e.km_driven, 0);
    const totalAmount = entries.reduce((sum, e) => sum + e.total_amount, 0);
    const totalExtra = entries.reduce((sum, e) => sum + e.extra, 0);
    
    document.getElementById('statsSection').innerHTML = `
        <div class="stat-card">
            <h4>Total Entries</h4>
            <p>${entries.length}</p>
        </div>
        <div class="stat-card">
            <h4>Total Kilometers</h4>
            <p>${totalKm.toFixed(2)}</p>
        </div>
        <div class="stat-card">
            <h4>Total Extra Charges</h4>
            <p>₹${totalExtra.toFixed(2)}</p>
        </div>
        <div class="stat-card">
            <h4>Grand Total</h4>
            <p>₹${totalAmount.toFixed(2)}</p>
        </div>
    `;
}

function calculateAmount() {
    const km = parseFloat(document.getElementById('kmDriven').value) || 0;
    const rate = parseFloat(document.getElementById('rate').value) || 0;
    const extra = parseFloat(document.getElementById('extra').value) || 0;
    
    const amount = km * rate;
    const total = amount + extra;
    
    document.getElementById('amount').value = amount.toFixed(2);
    document.getElementById('totalAmount').value = total.toFixed(2);
}

function calculateEditAmount() {
    const km = parseFloat(document.getElementById('editKmDriven').value) || 0;
    const rate = parseFloat(document.getElementById('editRate').value) || 0;
    const extra = parseFloat(document.getElementById('editExtra').value) || 0;
    
    const amount = km * rate;
    const total = amount + extra;
    
    document.getElementById('editAmount').value = amount.toFixed(2);
    document.getElementById('editTotalAmount').value = total.toFixed(2);
}

async function handleAddEntry(e) {
    e.preventDefault();
    
    const data = {
        date: document.getElementById('entryDate').value,
        route_name: document.getElementById('routeName').value,
        km_driven: document.getElementById('kmDriven').value,
        rate: document.getElementById('rate').value,
        extra: document.getElementById('extra').value
    };
    
    const result = await apiCall(`/api/vehicles/${currentVehicleId}/entries`, 'POST', data);
    showMessage(result.message, 'success');
    closeModal('addEntryModal');
    document.getElementById('addEntryForm').reset();
    
    // Reset to defaults
    const vehicle = vehicles.find(v => v.id === currentVehicleId);
    document.getElementById('rate').value = vehicle.default_rate;
    document.getElementById('extra').value = 0;
    document.getElementById('entryDate').value = new Date().toISOString().split('T')[0];
    
    await loadEntries();
}

function showEditEntryModal(entryId) {
    const entry = entries.find(e => e.id === entryId);
    
    document.getElementById('editEntryId').value = entry.id;
    document.getElementById('editEntryDate').value = entry.date;
    document.getElementById('editRouteName').value = entry.route_name;
    document.getElementById('editKmDriven').value = entry.km_driven;
    document.getElementById('editRate').value = entry.rate;
    document.getElementById('editExtra').value = entry.extra;
    document.getElementById('editAmount').value = entry.amount;
    document.getElementById('editTotalAmount').value = entry.total_amount;
    
    document.getElementById('editEntryModal').style.display = 'block';
}

async function handleEditEntry(e) {
    e.preventDefault();
    
    const entryId = document.getElementById('editEntryId').value;
    const data = {
        date: document.getElementById('editEntryDate').value,
        route_name: document.getElementById('editRouteName').value,
        km_driven: document.getElementById('editKmDriven').value,
        rate: document.getElementById('editRate').value,
        extra: document.getElementById('editExtra').value
    };
    
    const result = await apiCall(`/api/vehicles/${currentVehicleId}/entries/${entryId}`, 'PUT', data);
    showMessage(result.message, 'success');
    closeModal('editEntryModal');
    await loadEntries();
}

async function deleteEntry(entryId) {
    if (!confirm('Are you sure you want to delete this entry?')) {
        return;
    }
    
    const result = await apiCall(`/api/vehicles/${currentVehicleId}/entries/${entryId}`, 'DELETE');
    showMessage(result.message, 'success');
    await loadEntries();
}

// PDF Generation
async function handleGeneratePdf(e) {
    e.preventDefault();
    
    const data = {
        start_date: document.getElementById('startDate').value,
        end_date: document.getElementById('endDate').value,
        from_address: document.getElementById('fromAddress').value,
        to_address: document.getElementById('toAddress').value
    };
    
    try {
        const response = await fetch(`/api/vehicles/${currentVehicleId}/generate-pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            showMessage(error.error || 'Failed to generate PDF', 'error');
            return;
        }
        
        // Download the PDF
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `transport_report_${data.start_date}_to_${data.end_date}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showMessage('PDF generated successfully!', 'success');
        closeModal('generatePdfModal');
        document.getElementById('generatePdfForm').reset();
    } catch (error) {
        console.error('PDF generation error:', error);
        showMessage('Failed to generate PDF. Please try again.', 'error');
    }
}

// Modal functions
function showAddVehicleModal() {
    document.getElementById('addVehicleModal').style.display = 'block';
}

function showAddEntryModal() {
    if (!currentVehicleId) {
        showMessage('Please select a vehicle first', 'error');
        return;
    }
    document.getElementById('addEntryModal').style.display = 'block';
}

function showGeneratePdfModal() {
    if (!currentVehicleId) {
        showMessage('Please select a vehicle first', 'error');
        return;
    }
    
    // Set default date range (current month)
    const now = new Date();
    const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
    const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
    
    document.getElementById('startDate').value = firstDay.toISOString().split('T')[0];
    document.getElementById('endDate').value = lastDay.toISOString().split('T')[0];
    
    document.getElementById('generatePdfModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Message display
function showMessage(message, type) {
    const messageDiv = document.getElementById('messageDiv');
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}
