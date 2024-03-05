    const table = document.getElementById("generatedTable");
    function generateTable() {
        var tableSize = parseInt(document.getElementById('tableSize').value);
        if (isNaN(tableSize) || tableSize <= 0) {
            alert("Введите корректный размер таблицы!");
            return;
        }
        table.innerHTML = '';

        for (var i = 0; i < tableSize; i++) {
            var row = table.insertRow(i);

            for (var j = 0; j < tableSize; j++) {
                var cell = row.insertCell(j);
                cell.textContent = Math.floor(Math.random() * 100) + 1;
                cell.addEventListener("click", highlightCell);
            }
        }
    }

    const transposeButton = document.getElementById("transposeButton");
    transposeButton.addEventListener("click", () => {
            let rows = table.rows;
            let cols = rows[0].cells.length;

            let transposedTable = [];

            for (let j = 0; j < cols; j++) {
                transposedTable[j] = [];

                for (let i = 0; i < rows.length; i++) {
                    transposedTable[j][i] = rows[i].cells[j].textContent;
                }
            }

            // Очищаем предыдущее содержимое таблицы
            table.innerHTML = "";

            for (let i = 0; i < transposedTable.length; i++) {
                let row = table.insertRow();

                for (let j = 0; j < transposedTable[i].length; j++) {
                    let cell = row.insertCell();
                    cell.textContent = transposedTable[i][j];
                    cell.addEventListener("click", highlightCell);
                }
            }
        }
    );
    function addRow() {
        var table = document.getElementById('generatedTable');
        var newRow = table.insertRow(-1);
        var columns = table.rows[0].cells.length;

        for (var i = 0; i < columns; i++) {
            var cell = newRow.insertCell(i);
            cell.textContent = Math.floor(Math.random() * 100) + 1;
            cell.addEventListener('click', highlightCell);
        }
    }

    function addColumn() {
        var table = document.getElementById('generatedTable');
        var rows = table.getElementsByTagName('tr');

        for (var i = 0; i < rows.length; i++) {
            var cell = rows[i].insertCell(-1);
            cell.textContent = Math.floor(Math.random() * 100) + 1;
            cell.addEventListener('click',
                highlightCell);
        }
    }
    // Функция для выделения ячеек цветом
    function highlightCell(event) {
        let cell = event.target;
        let row = cell.parentNode;
        console.log(row);
        console.log(table);
        let columnIndex = cell.cellIndex;

        // Получаем значение ограничения для количества выделенных ячеек
        let limit = parseInt(document.getElementById("limitInput").value);

        let highlightedCountRow = 0;
        for (let cell of row.cells) {
            if (cell.classList.contains("highlight-even") || cell.classList.contains("highlight-odd")) {
                ++highlightedCountRow;
            }
        }

        let highlightedCountCol = 0;
        let col = []
        for (let row of table.rows) {
            col.push(row.cells[cell.cellIndex]);
        }

        for (let cell of col) {
            if (cell.classList.contains("highlight-even") || cell.classList.contains("highlight-odd")) {
                ++highlightedCountCol;
            }
        }
        let isNotLimited = highlightedCountRow < limit && highlightedCountCol < limit;
        let isHighlighted = cell.classList.contains("highlight-even") || cell.classList.contains("highlight-odd");

        let hasLeftNeighbor;
        if (columnIndex === 0) {
            hasLeftNeighbor = false;
        } else {
            hasLeftNeighbor = columnIndex > 0 && row.cells[columnIndex - 1].classList.contains("highlight-even") || row.cells[columnIndex - 1].classList.contains("highlight-odd");
        }
        let hasRightNeighbor;
        if (columnIndex === row.cells.length - 1) {
            hasRightNeighbor = false;
        } else {
            hasRightNeighbor = columnIndex < row.cells.length - 1 && row.cells[columnIndex + 1].classList.contains("highlight-even") || row.cells[columnIndex + 1].classList.contains("highlight-odd");
        }

        if (!isHighlighted) {
            if (isNotLimited && (!hasLeftNeighbor) && (!hasRightNeighbor)) {
                if (parseInt(cell.textContent) % 2 === 0) {
                    cell.classList.add("highlight-even");
                } else {
                    cell.classList.add("highlight-odd");
                }
            }
        } else {
            cell.classList.remove("highlight-even", "highlight-odd");
        }

    }