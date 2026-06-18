import { useState } from "react"
import { generateTweet, getHistory } from "./api"

function App() {
  const [topic, setTopic] = useState("")
  const [maxIter, setMaxIter] = useState(3)
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [view, setView] = useState("generate") // "generate" or "history"

  async function handleGenerate() {
    if (!topic.trim()) return
    setLoading(true)
    setError(null)
    try {
      const data = await generateTweet(topic, maxIter)
      setResult(data)
    } catch (err) {
      setError("Something went wrong. Is the server running?")
    } finally {
      setLoading(false)
    }
  }

  async function handleHistory() {
    setView("history")
    try {
      const data = await getHistory(10)
      setHistory(data)
    } catch (err) {
      setError("Could not fetch history.")
    }
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🐦 Tweet Generator</h1>

      {/* Nav */}
      <div style={styles.nav}>
        <button style={view === "generate" ? styles.activeTab : styles.tab}
          onClick={() => setView("generate")}>Generate</button>
        <button style={view === "history" ? styles.activeTab : styles.tab}
          onClick={handleHistory}>History</button>
      </div>

      {/* Generate View */}
      {view === "generate" && (
        <div style={styles.card}>
          <input
            style={styles.input}
            placeholder="Enter topic... (e.g. Monday mornings)"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
          <div style={styles.row}>
            <label style={styles.label}>Max iterations: {maxIter}</label>
            <input type="range" min="1" max="5" value={maxIter}
              onChange={(e) => setMaxIter(Number(e.target.value))} />
          </div>
          <button style={styles.btn} onClick={handleGenerate} disabled={loading}>
            {loading ? "Generating..." : "Generate Tweet"}
          </button>

          {error && <p style={styles.error}>{error}</p>}

          {result && (
            <div style={styles.result}>
              <p style={styles.tweet}>"{result.final_tweet}"</p>
              <p style={styles.meta}>Status: {result.status} | Iterations: {result.iterations_used}</p>
              <details>
                <summary style={styles.label}>Tweet history ({result.tweet_history.length} versions)</summary>
                {result.tweet_history.map((t, i) => (
                  <p key={i} style={styles.historyItem}>[{i + 1}] {t}</p>
                ))}
              </details>
            </div>
          )}
        </div>
      )}

      {/* History View */}
      {view === "history" && (
        <div>
          {history.length === 0 && <p style={styles.label}>No tweets yet.</p>}
          {history.map((item) => (
            <div key={item.id} style={styles.card}>
              <p style={styles.tweet}>"{item.final_tweet}"</p>
              <p style={styles.meta}>Topic: {item.topic} | {item.status} | {new Date(item.created_at).toLocaleString()}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

const styles = {
  container: { maxWidth: 640, margin: "0 auto", padding: "32px 16px", fontFamily: "sans-serif" },
  title: { fontSize: 28, marginBottom: 20, textAlign: "center" },
  nav: { display: "flex", gap: 8, marginBottom: 20 },
  tab: { padding: "8px 20px", borderRadius: 8, border: "1px solid #444", background: "transparent", color: "#aaa", cursor: "pointer" },
  activeTab: { padding: "8px 20px", borderRadius: 8, border: "1px solid #7c6aff", background: "#7c6aff22", color: "#7c6aff", cursor: "pointer" },
  card: { background: "#1a1a2e", border: "1px solid #333", borderRadius: 12, padding: 20, marginBottom: 16 },
  input: { width: "100%", padding: "10px 14px", borderRadius: 8, border: "1px solid #444", background: "#0f0f1a", color: "#fff", fontSize: 15, marginBottom: 12 },
  row: { display: "flex", alignItems: "center", gap: 12, marginBottom: 12 },
  label: { color: "#888", fontSize: 13 },
  btn: { width: "100%", padding: "12px", borderRadius: 8, border: "none", background: "#7c6aff", color: "#fff", fontSize: 15, cursor: "pointer" },
  result: { marginTop: 20, borderTop: "1px solid #333", paddingTop: 16 },
  tweet: { fontSize: 17, lineHeight: 1.6, color: "#fff", marginBottom: 8 },
  meta: { fontSize: 12, color: "#666", marginBottom: 12 },
  historyItem: { fontSize: 13, color: "#aaa", marginTop: 8, paddingLeft: 8, borderLeft: "2px solid #444" },
  error: { color: "#ff6b6b", fontSize: 13, marginTop: 8 },
}

export default App