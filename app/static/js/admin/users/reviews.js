function deleteThis(place_id, review_id) {
    if (confirm('Do you really want to delete this review?') == true) {
        window.location = '/admin/users/' + place_id + '/reviews/' + review_id + '/delete';
    }
}