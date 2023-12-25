import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import OcrResults from './components/OcrResults';
import OcrHistory from './components/OcrHistory';

function App() {
    const [updateResults, setUpdateResults] = useState(0);

    const handleUploadSuccess = () => {
        // Increment the state to trigger a re-fetch of OCR results
        setUpdateResults(updateResults + 1);
    };

    return (
        <div>
            <h1>Thai ID OCR App</h1>
            <UploadForm onUploadSuccess={handleUploadSuccess} />
            <OcrResults key={updateResults} />
            <OcrHistory />
        </div>
    );
}

export default App;
