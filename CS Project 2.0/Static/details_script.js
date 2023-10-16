document.addEventListener("DOMContentLoaded", function () {
    tableData=JSON.parse(JSON.stringify(custData))
    console.log(tableData)
    TableEntry("current")

    const selectButtons = document.querySelectorAll(".booking_btn");
    let selectedRoom = null;

    selectButtons.forEach(function (button) {
        button.addEventListener("click", handleSelectButtonClick);
    });
    
    pay_btn = document.getElementById('payDisplay_btn')
    pay_btn.addEventListener('click',function (){
        console.log("sdafasdfs")
        selected_cust = document.getElementsByClassName("selected-button")
        const cust_id = selected_cust[0].getAttribute('id-select');
        if (selected_cust){
            console.log(payData)
            pay_Data=payData[cust_id]
            console.log(pay_Data)
            document.getElementById('roomCharges').innerHTML ='₹' + pay_Data['roomCharges']
            document.getElementById('roomService').innerHTML ='₹' + pay_Data['roomService']
            document.getElementById('service').innerHTML ='₹' + pay_Data['service']
            document.getElementById('vat').innerHTML ='₹' + pay_Data['vat']
            document.getElementById('gym').innerHTML ='₹' + pay_Data['gym']
            document.getElementById('bar').innerHTML ='₹' + pay_Data['bar']
            document.getElementById('bed').innerHTML = '₹' +pay_Data['bed']
            document.getElementById('breakfast').innerHTML = '₹' + pay_Data['breakfast']
            document.getElementById('total').innerHTML = '₹' + pay_Data['total']
        }
    })

    const paid_btn=document.getElementById('paid')
    paid_btn.addEventListener('click', function(){

        selected_cust = document.getElementsByClassName("selected-button")
        const cust_id = selected_cust[0].getAttribute('id-select');
        const idJSON = {'id':cust_id};
        console.log(idJSON);

        // Display the JSON data (you can replace this with your preferred method)
        const requestOptions = {
            method: "POST",
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(idJSON)
        };
        
        const serverURL = "http://127.0.0.1:5000/customer_info";
        
        fetch(serverURL, requestOptions)
        .then(response => {
            if (response.status !== 200) {
            throw new Error(`Login failed. Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message)
        })
        .catch(error => {
            console.error('Error:', error.message);
        });
    })
});



function showTable(tableId) {
    // Hide all tablesa
    document.getElementById('currentTable').classList.add('hidden-table');
    document.getElementById('pastTable').classList.add('hidden-table');
    document.getElementById('advanceTable').classList.add('hidden-table');

    // Show the selected table
    document.getElementById(tableId + 'Table').classList.remove('hidden-table'); // or 'block' if you prefer
    TableEntry(tableId)
    if (tableId='currnt'){
        attachButtonListeners()
    }
}

function TableEntry(TableId) {
    var tableBody = document.querySelector("#"+TableId+"Table table tbody");
    tableBody.innerHTML = "";

    if (TableId=="current"){
        (tableData[0]).forEach(function (booking) {
            var row = document.createElement("tr");
            row.innerHTML = `
            <td><button class="booking_btn" \id-select=${booking.id}></button></td>
            <td>${booking.id}</td>
            <td>${booking.name}</td>
            <td>${booking.phone_no}</td>
            <td>${booking.email_id}</td>
            <td>${booking.guests}</td>
            <td>${booking.room_no}</td>
            <td>${booking.room_type}</td>
            <td>${Boolean(booking.addons[0])}</td>
            <td>${Boolean(booking.addons[1])}</td>
            <td>${Boolean(booking.addons[2])}</td>
            <td>${Boolean(booking.addons[3])}</td>
            <td>${booking.check_in}</td>
            <td>${booking.check_out}</td>`;
            tableBody.appendChild(row);
            }
    )}
    else if (TableId=="advance"){
        (tableData[1]).forEach(function (booking) {
           
            var row = document.createElement("tr");
            row.innerHTML = `
            <td>${booking.id}</td>
            <td>${booking.name}</td>
            <td>${booking.phone_no}</td>
            <td>${booking.email_id}</td>
            <td>${booking.guests}</td>
            <td>${booking.room_no}</td>
            <td>${booking.room_type}</td>
            <td>${Boolean(booking.addons[0])}</td>
            <td>${Boolean(booking.addons[1])}</td>
            <td>${Boolean(booking.addons[2])}</td>
            <td>${Boolean(booking.addons[3])}</td>
            <td>${booking.check_in}</td>`;
            tableBody.appendChild(row);
            }
    )}
    else if (TableId=="past"){
        (tableData[2]).forEach(function (booking) {
          
            var row = document.createElement("tr");
            row.innerHTML = `
            <td>${booking.id}</td>
            <td>${booking.name}</td>
            <td>${booking.phone_no}</td>
            <td>${booking.email_id}</td>
            <td>${booking.guests}</td>
            <td>${booking.room_no}</td>
            <td>${booking.room_type}</td>
            <td>${Boolean(booking.addons[0])}</td>
            <td>${Boolean(booking.addons[1])}</td>
            <td>${Boolean(booking.addons[2])}</td>
            <td>${Boolean(booking.addons[3])}</td>
            <td>${booking.check_in}</td>
            <td>${booking.check_out}</td>
            <td>${booking.amount}</td>`;
            tableBody.appendChild(row);
            }
    )}
    
    
}

function handleSelectButtonClick() {
    const roomType = this.getAttribute("room-select");

    // Check if the button is already selected
    const isAlreadySelected = this.classList.contains("selected-button");

    // Deselect the button if it's already selected
    if (isAlreadySelected) {
        this.classList.remove("selected-button");
        selectedRoom = null;
    } else {
        // Deselect any previously selected button
        const previouslySelectedButton = document.querySelector(".booking_btn.selected-button");
        if (previouslySelectedButton) {
            previouslySelectedButton.classList.remove("selected-button");
        }

        // Select the clicked button
        this.classList.add("selected-button");
        selectedRoom = roomType;
    }
}
function attachButtonListeners() {
    const selectButtons = document.querySelectorAll(".booking_btn");
    let selectedRoom = null;

    selectButtons.forEach(function (button) {
        button.addEventListener("click", handleSelectButtonClick);
    });
}


