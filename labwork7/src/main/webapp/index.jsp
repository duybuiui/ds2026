<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <title>Sudoku GAE</title>
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; }
        table { border-collapse: collapse; margin-top: 20px; }
        td { border: 1px solid black; width: 40px; height: 40px; text-align: center; padding: 0; }
        input { width: 100%; height: 100%; text-align: center; font-size: 20px; border: none; outline: none; }
        tr:nth-child(3n) td { border-bottom: 2px solid black; }
        td:nth-child(3n) { border-right: 2px solid black; }
        tr:first-child td { border-top: 2px solid black; }
        td:first-child { border-left: 2px solid black; }
        button { margin-top: 20px; padding: 10px 20px; font-size: 16px; }
    </style>
</head>
<body>
    <h1>Sudoku on Google App Engine</h1>
    <table id="grid"></table>
    <button onclick="checkSolution()">Check Solution</button>
    <script>
        const board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ];
        
        const table = document.getElementById('grid');
        for (let i = 0; i < 9; i++) {
            const tr = document.createElement('tr');
            for (let j = 0; j < 9; j++) {
                const td = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                if (board[i][j] !== 0) {
                    input.value = board[i][j];
                    input.readOnly = true;
                    input.style.backgroundColor = '#eee';
                }
                td.appendChild(input);
                tr.appendChild(td);
            }
            table.appendChild(tr);
        }

        function checkSolution() {
            alert('Sudoku logic check implemented here.');
        }
    </script>
</body>
</html>