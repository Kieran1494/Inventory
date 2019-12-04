// make movable true false not only true
if (document.getElementById("movable").checked) {
    document.getElementById('movablehidden').disabled = true;
}

// database table
var table = new Tabulator("#database", {
    selectable: 1, //make rows selectable
    layout: "fitColumns",
    height: "311px",
    columns: [
        {title: "Name", field: "name", align: "center"},
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

function matchAny(data, filterParams) {
    //data - the data for the row being filtered
    //filterParams - params object passed to the filter

    var match = false;

    for (var key in data) {
        if (JSON.stringify(data[key]).toLowerCase().search(filterParams.value) !== -1) {
            match = true;
        }
    }

    return match;
}

$("#Search").keyup(function () {
    table.setFilter(matchAny, {value: $("#Search").val().toLowerCase()});
    if ($("#Search").val() === " ") {
        table.clearFilter()
    }
});

// set database items
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

/**
 * checkout selected item
 */
$("#checkout").click(function () {
    if (getItemInfo("movable") !== "Yes") {
        swal({
            title: "item is not movable",
            icon: "error",
        });
    } else {
        sendItem("checkout")
    }
});

/**
 * request history of selected item
 */
$("#history").click(function () {
    sendItem("history")
});

/**
 * send the hidden id to python at url
 * @param url the url to send the id to
 */
function sendItem(url) {
    var info = getItemInfo("hidden", true);
    localStorage.setItem("item", info[0]);
    post(url, info[1]);
}

function getItemInfo(key, full = false) {
    var item = table.getSelectedData();
    if (item && item.length && item[0]) {
        item = item[0];
        if (!full) {
            return item[key];
        } else {
            return [item[key], item]
        }
    }
    swal({
        title: "No Item Selected",
        icon: "error",
    });
}