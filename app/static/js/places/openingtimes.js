function deleteThis(place_id, id) {
    if (confirm('Do you really want to delete this opening times?') == true) {
        window.location = '/places/' + place_id + '/openingtimes/' + id + '/delete/';
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

function updateTimes(timesID) {
    var openHours = parseInt(document.getElementById('open_' + timesID).value.slice(0, 2));
    var openMinutes = parseInt(document.getElementById('open_' + timesID).value.slice(3, 5));
    var openDot = document.getElementById('open_' + timesID).value[2];
    var closeHours = parseInt(document.getElementById('close_' + timesID).value.slice(0, 2));
    var closeMinutes = parseInt(document.getElementById('close_' + timesID).value.slice(3, 5));
    var closeDot = document.getElementById('close_' + timesID).value[2];
    window.alert(openHours + openDot + openMinutes + "   " + closeHours + closeDot + closeMinutes);
    if(openDot == ':' && closeDot == ':'){
        document.getElementById('openHour_' + timesID).value = openHours;
        document.getElementById('openMinutes_' + timesID).value = openMinutes;
        document.getElementById('closeHour_' + timesID).value = closeHours;
        document.getElementById('closeMinutes_' + timesID).value = closeMinutes;

        document.getElementById('editForm_' + timesID).submit();
    }
    else {
        window.alert("Invalid input! Please enter opening times in format HH:MM.");
    }
}