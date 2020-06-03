/* Inicializace filtru a razeni tabulky */
    $(document).ready(function() {
        $('.table').DataTable( {
            ordering: true,
            searching: true,
            paging: true,
            pageLength: 25,
            "columns": [ null,
                         null,
                         { "orderable": false } ]
        } );
    } );


/* table controls */
    var delete_click = false;
    $(function () {
        $('.delete').click(function () {
            delete_click = true;
            var response = confirm('Do you really want to delete this place?');
            if(response == true)
            {
                var id = $(this).parent().parent().attr('id');
                window.location = '/admin/places/' + id + '/delete';
            }
        });
        $('.edit').click(function () {
            if(!delete_click)
            {
                var id = $(this).attr('id');
                window.location = '/admin/places/' + id + '/edit/';
            }
            delete_click = false;
        });
    });