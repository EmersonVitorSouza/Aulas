document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formCadastro");
  const btnExibir = document.getElementById("btnExibir");
  const mensagem = document.getElementById("mensagem");
  const resultado = document.getElementById("resultado");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;

    fetch("/cadastrar", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `nome=${encodeURIComponent(nome)}&email=${encodeURIComponent(
        email
      )}`,
    })
      .then((res) => res.text())
      .then((data) => {
        mensagem.innerText = data;
        form.reset();
        exibirAlunos(); // Recarrega a lista após cadastro
      })
      .catch((err) => {
        console.error(err);
        mensagem.innerText = "Erro ao cadastrar.";
      });
  });

  btnExibir.addEventListener("click", function () {
    exibirAlunos();
  });

  function exibirAlunos() {
    fetch("/exibir")
      .then((res) => res.json())
      .then((alunos) => {
        let html = "";
        alunos.forEach((a) => {
          html += `<tr><td>${a.id}</td><td>${a.nome}</td><td>${a.email}</td></tr>`;
        });
        resultado.innerHTML =
          html || "<p colspan='3'>Nenhum aluno encontrado.</p>";
      })
      .catch((err) => {
        console.error(err);
        resultado.innerHTML =
          "<tr><td colspan='3'>Erro ao carregar alunos.</td></tr>";
      });
  }
});
