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
                         null,
                         null,
                         { "orderable": false } ]
        } );
    } );


/* table controls */
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
        $('.reviews').click(function () {
            delete_click = true;
            var id = $(this).parent().parent().attr('id');
            window.location = '/admin/users/' + id + '/reviews';
        });
        $('.edit').click(function () {
            if(!delete_click)
            {
                var id = $(this).attr('id');
                window.location = '/admin/users/' + id + '/edit';
            }
            delete_click = false;
        })
    });