function deleteThis(place_id, string) {
    if (string == 'place') {
        if(confirm('Do you really want to delete this place?')) {
            window.location = '/admin/places/' + place_id + '/delete/';
        }
    }
    else {
        if(confirm('Do you really want to delete this image?')) {
            window.location = '/admin/places/' + place_id + '/images/' + string + '/delete/';
        }
    }
}