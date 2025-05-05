<?php
$conn = new mysqli("localhost", "root", "", "escola");

if ($conn->connect_error) {
    die("Erro de conexão: " . $conn->connect_error);
}

$result = $conn->query("SELECT * FROM alunos");

echo "<h1>Lista de Alunos</h1>";

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        echo "ID: " . $row["id"] . " - Nome: " . $row["nome"] . " - Email: " . $row["email"] . "<br>";
    }
} else {
    echo "Nenhum aluno cadastrado.";
}

$conn->close();
?>
