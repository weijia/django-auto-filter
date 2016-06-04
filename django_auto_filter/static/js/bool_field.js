function toggleValue(e){
    console.log(e);
    var evTarget = $(e.currentTarget);
    var value = evTarget.attr("class");
    var td = evTarget.parent();
    var fieldName = td.attr("class");
    var data =  new Object();
    data[fieldName] = false;
    var finalChar = "✘";
    if(value=="false"){
        data[fieldName] = true;
        finalChar = "✔";
    }
    var row = $(evTarget.parents("tr")[0]);
    var idStr = $($("td a", row)[0]).text();
    $("body").restApi("updateItem", idStr, data, function(data){
        evTarget.attr("class", data[fieldName]);
        evTarget.text(finalChar);
    });
}


$(document).ready( function () {
    $("body").on("click", ".true", toggleValue);
    $("body").on("click", ".false", toggleValue);
    $("body").restApi({});
});
