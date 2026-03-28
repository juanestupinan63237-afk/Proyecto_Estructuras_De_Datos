async function GetVuelo() {
    const data = {
        code:             document.getElementById("Code").value,
        origin:           document.getElementById("Origin").value,
        destination:      document.getElementById("destination").value,
        departureTime:    document.getElementById("departureTime").value,
        basePrice:        document.getElementById("basePrice").value,
        numberPassengers: document.getElementById("numberPassengers").value
    };
 
    const response = await fetch("/Sent/Node", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
 
    if (response.ok) {
        document.getElementById("vueloForm").reset();
        await RefreshTree();
        await RefreshQueue();
        await RefreshMetrics();
    }
}
 
async function RefreshTree() {
    const res = await fetch("/Render/Tree");
    const svg = await res.text();
    document.getElementById("treeContainer").innerHTML = svg;
}
 
async function LoadJSON() {
    const filesLoad = document.getElementById("file-upload");
    const file = filesLoad.files[0];
    if (!file) return;
 
    const form = new FormData();
    form.append("archivo", file);
 
    const envio = await fetch("/ImportarJSON", {
        method: "POST",
        body: form
    });
 
    if (envio.ok) {
        await RefreshTree();
        await RefreshMetrics();
    }
}
 
async function obtenerDatos() {
    const respuesta = await fetch("/Descargar/Tree/Topology");
    const data = await respuesta.json();
    console.log(data);
}

async function RefreshQueue() {
    try {
        const res  = await fetch("/Cola/Ver");
        const data = await res.json();
        _renderQueue(data.size, data.vuelos);
    } catch (e) {
        console.error("Error fetching queue:", e);
    }
}
 
async function DesencolarVuelo() {
    try {
        const res  = await fetch("/Cola/DesencolarVuelo", { method: "POST" });
        const data = await res.json();
 
        if (data.status === "empty") {
            _showToast("La cola ya está vacía");
            return;
        }
 
        _showToast(`✔ Vuelo ${data.vuelos !== undefined ? "" : ""}${data.message}`);
        _renderQueue(data.size, data.vuelos);
        await RefreshTree();
        await RefreshMetrics();
 
    } catch (e) {
        console.error("Error al desencolar:", e);
    }
}
 
function _renderQueue(size, vuelos) {
    document.getElementById("queue-size").textContent = size;
 
    const emptyEl   = document.getElementById("queue-empty");
    const listEl    = document.getElementById("queue-list");
    const actionsEl = document.getElementById("queue-actions");
 
    if (!vuelos || vuelos.length === 0) {
        emptyEl.classList.remove("hidden");
        listEl.innerHTML = "";
        actionsEl.style.display = "none";
        return;
    }
 
    emptyEl.classList.add("hidden");
    actionsEl.style.display = "flex";
 
    listEl.innerHTML = vuelos.map((v, i) => `
        <div class="queue-card ${i === 0 ? 'next-flight' : ''}">
            <div class="queue-pos">${v.position}</div>
            <div class="queue-card-body">
                <div class="queue-card-top">
                    <span class="queue-code">#${v.code}</span>
                    ${i === 0 ? '<span class="next-label">Next</span>' : ''}
                    <span class="queue-route">${v.origin} → ${v.destination}</span>
                </div>
                <div class="queue-card-bottom">
                    <span class="queue-detail">🕐 <span>${v.departureTime}</span></span>
                    <span class="queue-detail">💰 <span>$${Number(v.basePrice).toLocaleString()}</span></span>
                    <span class="queue-detail">👥 <span>${v.numberPassengers}</span></span>
                </div>
            </div>
        </div>
    `).join("");
}
 
async function ProcessAll() {
    let remaining = parseInt(document.getElementById("queue-size").textContent) || 0;
    while (remaining > 0) {
        const res  = await fetch("/Cola/DesencolarVuelo", { method: "POST" });
        const data = await res.json();
        if (data.status === "empty") break;
        remaining = data.size;
        _renderQueue(data.size, data.vuelos);
    }
    await RefreshTree();
    await RefreshMetrics();
    _showToast("✔ All flights inserted into the tree");
}
 
function _showToast(msg) {
    const toast = document.getElementById("queue-toast");
    toast.textContent = msg;
    toast.style.opacity = "1";
    setTimeout(() => { toast.style.opacity = "0"; }, 3000);
}
 
 
let _traversals = {};
let _activeTab  = "preorder";
 
async function RefreshMetrics() {
    try {
        const res = await fetch("/Metricas/Analiticas");
        if (!res.ok) return;
        const data = await res.json();
 
        document.getElementById("m-height").textContent    = data.height;
        document.getElementById("m-leaves").textContent    = data.leaves;
        document.getElementById("m-rot-total").textContent = data.rotations.total;
        document.getElementById("m-mass").textContent      = data.massCancellations;
        document.getElementById("m-sl").textContent        = data.rotations.simpleLeft;
        document.getElementById("m-sr").textContent        = data.rotations.simpleRight;
        document.getElementById("m-dl").textContent        = data.rotations.doubleLeft;
        document.getElementById("m-dr").textContent        = data.rotations.doubleRight;
 
        _traversals = data.traversals;
        _renderTraversal(_activeTab);
 
    } catch (e) {
        console.error("Error fetching metrics:", e);
    }
}
 
function ShowTab(key, btn) {
    _activeTab = key;
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    if (btn) btn.classList.add("active");
    _renderTraversal(key);
}
 
function _renderTraversal(key) {
    const output = document.getElementById("traversal-output");
    const codes  = _traversals[key];
 
    if (!codes || codes.length === 0) {
        output.innerHTML = '<span class="traversal-placeholder">No data — click Refresh first</span>';
        return;
    }
 
    output.innerHTML = codes
        .map(c => `<span class="code-badge">${c}</span>`)
        .join("");
}