let pinState = null;
let activeLayout = null;

async function apiGet(url) {
    const res = await fetch(url, { cache: 'no-store' });
    let payload = {};
    try {
        payload = await res.json();
    } catch (e) {
        // ignore invalid json bodies
    }
    if (!res.ok) {
        throw new Error(payload.error || ('HTTP ' + res.status));
    }
    return payload;
}

function setMessage(msg, isError) {
    const el = document.getElementById('pinMsg');
    el.innerText = msg || '';
    el.className = isError ? 'pin-msg error' : 'pin-msg ok';
}

function isProtectedLayout(name) {
    if (!pinState || !pinState.protected_layouts) return false;
    return pinState.protected_layouts.indexOf(name) !== -1;
}

function buildLegend() {
    if (!pinState || !pinState.pin_meta) return;
    const meta = pinState.pin_meta;
    const legend = document.getElementById('pinLegend');
    legend.innerHTML = '';

    const allowed = document.createElement('span');
    allowed.className = 'legend-chip';
    allowed.innerText = 'Erlaubt: ' + meta.allowed_pins.join(', ');

    const restricted = document.createElement('span');
    restricted.className = 'legend-chip warn';
    restricted.innerText = 'Vorsicht: ' + meta.restricted_pins.join(', ');

    const inputOnly = document.createElement('span');
    inputOnly.className = 'legend-chip err';
    inputOnly.innerText = 'Input-only: ' + meta.input_only_pins.join(', ');

    legend.appendChild(allowed);
    legend.appendChild(restricted);
    legend.appendChild(inputOnly);
}

function buildTabs() {
    const tabs = document.getElementById('layoutTabs');
    tabs.innerHTML = '';
    const names = Object.keys(pinState.layouts || {});

    names.forEach(name => {
        const btn = document.createElement('button');
        btn.className = 'tab-btn' + (name === activeLayout ? ' active' : '');
        btn.innerText = name;
        btn.onclick = () => {
            activeLayout = name;
            renderEditor();
        };
        tabs.appendChild(btn);
    });
}

function buildPinSelect(selectedPin, disabled, onChange) {
    const meta = pinState.pin_meta || { allowed_pins: [] };
    const sel = document.createElement('select');
    sel.className = 'pin-select';
    sel.disabled = !!disabled;

    meta.allowed_pins.forEach(pin => {
        const opt = document.createElement('option');
        opt.value = String(pin);
        opt.innerText = 'GPIO ' + pin;
        if (Number(pin) === Number(selectedPin)) {
            opt.selected = true;
        }
        sel.appendChild(opt);
    });

    sel.onchange = onChange;
    return sel;
}

function renderEditor() {
    if (!pinState || !activeLayout) return;

    buildTabs();
    buildLegend();

    const editor = document.getElementById('layoutEditor');
    editor.innerHTML = '';

    const layout = pinState.layouts[activeLayout];
    if (!layout) {
        setMessage('Layout nicht gefunden.', true);
        return;
    }

    const panels = layout.panels || [];
    const locked = isProtectedLayout(activeLayout);

    if (locked) {
        setMessage('Dieses Layout ist geschützt (read-only). Bitte zuerst klonen.', false);
    }

    panels.forEach((panelPins, panelIdx) => {
        const card = document.createElement('div');
        card.className = 'panel-card';

        const title = document.createElement('h4');
        title.innerText = 'Panel ' + (panelIdx + 1);
        card.appendChild(title);

        const row = document.createElement('div');
        row.className = 'slot-row';

        panelPins.forEach((pin, slotIdx) => {
            const wrap = document.createElement('label');
            wrap.className = 'slot-item';
            wrap.innerText = 'Slot ' + (slotIdx + 1);

            const sel = buildPinSelect(pin, locked, async (ev) => {
                const newPin = ev.target.value;
                try {
                    const url = '/api/pins/set?layout=' + encodeURIComponent(activeLayout) +
                        '&panel=' + encodeURIComponent(panelIdx + 1) +
                        '&slot=' + encodeURIComponent(slotIdx + 1) +
                        '&pin=' + encodeURIComponent(newPin);
                    const res = await apiGet(url);
                    setMessage(res.message || 'Pin gespeichert.', false);
                    await reloadPinStatus(activeLayout);
                } catch (err) {
                    setMessage('Setzen fehlgeschlagen: ' + err.message, true);
                    await reloadPinStatus(activeLayout);
                }
            });

            wrap.appendChild(sel);
            row.appendChild(wrap);
        });

        card.appendChild(row);
        editor.appendChild(card);
    });
}

async function reloadPinStatus(preferredLayout) {
    try {
        pinState = await apiGet('/api/pins/status');
        if (!activeLayout || !pinState.layouts[activeLayout]) {
            activeLayout = preferredLayout || pinState.current_layout || Object.keys(pinState.layouts)[0];
        }
        renderEditor();
    } catch (err) {
        setMessage('Status konnte nicht geladen werden: ' + err.message, true);
    }
}

async function saveLayout() {
    if (!activeLayout) return;
    try {
        const res = await apiGet('/api/pins/save?layout=' + encodeURIComponent(activeLayout));
        setMessage(res.message || 'Gespeichert.', false);
    } catch (err) {
        setMessage('Speichern fehlgeschlagen: ' + err.message, true);
    }
}

async function cloneCurrentLayout() {
    if (!activeLayout) return;
    const cloneName = document.getElementById('cloneName').value.trim();
    if (!cloneName) {
        setMessage('Bitte einen Zielnamen eingeben.', true);
        return;
    }
    try {
        const url = '/api/pins/clone?src=' + encodeURIComponent(activeLayout) + '&dst=' + encodeURIComponent(cloneName);
        const res = await apiGet(url);
        setMessage(res.message || 'Layout geklont.', false);
        document.getElementById('cloneName').value = '';
        await reloadPinStatus(cloneName);
    } catch (err) {
        setMessage('Klonen fehlgeschlagen: ' + err.message, true);
    }
}

reloadPinStatus();

