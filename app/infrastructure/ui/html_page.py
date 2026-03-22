def ui_html() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Local RAG</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Syne:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #05080f;
            --surface-0: #080d18;
            --surface-1: #0c1220;
            --surface-2: #111828;
            --surface-3: #16202f;
            --text: #e8edf8;
            --text-dim: #6b7fa3;
            --text-faint: #3a4a66;
            --accent: #4f8bff;
            --accent-glow: rgba(79,139,255,0.18);
            --accent-bright: #7aabff;
            --green: #3ecf7a;
            --green-glow: rgba(62,207,122,0.15);
            --red: #ff5f6b;
            --red-glow: rgba(255,95,107,0.15);
            --amber: #f5a623;
            --border: rgba(255,255,255,0.06);
            --border-hover: rgba(79,139,255,0.3);
            --radius: 16px;
            --mono: 'DM Mono', monospace;
            --display: 'Syne', sans-serif;
        }

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        html { scroll-behavior: smooth; }

        body {
            font-family: var(--display);
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* ── Background ── */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 80% 50% at 20% 10%, rgba(79,139,255,0.07) 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 80% 80%, rgba(62,207,122,0.05) 0%, transparent 55%),
                radial-gradient(ellipse 100% 80% at 50% 50%, rgba(5,8,15,0.9) 0%, transparent 100%);
            pointer-events: none;
            z-index: 0;
        }

        /* ── Noise texture ── */
        body::after {
            content: '';
            position: fixed;
            inset: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
            pointer-events: none;
            z-index: 0;
            opacity: 0.4;
        }

        .wrap {
            position: relative;
            z-index: 1;
            max-width: 1280px;
            margin: 0 auto;
            padding: 36px 28px 60px;
        }

        /* ── Header ── */
        .header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 36px;
            animation: fadeDown 0.6s ease both;
        }

        .header-title {
            font-size: 13px;
            font-weight: 500;
            font-family: var(--mono);
            color: var(--accent);
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 8px;
            opacity: 0.8;
        }

        h1 {
            font-size: clamp(24px, 3vw, 38px);
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.1;
            background: linear-gradient(135deg, #e8edf8 0%, #7aabff 60%, #3ecf7a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header-badge {
            display: flex;
            align-items: center;
            gap: 6px;
            font-family: var(--mono);
            font-size: 11px;
            color: var(--text-dim);
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 6px 14px;
            margin-top: 4px;
        }

        .dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 8px var(--green);
            animation: pulse-dot 2s ease-in-out infinite;
        }

        /* ── Grid ── */
        .grid {
            display: grid;
            grid-template-columns: 340px 1fr;
            gap: 18px;
            align-items: start;
        }

        .sidebar {
            display: grid;
            gap: 16px;
        }

        .main {
            display: grid;
            gap: 16px;
        }

        /* ── Cards ── */
        .card {
            background: linear-gradient(145deg, var(--surface-1) 0%, var(--surface-0) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 22px;
            position: relative;
            overflow: hidden;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
            animation: fadeUp 0.5s ease both;
        }

        .card::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: var(--radius);
            background: linear-gradient(135deg, rgba(79,139,255,0.04) 0%, transparent 50%);
            pointer-events: none;
        }

        .card:hover {
            border-color: rgba(79,139,255,0.15);
            box-shadow: 0 0 40px rgba(79,139,255,0.06);
        }

        .card:nth-child(1) { animation-delay: 0.1s; }
        .card:nth-child(2) { animation-delay: 0.2s; }
        .card:nth-child(3) { animation-delay: 0.3s; }

        /* ── Card headers ── */
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 18px;
        }

        h2 {
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-dim);
        }

        .card-icon {
            width: 28px;
            height: 28px;
            border-radius: 8px;
            background: var(--surface-3);
            border: 1px solid var(--border);
            display: grid;
            place-items: center;
            font-size: 13px;
        }

        /* ── Status ── */
        .status-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: var(--mono);
            font-size: 12px;
            padding: 8px 14px;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: var(--surface-2);
            transition: all 0.4s ease;
            color: var(--text-dim);
            width: 100%;
        }

        .status-chip.ok {
            border-color: rgba(62,207,122,0.25);
            background: rgba(62,207,122,0.06);
            color: var(--green);
        }

        .status-chip.bad {
            border-color: rgba(255,95,107,0.25);
            background: rgba(255,95,107,0.06);
            color: var(--red);
        }

        .status-chip .dot-ok { width:7px; height:7px; border-radius:50%; background:var(--green); box-shadow:0 0 8px var(--green); flex-shrink:0; animation: pulse-dot 2s ease-in-out infinite; }
        .status-chip .dot-bad { width:7px; height:7px; border-radius:50%; background:var(--red); box-shadow:0 0 8px var(--red); flex-shrink:0; }

        .status-meta {
            font-family: var(--mono);
            font-size: 11px;
            color: var(--text-faint);
            margin-top: 10px;
            line-height: 1.7;
        }

        .status-meta span { color: var(--text-dim); }

        /* ── Buttons ── */
        .btn-row {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 10px;
            margin-top: 14px;
        }

        button {
            font-family: var(--display);
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.03em;
            padding: 11px 18px;
            border-radius: 12px;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
            white-space: nowrap;
        }

        button::after {
            content: '';
            position: absolute;
            inset: 0;
            background: white;
            opacity: 0;
            transition: opacity 0.15s;
        }

        button:active::after { opacity: 0.07; }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent) 0%, #3a6fe0 100%);
            color: #fff;
            box-shadow: 0 4px 18px rgba(79,139,255,0.35);
        }

        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 24px rgba(79,139,255,0.45);
        }

        .btn-secondary {
            background: var(--surface-2);
            border: 1px solid var(--border);
            color: var(--text-dim);
        }

        .btn-secondary:hover {
            border-color: var(--border-hover);
            color: var(--text);
            background: var(--surface-3);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
        }

        .btn-icon {
            display: flex;
            align-items: center;
            gap: 7px;
        }

        /* ── Loading spinner ── */
        .spinner {
            width: 14px;
            height: 14px;
            border: 2px solid rgba(255,255,255,0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
            display: none;
        }

        button.loading .spinner { display: block; }
        button.loading .btn-label { opacity: 0.6; }

        /* ── Ingest output ── */
        .ingest-output {
            font-family: var(--mono);
            font-size: 11px;
            color: var(--text-dim);
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px 14px;
            line-height: 1.7;
            white-space: pre-wrap;
            max-height: 120px;
            overflow: auto;
            display: none;
            animation: fadeUp 0.3s ease;
        }

        .ingest-output.visible { display: block; }

        /* ── Doc list ── */
        .doc-list {
            border: 1px solid var(--border);
            border-radius: 12px;
            max-height: 380px;
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: var(--surface-3) transparent;
        }

        .doc-list::-webkit-scrollbar { width: 4px; }
        .doc-list::-webkit-scrollbar-thumb { background: var(--surface-3); border-radius: 4px; }

        .doc-empty {
            padding: 32px 20px;
            text-align: center;
            font-family: var(--mono);
            font-size: 12px;
            color: var(--text-faint);
        }

        .doc-row {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
            transition: background 0.2s ease;
            animation: fadeIn 0.3s ease both;
        }

        .doc-row:last-child { border-bottom: none; }
        .doc-row:hover { background: rgba(255,255,255,0.02); }

        .doc-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: var(--surface-3);
            border: 1px solid var(--border);
            display: grid;
            place-items: center;
            font-size: 13px;
            flex-shrink: 0;
        }

        .doc-info { flex: 1; min-width: 0; }
        .doc-name { font-size: 13px; font-weight: 600; truncate: ellipsis; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .doc-chunks { font-family: var(--mono); font-size: 11px; color: var(--text-faint); margin-top: 2px; }

        .chunk-badge {
            font-family: var(--mono);
            font-size: 10px;
            padding: 3px 8px;
            border-radius: 999px;
            background: var(--surface-3);
            border: 1px solid var(--border);
            color: var(--accent);
            flex-shrink: 0;
        }

        /* ── Inputs ── */
        .input-group {
            position: relative;
            display: flex;
            align-items: center;
        }

        .input-icon {
            position: absolute;
            left: 14px;
            color: var(--text-faint);
            font-size: 14px;
            pointer-events: none;
            z-index: 1;
        }

        input, textarea {
            width: 100%;
            font-family: var(--display);
            font-size: 13px;
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 12px;
            color: var(--text);
            padding: 12px 14px;
            outline: none;
            transition: all 0.25s ease;
        }

        input:focus, textarea:focus {
            border-color: rgba(79,139,255,0.4);
            background: var(--surface-3);
            box-shadow: 0 0 0 3px rgba(79,139,255,0.08);
        }

        input::placeholder, textarea::placeholder { color: var(--text-faint); }

        input[type="number"] {
            max-width: 80px;
            text-align: center;
            padding: 12px 8px;
        }

        textarea {
            min-height: 110px;
            resize: vertical;
            line-height: 1.6;
        }

        .search-row {
            display: grid;
            grid-template-columns: 1fr auto auto;
            gap: 10px;
            align-items: center;
        }

        .topk-label {
            font-family: var(--mono);
            font-size: 11px;
            color: var(--text-faint);
            white-space: nowrap;
        }

        /* ── Results ── */
        .results-container {
            display: grid;
            gap: 10px;
        }

        .result-card {
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px 16px;
            background: var(--surface-2);
            transition: all 0.25s ease;
            animation: fadeUp 0.3s ease both;
            position: relative;
            overflow: hidden;
        }

        .result-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, var(--accent), var(--green));
            border-radius: 3px 0 0 3px;
            opacity: 0.6;
        }

        .result-card:hover {
            border-color: rgba(79,139,255,0.2);
            background: var(--surface-3);
        }

        .result-source {
            font-family: var(--mono);
            font-size: 11px;
            color: var(--accent);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .result-text {
            font-size: 13px;
            line-height: 1.65;
            color: var(--text);
        }

        .result-score {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-family: var(--mono);
            font-size: 10px;
            color: var(--text-faint);
            margin-top: 10px;
            background: var(--surface-0);
            padding: 3px 8px;
            border-radius: 999px;
            border: 1px solid var(--border);
        }

        .no-results {
            text-align: center;
            padding: 24px;
            font-family: var(--mono);
            font-size: 12px;
            color: var(--text-faint);
            border: 1px dashed var(--border);
            border-radius: 12px;
        }

        /* ── Chat answer ── */
        .answer-box {
            position: relative;
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            min-height: 60px;
            font-size: 14px;
            line-height: 1.7;
            color: var(--text-dim);
            transition: all 0.3s ease;
        }

        .answer-box.has-answer {
            color: var(--text);
            border-color: rgba(79,139,255,0.15);
        }

        .answer-box.thinking {
            color: var(--accent);
        }

        .thinking-dots::after {
            content: '';
            animation: dots 1.4s infinite;
        }

        /* ── Divider ── */
        .divider {
            height: 1px;
            background: var(--border);
            margin: 16px 0;
        }

        .section-label {
            font-family: var(--mono);
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-faint);
            margin-bottom: 10px;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--surface-3); border-radius: 5px; }

        /* ── Animations ── */
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; box-shadow: 0 0 6px currentColor; }
            50% { opacity: 0.6; box-shadow: 0 0 14px currentColor; }
        }

        @keyframes dots {
            0% { content: '.'; }
            33% { content: '..'; }
            66% { content: '...'; }
        }

        @keyframes shimmer {
            0% { background-position: -200% center; }
            100% { background-position: 200% center; }
        }

        /* ── Result animation stagger ── */
        .result-card:nth-child(1) { animation-delay: 0.0s; }
        .result-card:nth-child(2) { animation-delay: 0.05s; }
        .result-card:nth-child(3) { animation-delay: 0.1s; }
        .result-card:nth-child(4) { animation-delay: 0.15s; }
        .result-card:nth-child(5) { animation-delay: 0.2s; }

        /* ── Responsive ── */
        @media (max-width: 900px) {
            .grid { grid-template-columns: 1fr; }
            .search-row { grid-template-columns: 1fr auto; }
        }
    </style>
</head>
<body>
    <div class="wrap">

        <!-- Header -->
        <div class="header">
            <div>
                <div class="header-title">// Local Intelligence Stack</div>
                <h1>Local Document Ai Bot</h1>
            </div>
            <div>
                <div class="header-badge">
                    <span class="dot"></span>
                    Jina + Chroma + Ollama
                </div>
            </div>
        </div>

        <div class="grid">

            <!-- Sidebar -->
            <div class="sidebar">

                <!-- Status card -->
                <div class="card">
                    <div class="card-header">
                        <h2>System Status</h2>
                        <div class="card-icon">⚡</div>
                    </div>
                    <div id="statusBox" class="status-chip">
                        <div class="dot-bad"></div>
                        Checking…
                    </div>
                    <div id="statusMeta" class="status-meta"></div>
                    <div class="btn-row">
                        <button class="btn-primary btn-icon" id="ingestBtn">
                            <div class="spinner"></div>
                            <span class="btn-label">▶ Run Ingestion</span>
                        </button>
                        <button class="btn-secondary" id="refreshDocsBtn" title="Refresh">↻</button>
                    </div>
                    <div id="ingestOutput" class="ingest-output"></div>
                </div>

                <!-- Documents card -->
                <div class="card">
                    <div class="card-header">
                        <h2>Indexed Documents</h2>
                        <div class="card-icon">📄</div>
                    </div>
                    <div id="docList" class="doc-list">
                        <div class="doc-empty">No documents yet</div>
                    </div>
                </div>

            </div>

            <!-- Main -->
            <div class="main">

                <!-- Search card -->
                <div class="card">
                    <div class="card-header">
                        <h2>Vector Search</h2>
                        <div class="card-icon">🔍</div>
                    </div>
                    <div class="search-row">
                        <input id="searchQuery" placeholder="Search your indexed data…" />
                        <div class="topk-label">Top K</div>
                        <input id="searchTopK" type="number" min="1" max="20" value="5" />
                    </div>
                    <div style="margin-top:12px">
                        <button class="btn-primary btn-icon" id="searchBtn" style="width:100%">
                            <div class="spinner"></div>
                            <span class="btn-label">Search</span>
                        </button>
                    </div>
                    <div id="searchResults" class="results-container" style="margin-top:16px"></div>
                </div>

                <!-- Chat card -->
                <div class="card">
                    <div class="card-header">
                        <h2>Chat with Documents</h2>
                        <div class="card-icon">💬</div>
                    </div>
                    <textarea id="chatQuestion" placeholder="Ask a question about your documents…"></textarea>
                    <div style="margin-top:12px">
                        <button class="btn-primary btn-icon" id="chatBtn" style="width:100%">
                            <div class="spinner"></div>
                            <span class="btn-label">Ask</span>
                        </button>
                    </div>

                    <div class="divider"></div>

                    <div class="section-label">Answer</div>
                    <div id="chatAnswer" class="answer-box">Ask a question to get started.</div>

                    <div id="chatSourcesWrap" style="display:none">
                        <div class="divider"></div>
                        <div class="section-label">Sources</div>
                        <div id="chatSources" class="results-container"></div>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script>
        /* ── API helpers ── */
        async function fetchStatus() {
            const r = await fetch('/api/status');
            return r.json();
        }
        async function fetchDocuments() {
            const r = await fetch('/api/documents');
            return r.json();
        }
        async function runIngestion() {
            const r = await fetch('/api/ingest', { method: 'POST' });
            return r.json();
        }
        async function runSearch(query, topK) {
            const r = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, top_k: topK })
            });
            return r.json();
        }
        async function runChat(question, topK) {
            const r = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, top_k: topK })
            });
            return r.json();
        }

        /* ── Button loading state ── */
        function setLoading(btn, loading) {
            btn.disabled = loading;
            btn.classList.toggle('loading', loading);
        }

        /* ── Renderers ── */
        function renderStatus(status) {
            const chip = document.getElementById('statusBox');
            const meta = document.getElementById('statusMeta');
            const ok = status.initialized === true;
            chip.className = 'status-chip ' + (ok ? 'ok' : 'bad');
            chip.innerHTML = ok
                ? '<div class="dot-ok"></div> System Initialized'
                : '<div class="dot-bad"></div> Not Initialized';
            meta.innerHTML = ok
                ? `Collection: <span>${status.collection_name || '—'}</span><br>Model: <span>${status.embedding_model || '—'}</span>`
                : '';
        }

        const DOC_ICONS = { pdf: '📕', txt: '📄', md: '📝', json: '🗃️', csv: '📊', py: '🐍', js: '⚡' };
        function docIcon(filename) {
            const ext = (filename || '').split('.').pop().toLowerCase();
            return DOC_ICONS[ext] || '📄';
        }

        function renderDocuments(data) {
            const list = document.getElementById('docList');
            if (!data.documents || data.documents.length === 0) {
                list.innerHTML = '<div class="doc-empty">No indexed documents yet</div>';
                return;
            }
            list.innerHTML = data.documents.map((doc, i) => `
                <div class="doc-row" style="animation-delay:${i * 0.05}s">
                    <div class="doc-icon">${docIcon(doc.source)}</div>
                    <div class="doc-info">
                        <div class="doc-name" title="${doc.source}">${doc.source}</div>
                        <div class="doc-chunks">${doc.chunks} chunk${doc.chunks !== 1 ? 's' : ''}</div>
                    </div>
                    <div class="chunk-badge">${doc.chunks}</div>
                </div>
            `).join('');
        }

        function resultCardHTML(item) {
            const src = item.metadata?.source || 'unknown source';
            const score = typeof item.score === 'number' ? item.score.toFixed(4) : item.score;
            return `
                <div class="result-card">
                    <div class="result-source">${docIcon(src)} ${src}</div>
                    <div class="result-text">${item.document || ''}</div>
                    <div class="result-score">⬡ score: ${score}</div>
                </div>`;
        }

        function renderSearchResults(data) {
            const container = document.getElementById('searchResults');
            if (!data.results || data.results.length === 0) {
                container.innerHTML = '<div class="no-results">No results found.</div>';
                return;
            }
            container.innerHTML = data.results.map(resultCardHTML).join('');
        }

        function renderChat(data) {
            const answerEl = document.getElementById('chatAnswer');
            const sourcesEl = document.getElementById('chatSources');
            const sourcesWrap = document.getElementById('chatSourcesWrap');

            answerEl.className = 'answer-box has-answer';
            answerEl.textContent = data.answer || 'No answer returned.';

            if (data.sources && data.sources.length > 0) {
                sourcesEl.innerHTML = data.sources.map(resultCardHTML).join('');
                sourcesWrap.style.display = 'block';
            } else {
                sourcesWrap.style.display = 'none';
            }
        }

        async function refreshAll() {
            try {
                const [status, docs] = await Promise.all([fetchStatus(), fetchDocuments()]);
                renderStatus(status);
                renderDocuments(docs);
            } catch (e) {
                console.error('Refresh failed', e);
            }
        }

        /* ── Event listeners ── */
        document.getElementById('refreshDocsBtn').addEventListener('click', refreshAll);

        document.getElementById('ingestBtn').addEventListener('click', async () => {
            const btn = document.getElementById('ingestBtn');
            const output = document.getElementById('ingestOutput');
            setLoading(btn, true);
            output.textContent = 'Running ingestion pipeline…';
            output.classList.add('visible');
            try {
                const result = await runIngestion();
                output.textContent = JSON.stringify(result, null, 2);
                await refreshAll();
            } catch (e) {
                output.textContent = e.message || 'Ingestion failed.';
            } finally {
                setLoading(btn, false);
            }
        });

        document.getElementById('searchBtn').addEventListener('click', async () => {
            const query = document.getElementById('searchQuery').value.trim();
            const topK = parseInt(document.getElementById('searchTopK').value || '5', 10);
            const btn = document.getElementById('searchBtn');
            if (!query) { renderSearchResults({ results: [] }); return; }
            setLoading(btn, true);
            try {
                const result = await runSearch(query, topK);
                renderSearchResults(result);
            } finally {
                setLoading(btn, false);
            }
        });

        document.getElementById('searchQuery').addEventListener('keydown', e => {
            if (e.key === 'Enter') document.getElementById('searchBtn').click();
        });

        document.getElementById('chatBtn').addEventListener('click', async () => {
            const question = document.getElementById('chatQuestion').value.trim();
            const topK = parseInt(document.getElementById('searchTopK').value || '5', 10);
            const btn = document.getElementById('chatBtn');
            const answerEl = document.getElementById('chatAnswer');
            const sourcesWrap = document.getElementById('chatSourcesWrap');
            if (!question) { answerEl.textContent = 'Enter a question first.'; return; }
            setLoading(btn, true);
            answerEl.className = 'answer-box thinking';
            answerEl.innerHTML = '<span class="thinking-dots">Thinking</span>';
            sourcesWrap.style.display = 'none';
            try {
                const result = await runChat(question, topK);
                renderChat(result);
            } finally {
                setLoading(btn, false);
            }
        });

        document.getElementById('chatQuestion').addEventListener('keydown', e => {
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) document.getElementById('chatBtn').click();
        });

        /* ── Init ── */
        refreshAll();
    </script>
</body>
</html>
"""