/* Inicializace filtru a razeni tabulky */
    $(document).ready(function() {
        $('.table').DataTable( {
            ordering: true,
            searching: true,
            paging: true,
            "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
            pageLength: -1,
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
            delete_click = false;
        });
    });