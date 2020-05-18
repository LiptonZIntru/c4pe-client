var delete_click = false;
$(function () {
    $('.delete').click(function () {
        delete_click = true;
        var response = confirm('Do you really want to delete this place?');
        if(response == true)
        {
            var id = $(this).parent().parent().attr('id');
            window.location = '/admin/places/' + place.id + '/owners/' + id + '/delete';
        }
    });
});