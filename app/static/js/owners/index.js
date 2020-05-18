$(function () {
    $('.delete').click(function (e) {
        var response = confirm('Do you really want to remove this owner?');
        if(!response)
        {
            e.preventDefault();
        }
    });
});