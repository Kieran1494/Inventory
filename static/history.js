var table = new Tabulator("#database", {
    selectable: 1, //make rows selectable
    layout: "fitColumns",
    height: "311px",
    columns: [
        {title: "Name", field: "name", align: "center"},
        {title: "To", field: "to", align: "center"},
        {title: "From", field: "from", align: "center"},
        {title: "Time Out", field: "tout", align: "center"},
        {title: "Time Reached", field: "tin", align: "center"},
        {title: "Date", field: "date", align: "center"}
    ],
    rowSelectionChanged: function (data, rows) {
        //update selected row counter on selection change
        $("#select-stats span").text(data.length);
    },
});
var logs = log["items"];
for (var i = 0; i < logs.length; i++) {
    var tin = new Date(logs[i]["tin"]);
    var tout = new Date(logs[i]["tout"]);
    console.log(tin.toUTCString());
    console.log(tout.toUTCString());
    logs[i]["date"] = tin.toLocaleDateString();
    logs[i]["tin"] = formatTime(tin);
    logs[i]["tout"] = formatTime(tout);
}
table.setData(logs);

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