var url = "select_item";


if (document.getElementById("movable").checked) {
    document.getElementById('movablehidden').disabled = true;
}

function highlight_row() {
    var table = document.getElementById('database');
    var cells = table.getElementsByTagName('td');


    for (var i = 0; i < cells.length; i++) {
        // Take each cell
        var cell = cells[i];
        // do something on onclick event for cell
        cell.onclick = function () {
            // Get the row id where the cell exists
            var rowId = this.parentNode.rowIndex;

            var rowsNotSelected = table.getElementsByTagName('tr');
            for (var row = 0; row < rowsNotSelected.length; row++) {
                rowsNotSelected[row].style.backgroundColor = "";
                rowsNotSelected[row].classList.remove('selected');
            }
            var rowSelected = table.getElementsByTagName('tr')[rowId];
            rowSelected.style.backgroundColor = "black";
            rowSelected.className += " selected";
            $.post(url, {hidden: rowSelected.cells[10].innerHTML}, function () {
            });

        }
    }

} //end of function

window.onload = highlight_row;