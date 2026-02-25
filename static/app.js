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
    }
}