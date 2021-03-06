$("#checkout_item").click(function () {
    //set checkout url
    var url = "checkout_item";
    //get which item
    var item_check = localStorage.getItem("item");
    //get form info
    var form = $('#checkout').serializeArray();
    //correct formatting
    var checkoutInfo = {};
    form.forEach(function (item, index) {
        checkoutInfo[item["name"]] = item["value"];
    });
    //add hidden id
    checkoutInfo["hidden"] = item_check;
    //convert to utc
    checkoutInfo["tin"] = Date.today().at(checkoutInfo["tin"]).toISOString();
    checkoutInfo["tout"] = Date.today().at(checkoutInfo["tout"]).toISOString();
    //send post
    post(url, checkoutInfo);
    //report success
    swal({
        title: "Checkout Successful",
        icon: "success",
    });
});
//make those ids time selection
$("#tin, #tout").clockpicker();