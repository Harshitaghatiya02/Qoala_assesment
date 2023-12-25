import React, { useState } from 'react';
import axios from 'axios';

const UploadForm = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);

    const handleChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async () => {
        if (!file) {
            console.error('No file selected.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/ocr/process', formData);
            console.log(response);

            // Call the onUploadSuccess callback to update the OCR results
            if (typeof onUploadSuccess === 'function') {
                onUploadSuccess();
            }
        } catch (error) {
            console.error('Error processing OCR:', error);
        }
    };

    return (
        <div>
            <h2>Upload Thai ID Card Image</h2>
            <input type="file" accept=".png, .jpg, .jpeg" onChange={handleChange} />
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
};

export default UploadForm;
