# Quick Start Guide - Transport Management System

## Getting Started in 3 Simple Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
**On Windows:**
```bash
run.bat
```

**On Linux/Mac:**
```bash
./run.sh
```

**Or manually:**
```bash
python app.py
```

### Step 3: Open in Browser
Navigate to: `http://localhost:5000`

---

## First Time Setup

1. **Add Your First Vehicle**
   - Click "Add New Vehicle"
   - Enter name (e.g., "Van 1")
   - Set default rate per km (e.g., 8.00 for ₹8/km)
   - Click "Create Vehicle"

2. **Add Transport Entries**
   - Click on your vehicle card
   - Click "Add Entry"
   - Fill in:
     - Date
     - Route name
     - Kilometers driven
     - Rate (auto-filled from vehicle)
     - Extra charges (if any)
   - Click "Add Entry"

3. **Generate PDF Report**
   - Select vehicle
   - Click "Generate PDF"
   - Choose date range
   - Enter From/To addresses
   - Click "Generate PDF"

---

## File Structure

```
transport_management/
├── app.py                 # Main application (run this)
├── pdf_generator.py       # PDF creation logic
├── requirements.txt       # Dependencies
├── README.md             # Full documentation
├── QUICK_START.md        # This file
├── run.bat               # Windows launcher
├── run.sh                # Linux/Mac launcher
├── templates/
│   └── index.html        # Frontend
└── static/
    └── app.js            # JavaScript logic
```

---

## Common Issues

**Port 5000 already in use?**
Edit `app.py`, line at the end, change port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Database error?**
Delete `transport.db` file and restart the application.

**Python not found?**
Make sure Python 3.8+ is installed and in your PATH.

---

## Need Help?

See `README.md` for detailed documentation including:
- API endpoints
- Database structure
- Customization guide
- Full feature list

---

**Pro Tip:** Keep the terminal window open while using the application. You can see real-time logs there.
