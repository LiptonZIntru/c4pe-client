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