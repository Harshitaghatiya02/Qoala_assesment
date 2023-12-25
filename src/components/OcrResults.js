// OcrResults.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const OcrResults = () => {
    const [ocrResults, setOcrResults] = useState([]);
    const [serverError, setServerError] = useState(null);

    useEffect(() => {
        const fetchOcrResults = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/ocr/latest');
                // Check if the response is an array or a single object
                const results = Array.isArray(response.data.data) ? response.data.data : [response.data.data];
                setOcrResults(results);
            } catch (error) {
                console.error('Error fetching OCR results:', error.message);
                // Display the error on the component
                setServerError(error.message);
            }
        };

        fetchOcrResults();
    }, []);

    return (
        <div>
            <h2>OCR Results</h2>
            {serverError && <p style={{ color: 'red' }}>{serverError}</p>}
            <ul>
                {ocrResults.map((result) => (
                    <li key={result.id}>
                        <strong>Timestamp:</strong> {new Date(result.timestamp).toLocaleString()}<br />
                        <strong>Status:</strong> {result.status}<br />
                        <strong>Name:</strong> {result.name}<br />
                        <strong>Last Name:</strong> {result.last_name}<br />
                        <strong>Identification Number:</strong> {result.identification_number}<br />
                        {/* Add more details as needed */}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default OcrResults;
