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
    $('table').bootstrapTable({reorderableColumns: true});
    $('table').on("column-switch.bs.table", function(arg1, arg2, arg3, arg4,arg5,arg6){
        console.log(arg1,arg2,arg3,arg4,arg5,arg6);
    });

    $('body').taggingAjax({});
    $('table').on('editable-save.bs.table', function(event, rowIndex, rowArray, oldValue, editableElement){
      console.log("onEditableSave", event, rowIndex, rowArray, editableElement);
      //var
      var newTag = rowArray[1];
      var infoElem = $("td.row_info span", $(editableElement.parents("tr")[0]));
      var objectId = infoElem.attr("objectId");
      var contentType = infoElem.attr("contentType");
      $('body').taggingAjax("setTagForItem", newTag, objectId, contentType, function(){
            editableElement.toggleClass("editable-unsaved");
        });
        return true;
    });
    $('table td:first-child').each(function(){
        var hrefTagStart = '<a href="'+ admin_base_url;
        $(this).html(hrefTagStart.replace('%d', $(this).text())+'" target="_blank">'+$(this).text()+'</a>');
    });
});
