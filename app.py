from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from pdf_generator import generate_pdf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

db = SQLAlchemy(app)

# Database Models
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    default_rate = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    entries = db.relationship('TransportEntry', backref='vehicle', lazy=True, cascade='all, delete-orphan')

class TransportEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    route_name = db.Column(db.String(200), nullable=False)
    km_driven = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    extra = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        'id': v.id,
        'name': v.name,
        'default_rate': v.default_rate,
        'created_at': v.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for v in vehicles])

@app.route('/api/vehicles', methods=['POST'])
def create_vehicle():
    data = request.json
    vehicle = Vehicle(
        name=data['name'],
        default_rate=data.get('default_rate', 0.0)
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({
        'id': vehicle.id,
        'name': vehicle.name,
        'default_rate': vehicle.default_rate,
        'message': 'Vehicle created successfully'
    }), 201

@app.route('/api/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.json
    vehicle.name = data.get('name', vehicle.name)
    vehicle.default_rate = data.get('default_rate', vehicle.default_rate)
    db.session.commit()
    return jsonify({
        'id': vehicle.id,
        'name': vehicle.name,
        'default_rate': vehicle.default_rate,
        'message': 'Vehicle updated successfully'
    })

@app.route('/api/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle deleted successfully'})

@app.route('/api/vehicles/<int:vehicle_id>/entries', methods=['GET'])
def get_entries(vehicle_id):
    entries = TransportEntry.query.filter_by(vehicle_id=vehicle_id).order_by(TransportEntry.date.desc()).all()
    return jsonify([{
        'id': e.id,
        'date': e.date.strftime('%Y-%m-%d'),
        'route_name': e.route_name,
        'km_driven': e.km_driven,
        'rate': e.rate,
        'amount': e.amount,
        'extra': e.extra,
        'total_amount': e.total_amount
    } for e in entries])

@app.route('/api/vehicles/<int:vehicle_id>/entries', methods=['POST'])
def create_entry(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.json
    
    # Calculate amount and total
    km_driven = float(data['km_driven'])
    rate = float(data['rate'])
    extra = float(data.get('extra', 0.0))
    amount = km_driven * rate
    total_amount = amount + extra
    
    entry = TransportEntry(
        vehicle_id=vehicle_id,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        route_name=data['route_name'],
        km_driven=km_driven,
        rate=rate,
        amount=amount,
        extra=extra,
        total_amount=total_amount
    )
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({
        'id': entry.id,
        'date': entry.date.strftime('%Y-%m-%d'),
        'route_name': entry.route_name,
        'km_driven': entry.km_driven,
        'rate': entry.rate,
        'amount': entry.amount,
        'extra': entry.extra,
        'total_amount': entry.total_amount,
        'message': 'Entry added successfully'
    }), 201

@app.route('/api/vehicles/<int:vehicle_id>/entries/<int:entry_id>', methods=['PUT'])
def update_entry(vehicle_id, entry_id):
    entry = TransportEntry.query.filter_by(id=entry_id, vehicle_id=vehicle_id).first_or_404()
    data = request.json
    
    # Update fields
    entry.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    entry.route_name = data['route_name']
    entry.km_driven = float(data['km_driven'])
    entry.rate = float(data['rate'])
    entry.extra = float(data.get('extra', 0.0))
    
    # Recalculate amounts
    entry.amount = entry.km_driven * entry.rate
    entry.total_amount = entry.amount + entry.extra
    
    db.session.commit()
    
    return jsonify({
        'id': entry.id,
        'date': entry.date.strftime('%Y-%m-%d'),
        'route_name': entry.route_name,
        'km_driven': entry.km_driven,
        'rate': entry.rate,
        'amount': entry.amount,
        'extra': entry.extra,
        'total_amount': entry.total_amount,
        'message': 'Entry updated successfully'
    })

@app.route('/api/vehicles/<int:vehicle_id>/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(vehicle_id, entry_id):
    entry = TransportEntry.query.filter_by(id=entry_id, vehicle_id=vehicle_id).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Entry deleted successfully'})

@app.route('/api/vehicles/<int:vehicle_id>/generate-pdf', methods=['POST'])
def generate_vehicle_pdf(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.json
    
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    from_address = data.get('from_address', '')
    to_address = data.get('to_address', '')
    
    # Get entries in date range
    entries = TransportEntry.query.filter(
        TransportEntry.vehicle_id == vehicle_id,
        TransportEntry.date >= start_date,
        TransportEntry.date <= end_date
    ).order_by(TransportEntry.date).all()
    
    if not entries:
        return jsonify({'error': 'No entries found for the selected date range'}), 404
    
    # Generate PDF
    pdf_path = generate_pdf(vehicle, entries, from_address, to_address, start_date, end_date)
    
    return send_file(pdf_path, as_attachment=True, download_name=f'{vehicle.name}_report_{start_date}_to_{end_date}.pdf')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
