function deleteThis(id, target) {
    if(target != 'avatar') {
        if (confirm('Do you really want to delete this user?') == true) {
            window.location = '/admin/users/' + id + '/delete';
        }
    }
    else {
        if (confirm('Do you really want to delete this users avatar?') == true) {
            window.location = '/admin/users/' + id + '/avatar/delete';
        }
    }
}