$("#submit").click(function () {
    //set checkout url
    var url = "add_another";
    //get which item
    var item_check = localStorage.getItem("item");
    //get form info
    var form = $('#add_another').serializeArray();
    //correct formatting
    var checkoutInfo = {};
    form.forEach(function (item, index) {
        checkoutInfo[item["name"]] = item["value"];
    });
    //add hidden id
    checkoutInfo["hidden"] = item_check;
    //send post
    post(url, checkoutInfo);
    //report success
    swal({
        title: "Addition Successful",
        icon: "success",
    });
});