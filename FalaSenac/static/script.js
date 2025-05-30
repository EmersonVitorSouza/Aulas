document
  .getElementById("formulario")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const turma = document.getElementById("turma").value;
    const sentimento = document.getElementById("sentimento").value;
    const turno = document.getElementById("turno").value;

    const formData = new FormData();
    formData.append("turma", turma);
    formData.append("sentimento", sentimento);
    formData.append("turno", turno);

    fetch("/enviar", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        const status = document.getElementById("mensagemStatus");
        status.textContent = data.msg;
        status.style.display = "block";
        status.style.color = data.success ? "green" : "red";
        if (data.success) {
          document.getElementById("formulario").reset();
        }
      })
      .catch((error) => {
        console.error("Erro:", error);
      });
  });
