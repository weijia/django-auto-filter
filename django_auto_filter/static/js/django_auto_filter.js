$(document).ready( function () {
//    $('table').dragtable({
//        dragHandle:'.th-inner'
////        dragaccept:'th-inner'
//    });
//    $('table').DataTable( {
////        dom: 'Bfrtip',
//        dom: 'BHt',
//        buttons: [ 'colvis' ],
//        scrollX: true
//    } );
//    $('table').bootstrapTable();
    $('table').bootstrapTable();
    $('body').taggingAjax({});
    $('table').on('editable-save.bs.table', function(event, rowIndex, rowArray, oldValue, editableElement){
      console.log("onEditableSave", event, rowIndex, rowArray, editableElement);
      //var
      $('body').taggingAjax("setTagForItem", rowArray[1], $(rowArray[25]).attr("objectId"),
        $(rowArray[25]).attr("contentType"), function(){
            editableElement.toggleClass("editable-unsaved");
        });
        return true;
    });
    $('table td:first-child').each(function(){
        var hrefTagStart = '<a href="'+ admin_base_url;
        $(this).html(hrefTagStart.replace('%d', $(this).text())+'">'+$(this).text()+'</a>');
    });
});
