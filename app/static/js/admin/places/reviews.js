function deleteThis(place_id, review_id) {
    if (confirm('Do you really want to delete this review?') == true) {
        window.location = '/admin/places/' + place_id + '/reviews/' + review_id + '/delete';
    }
}