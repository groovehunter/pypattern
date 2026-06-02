async function fetchStatus() {
    try {
        const res = await fetch('/api/status');
        const data = await res.json();
        document.getElementById('currentPatt').innerText = data.current_pattern;

        const layoutSel = document.getElementById('layoutSelect');
        if (layoutSel.options[0].innerText === "Lade...") {
            layoutSel.innerHTML = "";
            data.layouts.forEach(l => {
                const opt = document.createElement('option');
                opt.value = l;
                opt.innerText = l;
                if (l === data.current_layout) opt.selected = true;
                layoutSel.appendChild(opt);
            });
        }

        const list = document.getElementById('patternList');
        if (list.childElementCount === 0) {
            data.patterns.forEach(p => {
                const btn = document.createElement('button');
                btn.innerText = p;
                btn.onclick = () => setPattern(p);
                list.appendChild(btn);
            });
        }

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

async function setPattern(name) {
    try {
        await fetch('/api/pattern?name=' + encodeURIComponent(name));
        fetchStatus();
    } catch(e) {
        console.error(e);
    }
}

async function setPlaylist(name) {
    try {
        await fetch('/api/playlist?name=' + encodeURIComponent(name));
        fetchStatus();
    } catch(e) {
        console.error(e);
    }
}

async function setLayout(name) {
    try {
        await fetch('/api/layout?name=' + encodeURIComponent(name));
        fetchStatus();
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
        await fetch('/api/speed?val=' + encodeURIComponent(val));
    } catch(e) {
        console.error(e);
    }
}

// Init
fetchStatus();
setInterval(fetchStatus, 3000); // 3 Sek Auto-Refresh
