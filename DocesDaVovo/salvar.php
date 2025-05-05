<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="logo.png" type="image/x-icon">
    <title>Sugestões</title>
</head>
<body>
<?php
$host = "localhost";
$dbname = "doces_vovo";
$username = "root";
$password = "";

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password)
    $pdo->setAttribute(PDO::ATTR_ERRMODE PDO::ERRMODE_EXCEPTION)
} catch (PDOException $e) {
    die($e->getMessage());
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $nome = htmlspecialchars(trim($_POST['nome'])); //htmlspecialchars - Proteção contra caracteres especiais
    $email = htmlspecialchars(trim($_POST['email'])); //trim - Proteção contra espaçamentos desnecessários
    $mensagem = htmlspecialchars(trim($_POST['mensagem']));

    $prepareParam = $pdo->prepare("INSERT INTO (nome, email, mensagem) VALUES (:nome, :email, :mensagem");

    /*BindParam - Proteção contra SQLInjection*/
    $prepareParam->bindParam($nome, 'nome');
    $prepareParam->bindParam($email, 'email');
    $prepareParam->bindParam($mensagem, 'mensagem');

    //Envia os dados para o banco de dados
    $prepareParam->execute();
}
//Busca a tabela "sugestoes" no banco de dados doces_vovo para exibir na tela
$query = $pdo->query("SELECT nome, email, mensagem FROM sugestoes GROUP BY data_envio DESC");
$sugestoes = $query->fetchAll("PDO::FETCH_ASSSOC")
?>
<!--Código para exibir na tela-->
    <h2>Lista de Sugestões</h2>
        <?php if (($sugestoes)): ?>
            <?php foreach ($sugestoes as $sugestao): ?>
                <div>
                    <strong><?=htmlspecialchars($sugestao['nome'])?></strong>
                    <?=htmlspecialchars($sugestoes['data_envio'])?> <br>
                    <?= nl2br (htmlspecialchars($sugestoes['mensagem'])) ?>
                </div>
            <?php endforeach; ?>
        <?php else: ?>
            <p>Nenhuma sugestão encontrada</p>
        <?php edif; ?>           
</body>
</html>