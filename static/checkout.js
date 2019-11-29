$("#checkout_item").click(function () {
    var item_check = localStorage.getItem("item");
    var checkoutInfo = $('#checkout').serializeArray();
    Object.assign(checkoutInfo, {"item": item_check});
    post(url, checkoutInfo);
});