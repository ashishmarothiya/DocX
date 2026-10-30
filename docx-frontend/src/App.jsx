import React, { useCallback, useEffect, useRef, useState } from "react";

import {
  Activity, ArrowUp, CheckCircle2, ChevronDown, CircleHelp, CloudUpload,
  FileImage, FileText, FolderOpen, History, Info, Loader2, Menu, MessageSquare,
  MoreHorizontal, Paperclip, Search, Send, Settings, ShieldCheck, Sparkles,
  X, Zap
} from "lucide-react";

const API = "/api";

function formatBytes(bytes) {
  if (!bytes) return "";
  const units = ["B", "KB", "MB", "GB"];
  let n = bytes, i = 0;
  while (n >= 1024 && i < units.length - 1) {
    n /= 1024;
    i++;
  }
  return `${n.toFixed(i ? 1 : 0)} ${units[i]}`;
}

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [files, setFiles] = useState([]);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [answer, setAnswer] = useState("");
  const [searching, setSearching] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [dragging, setDragging] = useState(false);
  const [status, setStatus] = useState({ type: "idle", text: "Ready" });
  const [activeTab, setActiveTab] = useState("workspace");
  const inputRef = useRef(null);

  const runSearch = useCallback(async (q = query) => {
    const clean = q.trim();
    if (!clean) return;

    setSearching(true);
    setAnswer("");
    setResults([]);
    setStatus({ type: "busy", text: "Reading your documents and generating an answer…" });

    try {
      const res = await fetch(`${API}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: clean,
          limit: 8,
          min_score: null,
          source: null
        })
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || data.message || `Request failed (${res.status})`);
      }

      setAnswer(data.answer || "");
      setResults(data.sources || []);

      setStatus({
        type: "success",
        text: `${(data.sources || []).length} supporting evidence matches found`
      });
    } catch (err) {
      setAnswer("");
      setResults([]);
      setStatus({
        type: "error",
        text: err.message || "Unable to generate an answer"
      });
    } finally {
      setSearching(false);
    }
  }, [query]);

  const uploadFiles = useCallback(async (incoming) => {
    const valid = [...incoming].filter(f => {
      const ext = (f.name || "").toLowerCase().split(".").pop();
      return (
        ["application/pdf", "application/x-pdf", "image/jpeg", "image/png"].includes(f.type) ||
        ["pdf", "png", "jpg", "jpeg"].includes(ext)
      );
    });

    if (!valid.length) {
      setStatus({
        type: "error",
        text: "Only PDF, JPG and PNG files are supported."
      });
      return;
    }

    setUploading(true);

    for (const file of valid) {
      const local = {
        id: crypto.randomUUID(),
        name: file.name,
        size: file.size,
        state: "processing"
      };

      setFiles(prev => [local, ...prev]);

      try {
        const form = new FormData();
        form.append("file", file);

        const res = await fetch(`${API}/upload`, {
          method: "POST",
          body: form
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          if (res.status === 413) {
            throw new Error("File is too large. Maximum supported upload size is 100MB.");
          }
          throw new Error(
            data.detail ||
            data.message ||
            `Upload failed (${res.status})`
          );
        }

        setFiles(prev =>
          prev.map(x =>
            x.id === local.id
              ? {
                  ...x,
                  state: "ready",
                  pipeline: data.pipeline,
                  original: data.original_filename
                }
              : x
          )
        );

        setStatus({
          type: "success",
          text: `${file.name} processed successfully`
        });
      } catch (err) {
        setFiles(prev =>
          prev.map(x =>
            x.id === local.id
              ? {
                  ...x,
                  state: "error",
                  error: err.message
                }
              : x
          )
        );

        setStatus({
          type: "error",
          text: err.message
        });
      }
    }

    setUploading(false);
  }, []);

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    uploadFiles(e.dataTransfer.files);
  };

  useEffect(() => {
    const onKey = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };

    window.addEventListener("keydown", onKey);

    return () => {
      window.removeEventListener("keydown", onKey);
    };
  }, []);

  const readyCount = files.filter(f => f.state === "ready").length;

  return (
    <div className="app-shell">

      <aside className={`sidebar ${sidebarOpen ? "open" : "closed"}`}>

        <div className="brand">
          <div className="logo">
            <Sparkles size={18} strokeWidth={2.6} />
          </div>

          {sidebarOpen && (
            <div>
              <div className="brand-name">DocX</div>
              <div className="brand-sub">Document Intelligence</div>
            </div>
          )}
        </div>

        <button
          className="new-btn"
          onClick={() => inputRef.current?.click()}
        >
          <CloudUpload size={18} />
          <span>{sidebarOpen ? "Upload document" : ""}</span>
        </button>

        <nav className="nav">

          <button
            className={`nav-item ${activeTab === "workspace" ? "active" : ""}`}
            onClick={() => setActiveTab("workspace")}
          >
            <MessageSquare size={18} />
            <span>Workspace</span>
          </button>

          <button
            className={`nav-item ${activeTab === "library" ? "active" : ""}`}
            onClick={() => setActiveTab("library")}
          >
            <FolderOpen size={18} />
            <span>Document library</span>
            {readyCount > 0 && <b>{readyCount}</b>}
          </button>

          <button
            className={`nav-item ${activeTab === "history" ? "active" : ""}`}
            onClick={() => setActiveTab("history")}
          >
            <History size={18} />
            <span>Search history</span>
          </button>

        </nav>

        {sidebarOpen && (
          <div className="sidebar-bottom">

            <div className="secure-card">
              <div className="secure-icon">
                <ShieldCheck size={16} />
              </div>

              <div>
                <strong>Private workspace</strong>
                <p>Your documents stay in your local API workflow.</p>
              </div>
            </div>

            <button className="nav-item">
              <Settings size={18} />
              <span>Settings</span>
            </button>

            <button className="nav-item">
              <CircleHelp size={18} />
              <span>Help & docs</span>
            </button>

          </div>
        )}

      </aside>

      <main className="main">

        <header className="topbar">

          <button
            className="icon-btn"
            onClick={() => setSidebarOpen(v => !v)}
          >
            <Menu size={20} />
          </button>

          <div className="crumb">
            <span>DocX</span>
            <span className="slash">/</span>
            <strong>Workspace</strong>
          </div>

          <div className="top-actions">

            <div className="api-status">
              <span
                className={`dot ${status.type === "error" ? "bad" : ""}`}
              />
              API {status.type === "error" ? "error" : "connected"}
            </div>

            <button className="avatar">AM</button>

          </div>

        </header>

        <section className="content">

          <div className="hero">

            <div>

              <div className="eyebrow">
                <Zap size={13} />
                AI DOCUMENT WORKSPACE
              </div>

              <h1>
                Turn documents into <span>answers.</span>
              </h1>

              <p>
                Upload PDFs or scans, ask questions across your documents,
                and inspect the evidence behind every answer.
              </p>

            </div>

            <div className="hero-metric">
              <div className="metric-number">{readyCount}</div>
              <div className="metric-label">indexed docs</div>
            </div>

          </div>

          <div
            className={`dropzone ${dragging ? "dragging" : ""}`}
            onDragOver={(e) => {
              e.preventDefault();
              setDragging(true);
            }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
            onClick={() => inputRef.current?.click()}
          >

            <input
              ref={inputRef}
              type="file"
              hidden
              multiple
              accept=".pdf,.png,.jpg,.jpeg"
              onChange={(e) => {
                uploadFiles(e.target.files);
                e.target.value = "";
              }}
            />

            <div className="upload-icon">
              <CloudUpload size={26} />
            </div>

            <div className="drop-copy">
              <strong>
                {uploading
                  ? "Processing document…"
                  : "Drop your documents here"}
              </strong>

              <span>
                or click to browse • PDF, PNG, JPG
              </span>
            </div>

            <div className="drop-kbd">⌘ K</div>

          </div>

          {files.length > 0 && (
            <section className="section">

              <div className="section-head">

                <div>
                  <h2>Documents</h2>
                  <p>
                    Files sent to the FastAPI processing pipeline.
                  </p>
                </div>

                <span className="pill">
                  {files.length} total
                </span>

              </div>

              <div className="file-grid">

                {files.map(file => (

                  <div className="file-card" key={file.id}>

                    <div
                      className={`file-type ${
                        file.name.toLowerCase().endsWith(".pdf")
                          ? "pdf"
                          : "img"
                      }`}
                    >
                      {file.name.toLowerCase().endsWith(".pdf")
                        ? <FileText size={20} />
                        : <FileImage size={20} />}
                    </div>

                    <div className="file-info">
                      <strong title={file.name}>
                        {file.name}
                      </strong>

                      <span>
                        {formatBytes(file.size)}
                      </span>
                    </div>

                    <div className={`file-state ${file.state}`}>

                      {file.state === "processing" && (
                        <>
                          <Loader2 size={14} className="spin" />
                          Processing
                        </>
                      )}

                      {file.state === "ready" && (
                        <>
                          <CheckCircle2 size={14} />
                          Ready
                        </>
                      )}

                      {file.state === "error" && (
                        <>
                          <Info size={14} />
                          Failed
                        </>
                      )}

                    </div>

                    {file.error && (
                      <div className="file-error">
                        {file.error}
                      </div>
                    )}

                  </div>

                ))}

              </div>

            </section>
          )}

          <section className="search-panel">

            <div className="section-head">

              <div>
                <h2>Ask your documents</h2>
                <p>
                  AI-powered answers grounded in your indexed document evidence.
                </p>
              </div>

              <div className="search-hint">
                <Search size={14} />
                ⌘K
              </div>

            </div>

            <div className="search-box">

              <Search size={20} />

              <input
                ref={inputRef}
                value={query}
                onChange={e => setQuery(e.target.value)}
                onKeyDown={e => {
                  if (e.key === "Enter") runSearch();
                }}
                placeholder="Ask a question about your documents…"
              />

              {query && (
                <button
                  className="clear"
                  onClick={() => {
                    setQuery("");
                    setAnswer("");
                    setResults([]);
                  }}
                >
                  <X size={16} />
                </button>
              )}

              <button
                className="send"
                disabled={!query.trim() || searching}
                onClick={() => runSearch()}
              >
                {searching
                  ? <Loader2 size={17} className="spin" />
                  : <ArrowUp size={17} />}
              </button>

            </div>

            {searching && (
              <div className="ai-loading">
                <Sparkles size={17} className="spin" />
                <span>
                  DocX is reading the relevant evidence and generating your answer…
                </span>
              </div>
            )}

            {answer && (
              <div className="answer-card">

                <div className="answer-header">

                  <div className="answer-title">
                    <div className="answer-icon">
                      <Sparkles size={17} />
                    </div>

                    <div>
                      <strong>AI Answer</strong>
                      <span>Generated from your indexed documents</span>
                    </div>
                  </div>

                  <div className="answer-badge">
                    <CheckCircle2 size={14} />
                    Grounded
                  </div>

                </div>

                <div className="answer-body">
                  {answer.split("\n").map((line, index) => (
                    <p key={index}>
                      {line || "\u00A0"}
                    </p>
                  ))}
                </div>

              </div>
            )}

            {results.length > 0 && (

              <div className="results">

                <div className="result-title">
                  <span>Supporting evidence</span>
                  <span>{results.length} sources</span>
                </div>

                {results.map((r, i) => (

                  <article
                    className="result"
                    key={`${r.chunk_index}-${i}`}
                  >

                    <div className="result-meta">

                      <span className="source-tag">
                        <FileText size={13} />
                        {r.source || "Document"}
                      </span>

                      {r.page != null && (
                        <span>Page {r.page}</span>
                      )}

                      <span>
                        Score {(Number(r.score) * 100).toFixed(1)}%
                      </span>

                    </div>

                    <p>{r.text}</p>

                    {r.chunk_index != null && (
                      <div className="chunk">
                        Chunk {r.chunk_index}
                      </div>
                    )}

                  </article>

                ))}

              </div>

            )}

          </section>

          <div className={`status ${status.type}`}>

            <Activity size={15} />

            <span>{status.text}</span>

            <button
              onClick={() =>
                setStatus({
                  type: "idle",
                  text: "Ready"
                })
              }
            >
              <X size={14} />
            </button>

          </div>

        </section>

        <footer className="footer">
          <span>DocX</span>
          <span>•</span>
          <span>FastAPI + Qdrant + Gemini</span>
          <span>•</span>
          <span>Local development</span>
        </footer>

      </main>

    </div>
  );
}

export default App;
