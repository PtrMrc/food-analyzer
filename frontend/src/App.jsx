import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showInfo, setShowInfo] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    validateAndSetFile(selectedFile);
  };

  const validateAndSetFile = (selectedFile) => {
    if (!selectedFile) return;

    if (!selectedFile.name.toLowerCase().endsWith('.pdf')) {
      setError("Csak PDF fájlokat fogadunk el!");
      setFile(null);
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      setError("A fájl túl nagy! Maximum 10MB engedélyezett.");
      setFile(null);
      return;
    }

    if (selectedFile.size === 0) {
      setError("A fájl üres!");
      setFile(null);
      return;
    }

    setError(null);
    setFile(selectedFile);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Válasszon ki egy PDF fájlt!");
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

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Szerver hiba történt");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Ismeretlen hiba történt");
    } finally {
      setLoading(false);
    }
  };

  const downloadJSON = () => {
    const dataStr = JSON.stringify(result, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "elemzes_eredmeny.json";
    link.click();
    URL.revokeObjectURL(url);
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / 1048576).toFixed(1) + " MB";
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Élelmiszer-elemző🍽️</h1>
        <button className="info-btn" onClick={() => setShowInfo(!showInfo)}>
          ℹ️
        </button>
      </div>

      {showInfo && (
        <div className="info-panel">
          <h3>📋 Miről szól ez az oldal?</h3>
          <p>
            Ez az alkalmazás automatikusan elemzi az élelmiszer PDF fájlokat,
            és kinyeri belőlük az allergéneket és tápértékadatokat.
          </p>
          <h3>🔧 Hogyan működik?</h3>
          <ol>
            <li>Tölts fel egy PDF fájlt (max. 10MB)</li>
            <li>Az AI elemzi a dokumentumot</li>
            <li>Az eredmény azonnal megjelenik</li>
            <li>Exportálhatod JSON formátumban</li>
          </ol>
          <h3>⚠️ Támogatott fájlok</h3>
          <p>Csak PDF formátumú fájlok, maximum 10MB méretben.</p>
        </div>
      )}

      <p>Töltsön fel egy PDF fájlt egy élelmiszerről az allergének és tápértékek elemzéséhez!</p>

      <div
        className={`upload-area ${dragActive ? "drag-active" : ""}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          id="file-input"
        />
        <label htmlFor="file-input" className="file-label">
          📄 {file ? file.name : "Válassz PDF fájlt vagy húzd ide"}
        </label>
        {file && (
          <p className="file-info">
            Méret: {formatFileSize(file.size)}
          </p>
        )}
      </div>

      <button onClick={handleUpload} disabled={loading || !file}>
        {loading ? "⏳ Elemzés folyamatban..." : "🚀 Elemzés indítása"}
      </button>

      {loading && (
        <div className="progress">
          <div className="spinner"></div>
          <p>Az AI dolgozik az elemzésen...</p>
        </div>
      )}

      {error && <div className="error">❌ {error}</div>}

      {result && (
        <div className="result">
          <div className="result-header">
            <h2>📊 Elemzés eredménye</h2>
            <button onClick={downloadJSON} className="download-btn">
              💾 Letöltés JSON-ként
            </button>
          </div>

          {result.Allergének && (
            <div className="section">
              <h3>⚠️ Allergének:</h3>
              {result.Allergének.length > 0 ? (
                <div className="allergen-list">
                  {result.Allergének.map((allergen, idx) => (
                    <span key={idx} className="allergen-badge">
                      {allergen}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="no-data">Nincs allergén a termékben ✅</p>
              )}
            </div>
          )}

          {result.Tápanyagok && (
            <div className="section">
              <h3>📈 Tápértékek:</h3>
              <table className="nutrition-table">
                <tbody>
                  {Object.entries(result.Tápanyagok).map(([key, value]) => {
                    let unit = "";
                    if (key === "Energia") unit = " kcal";
                    else if (key === "Nátrium") unit = " mg";
                    else unit = " g";

                    return (
                      <tr key={key}>
                        <td className="label">{key}</td>
                        <td className="value">
                          {value !== null ? `${value}${unit}` : "N/A"}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;