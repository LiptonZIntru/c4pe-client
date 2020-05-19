var delete_click = false;
$(function () {
    $('.delete').click(function () {
        delete_click = true;
        var response = confirm('Do you really want to delete this user?');
        if(response == true)
        {
            var id = $(this).parent().parent().attr('id');
            window.location = '/admin/users/' + id + '/delete';
        }
    });
    $('.edit').click(function () {
        if(!delete_click)
        {
            var id = $(this).attr('id');
            window.location = '/admin/users/' + id + '/edit/';
        }
    });
});