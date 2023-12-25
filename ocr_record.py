from backend import db

# Create a new OCR record model
db.create_all()

class OCRRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(20))
    ocr_result = db.Column(db.String(500))
    name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    identification_number = db.Column(db.String(20))
    date_of_issue = db.Column(db.Date)
    date_of_expiry = db.Column(db.Date)
    date_of_birth = db.Column(db.Date)

   
