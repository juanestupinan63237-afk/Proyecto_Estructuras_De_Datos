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

    if(response.ok){
        document.getElementById("vueloForm").reset();
        RefreshTree();
    }
}

async function RefreshTree() {
    const res = await fetch("/Render/AVL");
    const svg = await res.text();
    document.getElementById("treeContainer").innerHTML = svg;
}

async function OpenBSTWindow() {
    const popup = window.open("", "BST Tree", "width=800,height=600");
    const res = await fetch("/Render/BST");
    const svg = await res.text();

    popup.document.write(`
        <html>
        <head>
            <title>BST Tree</title>
        </head>
        <body style="background:#0f172a;display:flex;justify-content:center;align-items:center;">
            ${svg}
        </body>
        </html>
    `);
}

async function PrintPreOrderTour() {
    const res = await fetch("/Print", {method:"POST"});
    const data = await res.json();
    alert("PreOrder: " + data.preorder.join(" -> "));
}