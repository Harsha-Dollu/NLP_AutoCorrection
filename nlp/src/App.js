import React, { useState, useEffect } from "react";

const App = () => {
  const [inputText, setInputText] = useState("");
  const [correctedText, setCorrectedText] = useState("");
  const [corrections, setCorrections] = useState([]);

  useEffect(() => {
    const debounceTimeout = setTimeout(() => {
      if (inputText.trim() !== "") {
        fetchCorrection();
      } else {
        setCorrectedText("");
        setCorrections([]);
      }
    }, 500); // Debounce API calls by 500ms

    return () => clearTimeout(debounceTimeout);
  }, [inputText]);

  const fetchCorrection = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/autocorrect", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setCorrectedText(data.corrected_text);
      setCorrections(data.corrections || []);
    } catch (error) {
      console.error("There was an error!", error);
      setCorrectedText("Error occurred while fetching corrections");
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Auto-Correct Application</h1>

      <textarea
        rows="4"
        placeholder="Enter text to autocorrect..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        style={styles.textArea}
      />

      <div style={styles.outputContainer}>
        <div style={styles.correctedTextContainer}>
          <h3 style={styles.subtitle}>Corrected Text:</h3>
          <p style={styles.outputText}>{correctedText}</p>
        </div>

        {corrections.length > 0 && (
          <div style={styles.correctionsContainer}>
            <h3 style={styles.subtitle}>Corrections Made:</h3>
            <ul style={styles.correctionsList}>
              {corrections.map((correction, index) => (
                <li key={index} style={styles.correctionItem}>
                  <span style={styles.originalWord}>{correction.original}</span>
                  {" → "}
                  <span style={styles.correctedWord}>
                    {correction.corrected}
                  </span>
                  <span style={styles.probability}>
                    ({(correction.probability * 100).toFixed(1)}%)
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    minHeight: "100vh",
    background: "linear-gradient(135deg, #f5f7fa, #c3cfe2)",
    padding: "20px",
  },
  title: {
    marginBottom: "20px",
    fontSize: "2rem",
    color: "#333",
    textAlign: "center",
    fontFamily: "'Roboto', sans-serif",
  },
  subtitle: {
    fontSize: "1.2rem",
    color: "#4a90e2",
    marginBottom: "10px",
    fontFamily: "'Roboto', sans-serif",
  },
  textArea: {
    padding: "15px",
    width: "80%",
    maxWidth: "600px",
    fontSize: "16px",
    borderRadius: "12px",
    border: "2px solid #4a90e2",
    background: "#ffffff",
    boxShadow:
      "4px 4px 8px rgba(0, 0, 0, 0.1), -4px -4px 8px rgba(255, 255, 255, 0.7)",
    marginBottom: "20px",
    resize: "none",
    transform: "perspective(500px) rotateX(3deg)",
  },
  outputContainer: {
    backgroundColor: "#fff",
    borderRadius: "12px",
    boxShadow:
      "4px 4px 12px rgba(0, 0, 0, 0.1), -4px -4px 12px rgba(255, 255, 255, 0.7)",
    padding: "20px",
    width: "80%",
    maxWidth: "600px",
  },
  correctedTextContainer: {
    marginBottom: "20px",
  },
  correctionsContainer: {
    borderTop: "1px solid #eee",
    paddingTop: "20px",
  },
  outputText: {
    fontSize: "16px",
    color: "#333",
    textAlign: "left",
    fontFamily: "'Roboto', sans-serif",
    lineHeight: "1.5",
    margin: "0",
  },
  correctionsList: {
    listStyle: "none",
    padding: "0",
    margin: "0",
  },
  correctionItem: {
    padding: "8px 0",
    borderBottom: "1px solid #f0f0f0",
    fontSize: "14px",
  },
  originalWord: {
    color: "#e74c3c",
    fontWeight: "bold",
  },
  correctedWord: {
    color: "#27ae60",
    fontWeight: "bold",
  },
  probability: {
    color: "#7f8c8d",
    fontSize: "12px",
    marginLeft: "8px",
  },
};

export default App;
