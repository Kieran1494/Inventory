if (document.getElementById("movable").checked) {
    document.getElementById('movablehidden').disabled = true;
}

var table = new Tabulator("#database", {
    layout: "fitDataFill",
    selectable: 1, //make rows selectable
    columns: [
        {title: "Name", field: "name", align: "center", widthShrink: true},
        {title: "Make", field: "make", align: "center"},
        {title: "Model", field: "model", align: "center"},
        {title: "ID", field: "ID", align: "center", sorter: "number"},
        {title: "Room", field: "room", align: "center"},
        {title: "Teacher", field: "teacher", align: "center"},
        {title: "Manual", field: "manual", align: "center"},
        {title: "Condition", field: "condition", align: "center"},
        {title: "Movable", field: "movable", align: "center"},
        {title: "Description", field: "description", align: "center"},
        {title: "Hidden", field: "hidden", align: "center", visible: false},
    ],
    rowSelectionChanged: function (data, rows) {
        //update selected row counter on selection change
        $("#select-stats span").text(data.length);
    },
});
data = items["items"];
table.setData(data);

//select row on "select" button click
$("#select-row").click(function () {
    table.selectRow(1);
});

//deselect row on "deselect" button click
$("#deselect-row").click(function () {
    table.deselectRow(1);
});

//select row on "select all" button click
$("#select-all").click(function () {
    table.selectRow();
});

//deselect row on "deselect all" button click
$("#deselect-all").click(function () {
    table.deselectRow();
});

$("#checkout").click(function () {
    var item;
    var url = "checkout";
    item = table.getSelectedData();
    if (item && item.length && item[0]) {
        item = item[0];
        var key = item["hidden"];
        localStorage.setItem("item", key);
        post(url, item);
    } else {
        swal({
            title: "No Item Selected",
            icon: "error",
        });
    }
});