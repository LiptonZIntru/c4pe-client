var delete_click = false;
$(function () {
    $('.delete').click(function () {
        delete_click = true;
        var response = confirm('Do you really want to delete this place type?');
        if(response == true)
        {
            var id = $(this).parent().parent().attr('id');
            window.location = '/admin/placetypes/' + id + '/delete';
        }
    });
    $('.edit').click(function () {
        if(!delete_click)
        {
            var id = $(this).attr('id');
            window.location = '/admin/placetypes/' + id + '/edit/';
        }
    });
});