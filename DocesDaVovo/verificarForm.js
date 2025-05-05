document.addEventListener("DOMContentLoaded", function() {
    const enviarBotao = document.getElementById("enviarBotao");

    enviarBotao.addEventListener("click", function(event) {
        event.preventDefault();

        const nome = document.getElementById("nome").value.trim();
        const email = document.getElementById("email").value.trim();
        const mensagem = document.getElementById("mensagem").value.trim();
        /*Verificar o campo Nome*/

        if (nome === "") {
            document.getElementById("error").innerText = "Por favor, preencha o nome!";
            return;
        }
        /*Verificar o campo E-mail*/
        if (email === "" || !email.includes("@") || !email.includes(".")) {
            document.getElementById("error").innerText = "Por favor, preencha um e-mail válido!";
            return;
        }
        /*Verificar o campo Mesnagem*/
        if (mensagem === "") {
            document.getElementById("error").innerText = "Por favor, digite uma mensagem!";
            return;
        } else {
        document.getElementById("sugestaoForm").onsubmit(); /*Iniciar o PHP*/
            document.getElementById("error").innerText = "Mensagem enviada com sucesso!"
        }

    });
    /*Limpar os campos*/
    document.getElementById("nome").value == "";
    document.getElementById("email").value == "";
    document.getElementById("mensagem").value == "";
})