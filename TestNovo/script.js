document
  .getElementById("feedbackForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const turma = document.getElementById("turma").value;
    const sentimento = document.getElementById("sentimento").value;
    const mensagem = document.getElementById("mensagem").value;

    console.log("Turma:", turma);
    console.log("Sentimento:", sentimento);
    console.log("Mensagem:", mensagem);

    const status = document.getElementById("mensagemStatus");
    status.textContent = "Obrigado pela suas palavras!";
    status.style.display = "block";

    this.reset();
  });
