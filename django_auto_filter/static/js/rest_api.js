$.widget( "rest_api.restApi", {
    options: {
        title: ""
    },

    _create: function() {
//        this.element.on("click", ".add-item", function(ev){
//                var addButton = $(ev.target);
//                var liElem = thisWidget.getFirstParent(addButton, "li");
//                thisWidget.element.treeEditor("insertChildBefore", liElem, function(childElem){
//                    thisWidget.onAddChecklistContent(childElem);
//                });
//            }
//        );
    },

    updateItem: function(itemId, data, success){
          $.ajax({
              url : model_rest_api_url+itemId+"/",
              data : JSON.stringify(data),
              type : 'PATCH',
              contentType : 'application/json',
              processData: false,
              dataType: 'json',
              success: function(data){
                if(success){
                        success(data);
                    }
              }
        });
    }
});
