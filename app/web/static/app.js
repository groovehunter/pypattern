async function apiGet(url) {
    return fetch(url, { cache: 'no-store' });
}

async function fetchStatus() {
    try {
        const res = await apiGet('/api/status');
        const data = await res.json();
        document.getElementById('currentPatt').innerText = data.current_pattern;
        const runIcon = document.getElementById('runIcon');
        runIcon.innerText = data.is_running ? '✓' : 'x';
        runIcon.className = data.is_running ? 'status-icon running' : 'status-icon stopped';

        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        startBtn.disabled = !!data.is_running;
        stopBtn.disabled = !data.is_running;

        const currentPatternName = getPatternName(data.current_pattern);

        const layoutSel = document.getElementById('layoutSelect');
        const needsLayoutRefresh =
            layoutSel.options.length !== data.layouts.length ||
            layoutSel.options[0].innerText === "Lade...";

        if (needsLayoutRefresh) {
            layoutSel.innerHTML = "";
            data.layouts.forEach(l => {
                const opt = document.createElement('option');
                opt.value = l;
                opt.innerText = l;
                layoutSel.appendChild(opt);
            });
        }
        layoutSel.value = data.current_layout;

        const list = document.getElementById('patternList');
        if (list.childElementCount === 0) {
            data.patterns.forEach(p => {
                const btn = document.createElement('button');
                btn.className = 'pattern-btn';
                btn.dataset.pattern = p;
                btn.innerText = p;
                btn.onclick = () => setPattern(p);
                list.appendChild(btn);
            });
        }
        highlightActivePattern(currentPatternName);

        const plist = document.getElementById('playlistList');
        if (plist.childElementCount === 0) {
            data.playlists.forEach(pl => {
                const btn = document.createElement('button');
                btn.innerText = pl;
                btn.onclick = () => setPlaylist(pl);
                plist.appendChild(btn);
            });
        }
    } catch(e) {
        console.error("Status fetch failed", e);
    }
}

function getPatternName(stateText) {
    if (!stateText) return '';
    if (stateText.indexOf('|') === -1) return stateText.trim();
    const parts = stateText.split('|');
    return parts[parts.length - 1].trim();
}

function highlightActivePattern(patternName) {
    const buttons = document.querySelectorAll('#patternList .pattern-btn');
    buttons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.pattern === patternName);
    });
}

async function setPattern(name) {
    try {
        await apiGet('/api/pattern?name=' + encodeURIComponent(name));
        fetchStatus();
    } catch(e) {
        console.error(e);
    }
}

async function setPlaylist(name) {
    try {
        await apiGet('/api/playlist?name=' + encodeURIComponent(name));
        fetchStatus();
    } catch(e) {
        console.error(e);
    }
}

async function setLayout(name) {
    try {
        await apiGet('/api/layout?name=' + encodeURIComponent(name));
        await fetchStatus();
    } catch(e) {
        console.error(e);
    }
}

function updateSpeedLabel(val) {
    let interval = 11 - parseInt(val);
    let bpm = Math.round(600 / interval);
    document.getElementById('bpmLabel').innerText = bpm + " BPM";
}

async function setSpeedUI(val) {
    let interval = 11 - parseInt(val);
    setSpeed(interval);
}

async function setSpeed(val) {
    try {
        await apiGet('/api/speed?val=' + encodeURIComponent(val));
    } catch(e) {
        console.error(e);
    }
}

async function startPlayback() {
    try {
        await apiGet('/api/start');
        await fetchStatus();
    } catch(e) {
        console.error(e);
    }
}

async function stopPlayback() {
    try {
        await apiGet('/api/stop');
        await fetchStatus();
    } catch(e) {
        console.error(e);
    }
}

// Init
fetchStatus();
setInterval(fetchStatus, 3000); // 3 Sek Auto-Refresh
