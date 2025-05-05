<?php
$nome = $_POST['nome'];
$email = $_POST['email'];

$conn = new mysqli("localhost", "root", "", "escola");

if ($conn->connect_error) {
    die("Erro de conexão: " . $conn->connect_error);
}

$sql = "INSERT INTO alunos (nome, email) VALUES ('$nome', '$email')";

if ($conn->query($sql) === TRUE) {
    echo "Aluno cadastrado com sucesso!<br><a href='index.php'>Voltar</a>";
} else {
    echo "Erro: " . $conn->error;
}

$conn->close();
?>
