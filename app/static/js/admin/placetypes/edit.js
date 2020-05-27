function deleteThis(id) {
    if(confirm('Do you really want to delete this place type?') == true)
    {
        window.location = '/admin/placetypes/' + id + '/delete';
    }
}