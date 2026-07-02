/**
 * script.js
 * Dashboard controller: polls /status and /logs every 2 s,
 * handles Start Update button, and manages the log-file modal.
 */

/* ── Helpers ─────────────────────────────────────── */

function fmtPct(val) {
    return parseFloat(val || 0).toFixed(1) + '%';
}

function badgeHTML(status) {
    var label = status.charAt(0).toUpperCase() + status.slice(1);
    return '<span class="status-badge ' + status + '">'
         + '<span class="dot"></span>' + label + '</span>';
}

function lineClass(line) {
    var lo = line.toLowerCase();
    if (lo.indexOf('error') >= 0 || lo.indexOf('fail') >= 0 || lo.indexOf('fatal') >= 0) return 'error';
    if (lo.indexOf('warn') >= 0) return 'warning';
    if (lo.indexOf('===') >= 0 || lo.indexOf('started') >= 0) return 'header';
    if (lo.indexOf('completed') >= 0 || lo.indexOf('success') >= 0 || lo.indexOf('updated') >= 0) return 'done';
    return 'info';
}

/* ── DOM refs ─────────────────────────────────────── */

var btnStart      = document.getElementById('btn-start-update');
var btnStop       = document.getElementById('btn-stop-update');
var progressFill  = document.getElementById('progress-fill');
var progressLabel = document.getElementById('progress-label');
var logConsole    = document.getElementById('log-console');
var alertBox      = document.getElementById('alert-box');
var statusBadgeEl = document.getElementById('status-badge');
var clearBtn      = document.getElementById('btn-clear-console');

var elTotal       = document.getElementById('stat-total');
var elProcessed   = document.getElementById('stat-processed');
var elSuccess     = document.getElementById('stat-success');
var elFailed      = document.getElementById('stat-failed');
var elRemaining   = document.getElementById('stat-remaining');
var elSuccessPct  = document.getElementById('stat-success-pct');
var elFailedPct   = document.getElementById('stat-failed-pct');
var elCurrent     = document.getElementById('stat-current');
var elStatus      = document.getElementById('stat-status');

/* ── Alert ─────────────────────────────────────────── */

function showAlert(msg, type) {
    if (!alertBox) return;
    alertBox.className = 'alert-box show ' + type;
    alertBox.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> ' + msg;
    setTimeout(function () { alertBox.classList.remove('show'); }, 6000);
}

/* ── Dashboard update ───────────────────────────────── */

var lastLogCount = 0;

function setText(el, val) { if (el) el.textContent = val; }

function applyStatus(data) {
    var pct = parseFloat(data.progress || 0);

    if (progressFill) {
        progressFill.style.width = pct + '%';
        progressFill.setAttribute('aria-valuenow', pct);
    }
    setText(progressLabel, pct.toFixed(1) + '%');

    if (statusBadgeEl) statusBadgeEl.innerHTML = badgeHTML(data.status || 'idle');
    if (elStatus)      elStatus.innerHTML      = badgeHTML(data.status || 'idle');

    setText(elTotal,      data.total      || 0);
    setText(elProcessed,  data.processed  || 0);
    setText(elSuccess,    data.success    || 0);
    setText(elFailed,     data.failed     || 0);
    setText(elRemaining,  data.remaining  || 0);
    setText(elSuccessPct, fmtPct(data.success_pct));
    setText(elFailedPct,  fmtPct(data.failed_pct));

    if (elCurrent) {
        elCurrent.textContent = data.current_username
            ? '@' + data.current_username
            : (data.running ? 'Initialising...' : '—');
    }

    if (btnStart) {
        if (data.running) {
            btnStart.disabled = true;
            btnStart.classList.add('loading');
        } else {
            btnStart.disabled = false;
            btnStart.classList.remove('loading');
        }
    }
    if (btnStop) {
        if (data.running) {
            if (data.status === 'stopping') {
                btnStop.disabled = true;
            } else {
                btnStop.disabled = false;
            }
        } else {
            btnStop.disabled = true;
        }
    }
}

/* ── Fetch /status ──────────────────────────────────── */

function fetchStatus() {
    fetch('/status')
        .then(function (r) { return r.json(); })
        .then(function (data) {
            applyStatus(data);
        })
        .catch(function (e) { console.warn('Status error:', e); });
}

/* ── Fetch /logs ────────────────────────────────────── */

function fetchLogs() {
    fetch('/logs')
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (!logConsole) return;
            var lines = data.logs || [];
            if (lines.length > lastLogCount) {
                var newLines = lines.slice(lastLogCount);
                for (var i = 0; i < newLines.length; i++) {
                    var div = document.createElement('div');
                    div.className = 'log-line ' + lineClass(newLines[i]);
                    div.textContent = newLines[i];
                    logConsole.appendChild(div);
                }
                lastLogCount = lines.length;
                logConsole.scrollTop = logConsole.scrollHeight;
            }
        })
        .catch(function (e) { console.warn('Logs error:', e); });
}

/* ── Polling ─────────────────────────────────────────── */

var pollTimer = null;

function startPolling() {
    if (pollTimer) return;
    pollTimer = setInterval(function () {
        fetchStatus();
        fetchLogs();
    }, 2000);
}

function stopPolling() {
    if (pollTimer) { clearInterval(pollTimer); pollTimer = null; }
}

/* ── Stop Update button ──────────────────────────────── */
if (btnStop) {
    btnStop.addEventListener('click', function () {
        btnStop.disabled = true;
        fetch('/stop-update', { method: 'POST' })
            .then(function (r) { return r.json(); })
            .then(function (res) {
                if (res.success) {
                    showAlert(res.message, 'info');
                } else {
                    showAlert('Error: ' + res.message, 'danger');
                }
            })
            .catch(function (e) {
                showAlert('Network error: ' + e.message, 'danger');
            });
    });
}

/* ── Start Update button ─────────────────────────────── */

if (btnStart) {
    btnStart.addEventListener('click', function () {
        btnStart.disabled = true;
        btnStart.classList.add('loading');
        if (logConsole) { logConsole.innerHTML = ''; }
        lastLogCount = 0;

        fetch('/start-update', { method: 'POST' })
            .then(function (r) {
                return r.json().then(function (body) {
                    return { status: r.status, body: body };
                });
            })
            .then(function (res) {
                if (res.status === 200 && res.body.success) {
                    showAlert(res.body.message, 'success');
                    startPolling();
                } else if (res.status === 409) {
                    showAlert(res.body.message, 'info');
                    btnStart.disabled = false;
                    btnStart.classList.remove('loading');
                    startPolling();
                } else {
                    showAlert('Error: ' + (res.body.message || 'Unknown error'), 'danger');
                    btnStart.disabled = false;
                    btnStart.classList.remove('loading');
                }
            })
            .catch(function (e) {
                showAlert('Network error: ' + e.message, 'danger');
                btnStart.disabled = false;
                btnStart.classList.remove('loading');
            });
    });
}

/* ── Clear console button ─────────────────────────────── */

if (clearBtn) {
    clearBtn.addEventListener('click', function () {
        if (logConsole) logConsole.innerHTML = '';
        lastLogCount = 0;
    });
}

/* ── On page load ─────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', function () {
    fetchStatus();
    fetchLogs();
    fetch('/status')
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.running) startPolling();
        })
        .catch(function () {});
});

/* ── Log modal (History page) ─────────────────────────── */

var logModal       = document.getElementById('log-modal');
var logModalTitle  = document.getElementById('log-modal-title');
var logModalBody   = document.getElementById('log-modal-content');
var logModalClose  = document.getElementById('log-modal-close');

function openLogModal(filename) {
    if (!logModal) return;
    logModalTitle.textContent = filename;
    logModalBody.textContent  = 'Loading...';
    logModal.classList.add('show');

    fetch('/logs/view/' + encodeURIComponent(filename))
        .then(function (r) { return r.json(); })
        .then(function (data) {
            logModalBody.textContent = data.error ? ('Error: ' + data.error) : data.content;
        })
        .catch(function (e) {
            logModalBody.textContent = 'Load failed: ' + e.message;
        });
}

if (logModalClose) {
    logModalClose.addEventListener('click', function () {
        logModal.classList.remove('show');
    });
}

if (logModal) {
    logModal.addEventListener('click', function (e) {
        if (e.target === logModal) logModal.classList.remove('show');
    });
}
