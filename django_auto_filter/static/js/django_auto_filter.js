$(document).ready( function () {
//    $('table').bootstrapTable();
    $('table').DataTable( {
//        dom: 'Bfrtip',
        dom: 'BHt',
        buttons: [ 'colvis' ],
        scrollX: true
    } );
//    $('table').bootstrapTable();
} );
