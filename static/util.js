var url = "select_item";


if (document.getElementById("movable").checked) {
    document.getElementById('movablehidden').disabled = true;
}

var table = new Tabulator("#database", {
    height: "311px",
    layout: "fitColumns",
    selectable: 1, //make rows selectable
    columns: [
        {title: "Name", field: "name"},
        {title: "Make", field: "make"},
        {title: "Model", field: "model"},
        {title: "ID", field: "ID", align: "center", sorter: "number"},
        {title: "Room", field: "room"},
        {title: "Teacher", field: "teacher", align: "center"},
        {title: "Manual", field: "manual", align: "center"},
        {title: "Condition", field: "condition", align: "center"},
        {title: "Movable", field: "movable", align: "center"},
        {title: "Description", field: "description", align: "center"},
        {title: "Hidden", field: "hidden", align: "center"},
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
    var selectedRows = table.getSelectedRows();
    alert(selectedRows.toString());
});

// function highlight_row() {
//     var table = document.getElementById('database');
//     var cells = table.getElementsByTagName('td');
//
//
//     for (var i = 0; i < cells.length; i++) {
//         // Take each cell
//         var cell = cells[i];
//         // do something on onclick event for cell
//         cell.onclick = function () {
//             // Get the row id where the cell exists
//             var rowId = this.parentNode.rowIndex;
//
//             var rowsNotSelected = table.getElementsByTagName('tr');
//             for (var row = 0; row < rowsNotSelected.length; row++) {
//                 rowsNotSelected[row].style.backgroundColor = "";
//                 rowsNotSelected[row].classList.remove('selected');
//             }
//             var rowSelected = table.getElementsByTagName('tr')[rowId];
//             rowSelected.style.backgroundColor = "black";
//             rowSelected.className += " selected";
//             $.post(url, {hidden: rowSelected.cells[10].innerHTML}, function () {
//             });
//
//         }
//     }
//
// } //end of function

// window.onload = highlight_row;