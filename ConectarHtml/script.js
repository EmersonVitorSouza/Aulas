document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formCadastro");
    const btnExibir = document.getElementById("btnExibir");
    const mensagem = document.getElementById("mensagem");
    const listaAlunos = document.getElementById("listaAlunos");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const nome = document.getElementById("nome").value;
        const email = document.getElementById("email").value;

        const xhr = new XMLHttpRequest();
        xhr.open("POST", "cadastrar.php", true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.onload = function () {
            mensagem.innerHTML = this.responseText;
            form.reset();
        };
        xhr.send("nome=" + encodeURIComponent(nome) + "&email=" + encodeURIComponent(email));
    });

    btnExibir.addEventListener("click", function () {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "exibir.php", true);
        xhr.onload = function () {
            listaAlunos.innerHTML = this.responseText;
        };
        xhr.send();
    });
});
