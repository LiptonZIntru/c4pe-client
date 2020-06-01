function deleteThis(place_id, id) {
    if (confirm('Do you really want to delete this opening times?') == true) {
        window.location = '/admin/places/' + place_id + '/openingtimes/' + id + '/delete/';
    }
}

function showEdit(id) {
    var elements = document.getElementsByTagName("form");
    for(var i = 0; i < elements.length; i++) {
        if (elements[i].id.includes('editForm_')) {
            elements[i].hidden = true;
        }
    }
    document.getElementById('editForm_' + id).hidden = false;
}

function updateTimes(char, timesID) {
    if(timesID) timesID = char + timesID;

    var openHours = document.getElementById('open' + timesID).value.slice(0, 2);
    var openMinutes = document.getElementById('open' + timesID).value.slice(3, 5);
    var openDot = document.getElementById('open' + timesID).value[2];
    var closeHours = document.getElementById('close' + timesID).value.slice(0, 2);
    var closeMinutes = document.getElementById('close' + timesID).value.slice(3, 5);
    var closeDot = document.getElementById('close' + timesID).value[2];

    if (openDot == ':' && closeDot == ':' && document.getElementById('open' + timesID).value.length == 5 && document.getElementById('close' + timesID).value.length == 5) {
        document.getElementById('openHour' + timesID).value = openHours;
        document.getElementById('openMinutes' + timesID).value = openMinutes;
        document.getElementById('closeHour' + timesID).value = closeHours;
        document.getElementById('closeMinutes' + timesID).value = closeMinutes;

        if(timesID) {
            document.getElementById('editForm' + timesID).submit();
        }
        else {
            document.getElementById('createForm').submit();
        }
    }
    else {
        window.alert("Invalid input! Please enter opening times in format HH:MM.");
    }
}