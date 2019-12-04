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
    //grab date
    var d = new Date();
    checkoutInfo["date"] = d.toLocaleDateString();
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