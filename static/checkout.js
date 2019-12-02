$("#checkout_item").click(function () {
    var url = "checkout_item";
    var item_check = localStorage.getItem("item");
    var form = $('#checkout').serializeArray();
    var checkoutInfo = {};
    form.forEach(function (item, index) {
        console.log(item, index);
        checkoutInfo[item["name"]] = item["value"];
    });
    checkoutInfo["hidden"] = item_check;
    post(url, checkoutInfo);
    swal({
        title: "Checkout Successful",
        icon: "success",
    });
});
$("#tin, #tout").clockpicker();