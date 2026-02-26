async function GetVuelo() {
    let code = document.getElementById("Code").value;
    let origin = document.getElementById("Origin").value;
    let destination = document.getElementById("destination").value;
    let departureTime = document.getElementById("departureTime").value;
    let basePrice = document.getElementById("basePrice").value;
    let numberPassengers = document.getElementById("numberPassengers").value
    let respuesta = await fetch ("/Sent/Node" , {
        method : "POST" , 
        headers : {
            "Content-Type" : "application/json"
        },
        body : JSON.stringify ({
            "code" : code,
            "origin" : origin,
            "destination" : destination,
            "departureTime" : departureTime,
            "basePrice" : basePrice,
            "numberPassengers" : numberPassengers
        })
    });
    if (respuesta.ok){
        console.log ("Nodo Insertado con exito");
        RefreshTree();
    }
}

async function PrintPreOrderTour() {
    let respuesta = await fetch ("/Print" , {
        method : "POST",
        headers : {
            "Content-Type" : "application/json"
        },
        body : JSON.stringify ({
            "Hecho" : true
        })
    });
}

async function RefreshTree(){
    let respuesta = await fetch('/Render/Tree',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    });
        if (respuesta.ok){
            let svg = await respuesta.text();
            document.getElementById('treeContainer').innerHTML = svg;
        }
    }

window.addEventListener('load', function(){
    RefreshTree();
});