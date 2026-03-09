async function GetVuelo() {
    const data = {
        code: document.getElementById("Code").value,
        origin: document.getElementById("Origin").value,
        destination: document.getElementById("destination").value,
        departureTime: document.getElementById("departureTime").value,
        basePrice: document.getElementById("basePrice").value,
        numberPassengers: document.getElementById("numberPassengers").value
    };

    const response = await fetch("/Sent/Node", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if(response.ok) {
        document.getElementById("vueloForm").reset();
        RefreshTree();
    }
}

async function RefreshTree() {
    const res = await fetch('/Render/Tree');
    const svg = await res.text();
    document.getElementById('treeContainer').innerHTML = svg;
}

async function PrintPreOrderTour() {
    const res = await fetch("/Print", { method: "POST" });
    const data = await res.json();
    alert("PreOrder: " + data.preorder.join(" -> "));
}

async function ControlZ (){
    const res = await fetch ("/Control/Pila");
    console.log ("Control-z");
}

async function LoadJSON (){
    const filesLoad = document.getElementById("file-upload");
    const file = filesLoad.files[0];
    const form = new FormData ();
    form.append ("archivo" , file);

    const envio = await fetch ("/ImportarJSON", {
        method : "POST",
        body : form
    });
}

async function ModoEstresActivar () {
    let request = await fetch ("/ModoEstres/Activar");
}

async function ModoEstresDesactivar (){
    let request = await fetch ("/ModoEstres/Desactivar");
}