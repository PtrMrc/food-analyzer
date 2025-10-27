import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Válasszon ki egy pdf fájlt!");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:8000/analyze-pdf/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Server error: " + response.statusText);
      }

      const data = await response.json();
      setResult(data.analysis || data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Élelmiszer elemzése</h1>
      <p>Töltsön fel egy PDF fájlt és elemezze az allergéneket és tápértékeket!</p>

      <input type="file" accept=".pdf" onChange={handleFileChange} />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Elemzés..." : "Feltöltés & Elemzés"}
      </button>

      {error && <p className="error">❌ {error}</p>}

      {result && (
        <div className="result">
          <h2>📊 Elemzés eredménye</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
