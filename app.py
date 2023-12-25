from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from google.cloud import vision
import json
from flask_migrate import Migrate
from sqlalchemy.dialects.mysql import JSON


app = Flask(__name__)
# Enable CORS for all routes
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://harshita:Gogo%402710@localhost/id_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Set up Google Vision API client
vision_client = vision.ImageAnnotatorClient.from_service_account_file('/Users/gaurankmaheshwari/Desktop/Assesment/Qoala_assesment/qoala-assesment-9b3d79421139.json')

class OCRRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(20))
    ocr_result = db.Column(JSON)
    name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    identification_number = db.Column(db.String(20))
    date_of_issue = db.Column(db.Date)
    date_of_expiry = db.Column(db.Date)
    date_of_birth = db.Column(db.Date)

# Create a new OCR record
@app.route('/api/ocr', methods=['POST'])
def create_ocr_record():
    try:
        # Get the uploaded image file
        file = request.files['file']

        # Process image using Google Vision API
        content = file.read()
        image = vision.Image(content=content)
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations

        # Extract relevant data from OCR result
        ocr_result = {
            "text": texts[0].description if texts else "",
            # Add more fields as needed
        }

        # Create a new OCR record
        new_ocr_record = OCRRecord(
            status="success",
            ocr_result=json.dumps(ocr_result),
            # Add more fields as needed
        )

        # Save the record to the MySQL database
        db.session.add(new_ocr_record)
        db.session.commit()

        # Return the JSON response with CORS headers and correct content type
        return jsonify({"status": "success", "message": 'OCR Recorded successfully'}), 200, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

    except Exception as e:
        # Return the JSON response with CORS headers and correct content type
        return jsonify({"status": "error", "message": str(e)}), 500, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}
    
# Retrieve and display OCR data based on filters
@app.route('/api/ocr/display', methods=['GET'])
def get_ocr_records():
    try:
        # Retrieve and display all OCR records
        ocr_records = OCRRecord.query.all()

        # Convert the query result to a list of dictionaries
        ocr_records_list = [
            {
                "id": record.id,
                "timestamp": record.timestamp.isoformat(),
                "status": record.status,
                "ocr_result": json.loads(record.ocr_result),
                "name": record.name,
                "last_name": record.last_name,
                "identification_number": record.identification_number,
                "date_of_issue": record.date_of_issue.isoformat(),
                "date_of_expiry": record.date_of_expiry.isoformat(),
                "date_of_birth": record.date_of_birth.isoformat(),
            }
            for record in ocr_records
        ]

        # Return the JSON response with CORS headers and correct content type
        return jsonify({"status": "success", "data": ocr_records_list}), 200, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

    except Exception as e:
        # Return the JSON response with CORS headers and correct content type
        return jsonify({"status": "error", "message": str(e)}), 500, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

# Update an existing OCR record
@app.route('/api/ocr/<int:id>', methods=['PUT'])
def update_ocr_record(id):
    try:
        data = request.json

        # Find the OCR record by id
        ocr_record = OCRRecord.query.get(id)

        if not ocr_record:
            return jsonify({"status": "error", "message": "OCR record not found"}), 404, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

        # Update the OCR record fields
        ocr_record.status = data.get('status', ocr_record.status)
        ocr_record.ocr_result = data.get('ocr_result', ocr_record.ocr_result)
        ocr_record.name = data.get('name', ocr_record.name)
        ocr_record.last_name = data.get('last_name', ocr_record.last_name)
        ocr_record.identification_number = data.get('identification_number', ocr_record.identification_number)
        ocr_record.date_of_issue = data.get('date_of_issue', ocr_record.date_of_issue)
        ocr_record.date_of_expiry = data.get('date_of_expiry', ocr_record.date_of_expiry)
        ocr_record.date_of_birth = data.get('date_of_birth', ocr_record.date_of_birth)

        # Commit the changes to the MySQL database
        db.session.commit()

        # Return the JSON response with CORS headers and correct content type
        return jsonify({"status": "success", "message": "OCR record updated successfully"}), 200, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

    except Exception as e:
        # Return the JSON response with CORS headers and correct content type
        return jsonify({"status": "error", "message": str(e)}), 500, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

# Delete an OCR record from the MySQL database
@app.route('/api/ocr/<int:id>', methods=['DELETE'])
def delete_ocr_record(id):
    try:
        # Find the OCR record by id
        ocr_record = OCRRecord.query.get(id)

        if not ocr_record:
            return jsonify({"status": "error", "message": "OCR record not found"}), 404, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

        # Soft delete the OCR record (update status or flag)
        ocr_record.status = 'deleted'
        db.session.commit()

        # Return the JSON response with CORS headers and correct content type
        return jsonify({"status": "success", "message": "OCR record deleted successfully"}), 200, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

    except Exception as e:
        # Return the JSON response with CORS headers and correct content type
        return jsonify({"status": "error", "message": str(e)}), 500, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

# Process OCR
@app.route('/api/ocr/process', methods=['POST'])
def process_ocr():
    try:
        # Process image using Google Vision API
        file = request.files['file']
        content = file.read()
        image = vision.Image(content=content)
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations

        # Extract relevant data from OCR result
        ocr_result = {
            "text": texts[0].description if texts else "",
        }

        # Create a new OCR record
        new_ocr_record = OCRRecord(
            status="success",
            ocr_result=json.dumps(ocr_result),
        )

        # Save the record to the MySQL database
        db.session.add(new_ocr_record)
        db.session.commit()

        # Return the JSON response with CORS headers and correct content type
        return jsonify({"status": "success", "message": "OCR record created successfully"}), 200, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

    except FileNotFoundError as e:
        return jsonify({"status": "error", "message": f"File not found: {str(e)}"}), 400, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error processing OCR: {str(e)}")

        # Return a generic error response
        return jsonify({"status": "error", "message": "Internal server error"}), 500, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'http://localhost:3000'}


@app.route('/api/ocr/all', methods=['GET'])
def get_all_ocr_records():
    try:
        # Retrieve and display all OCR records
        ocr_records = OCRRecord.query.all().order_by(OCRRecord.timestamp.desc())

        # Convert the query result to a list of dictionaries
        ocr_records_list = [
            {
                "id": record.id,
                "timestamp": record.timestamp.isoformat() if record.timestamp else None,
                "status": record.status,
                "ocr_result": json.loads(record.ocr_result),
                "name": record.name if record.name else None,
                "last_name": record.last_name if record.last_name else None,
                "identification_number": record.identification_number if record.identification_number else None,
                "date_of_issue": record.date_of_issue.isoformat() if record.date_of_issue else None,
                "date_of_expiry": record.date_of_expiry.isoformat() if record.date_of_expiry else None,
                "date_of_birth": record.date_of_birth.isoformat() if record.date_of_birth else None,
            }
            for record in ocr_records
        ]

        # Return the JSON response
        return jsonify({"status": "success", "data": ocr_records_list}), 200

    except Exception as e:
        # Log the error
        app.logger.error(f"Error fetching OCR records: {str(e)}")
        # Return the JSON response with an error message
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/ocr/latest', methods=['GET'])
def get_latest_ocr_result():
    try:
        # Retrieve the latest OCR record
        latest_record = OCRRecord.query.order_by(OCRRecord.timestamp.desc()).first()

        # Convert the result to a dictionary
        ocr_result = {
            "id": latest_record.id,
            "timestamp": latest_record.timestamp.isoformat() if latest_record.timestamp else None,
            "status": latest_record.status,
            "name": latest_record.name,
            "last_name": latest_record.last_name,
            "identification_number": latest_record.identification_number,
            "date_of_issue": latest_record.date_of_issue.isoformat() if latest_record.date_of_issue else None,
            "date_of_expiry": latest_record.date_of_expiry.isoformat() if latest_record.date_of_expiry else None,
            "date_of_birth": latest_record.date_of_birth.isoformat() if latest_record.date_of_birth else None,
        }

        # Return the JSON response
        return jsonify({"status": "success", "data": ocr_result}), 200, {'Access-Control-Allow-Origin': 'http://localhost:3000'}

    except Exception as e:
        # Log the error
        app.logger.error(f"Error fetching latest OCR result: {str(e)}")
        # Return the JSON response with an error message
        return jsonify({"status": "error", "message": str(e)}), 500, {'Access-Control-Allow-Origin': 'http://localhost:3000'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
