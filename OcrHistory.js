// OcrHistory.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const OcrHistory = () => {
    const [ocrHistory, setOcrHistory] = useState([]);

    useEffect(() => {
        // Fetch OCR history data from the backend API
        const fetchOcrHistory = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/ocr/all');
                setOcrHistory(response.data.data);
            } catch (error) {
                console.error('Error fetching OCR history:', error.message);
            }
        };

        fetchOcrHistory();
    }, []);

    return (
        <div>
            <h2>OCR History</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Timestamp</th>
                        <th>Status</th>
                        <th>Name</th>
                        <th>Last Name</th>
                        <th>Identification Number</th>
                        <th>Date of Issue</th>
                        <th>Date of Expiry</th>
                        <th>Date of Birth</th>
                        {/* Add more table headers as needed */}
                    </tr>
                </thead>
                <tbody>
                    {ocrHistory.map((record) => (
                        <tr key={record.id}>
                            <td>{record.id}</td>
                            <td>{new Date(record.timestamp).toLocaleString()}</td>
                            <td>{record.status}</td>
                            <td>{record.name}</td>
                            <td>{record.last_name}</td>
                            <td>{record.identification_number}</td>
                            <td>{record.date_of_issue}</td>
                            <td>{record.date_of_expiry}</td>
                            <td>{record.date_of_birth}</td>
                            {/* Add more table cells as needed */}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default OcrHistory;
