# Transport Management System

A web-based transport management application for tracking vehicle entries, routes, kilometers driven, and generating PDF reports.

## Features

- **Multi-Vehicle Support**: Create and manage multiple vehicles
- **Entry Management**: Add, edit, and delete transport entries
- **Automatic Calculations**: Auto-calculate amounts based on km and rate
- **PDF Report Generation**: Generate professional PDF reports with custom date ranges
- **Dashboard Statistics**: View total entries, kilometers, and amounts at a glance
- **Responsive Design**: Works on mobile, tablet, and desktop devices
- **SQLite Database**: Persistent data storage

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **PDF Generation**: ReportLab

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Extract the ZIP file
Extract the project files to your desired location.

### Step 2: Install Dependencies
Open terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### 1. Adding a Vehicle
1. Click on "Add New Vehicle" button
2. Enter vehicle name (e.g., "Van 1", "Truck A")
3. Set default rate per kilometer (optional)
4. Click "Create Vehicle"

### 2. Adding Transport Entries
1. Select a vehicle from the dashboard
2. Click "Add Entry" button
3. Fill in the details:
   - **Date**: Select the date of transport
   - **Route Name**: Enter the route (e.g., "Chennai to Bangalore")
   - **Kilometers Driven**: Enter the distance
   - **Rate**: Enter rate per km (auto-filled from vehicle default)
   - **Extra**: Enter any additional charges (optional)
   - **Amount & Total**: Auto-calculated
4. Click "Add Entry"

### 3. Editing Entries
1. Click "Edit" button on any entry row
2. Modify the required fields
3. Click "Update Entry"

### 4. Generating PDF Reports
1. Select a vehicle
2. Click "Generate PDF" button
3. Select date range (start date to end date)
4. Enter "From" address (sender details)
5. Enter "To" address (recipient details)
6. Click "Generate PDF"
7. PDF will be downloaded automatically

### 5. Managing Vehicles
- **Edit Vehicle**: Click "Edit Vehicle" to update name or default rate
- **Delete Vehicle**: Click "Delete Vehicle" to remove (Warning: This deletes all entries too)

## Database Structure

### Vehicle Table
- `id`: Primary key
- `name`: Vehicle name
- `default_rate`: Default rate per kilometer
- `created_at`: Creation timestamp

### TransportEntry Table
- `id`: Primary key
- `vehicle_id`: Foreign key to Vehicle
- `date`: Entry date
- `route_name`: Route name
- `km_driven`: Kilometers driven
- `rate`: Rate per kilometer
- `amount`: Calculated amount (km × rate)
- `extra`: Extra charges
- `total_amount`: Total amount (amount + extra)
- `created_at`: Creation timestamp

## File Structure

```
transport_management/
├── app.py                  # Main Flask application
├── pdf_generator.py        # PDF generation logic
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── transport.db           # SQLite database (created automatically)
├── generated_pdfs/        # PDF output folder (created automatically)
├── templates/
│   └── index.html         # Main HTML template
└── static/
    └── app.js             # JavaScript application logic
```

## API Endpoints

### Vehicles
- `GET /api/vehicles` - Get all vehicles
- `POST /api/vehicles` - Create new vehicle
- `PUT /api/vehicles/<id>` - Update vehicle
- `DELETE /api/vehicles/<id>` - Delete vehicle

### Entries
- `GET /api/vehicles/<id>/entries` - Get all entries for a vehicle
- `POST /api/vehicles/<id>/entries` - Create new entry
- `PUT /api/vehicles/<id>/entries/<entry_id>` - Update entry
- `DELETE /api/vehicles/<id>/entries/<entry_id>` - Delete entry

### PDF Generation
- `POST /api/vehicles/<id>/generate-pdf` - Generate PDF report

## Customization

### Changing Port
Edit `app.py` and modify the last line:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

### Modifying PDF Layout
Edit `pdf_generator.py` to customize:
- PDF page size
- Table styling
- Header/footer content
- Colors and fonts

### Updating UI
- Edit `templates/index.html` for HTML structure and CSS styling
- Edit `static/app.js` for functionality changes

## Troubleshooting

### Database Issues
If you encounter database errors, delete `transport.db` and restart the application. A new database will be created automatically.

### PDF Generation Fails
Ensure ReportLab is installed correctly:
```bash
pip install reportlab --upgrade
```

### Port Already in Use
Change the port number in `app.py` or stop the process using port 5000.

## Security Notes

- This is a local development application
- For production use, change the `SECRET_KEY` in `app.py`
- Add authentication and authorization
- Use environment variables for sensitive data
- Enable HTTPS

## Future Enhancements

Possible additions:
- User authentication
- Export to Excel
- Email reports
- Fuel cost tracking
- Maintenance records
- Driver management
- Route optimization

## Support

For modifications or issues, you can:
1. Review the code comments in each file
2. Check API endpoints documentation above
3. Modify and test changes in development mode (debug=True)

## License

This project is for educational and commercial use.

---

**Developed for**: Transport Management
**Version**: 1.0
**Date**: February 2026
