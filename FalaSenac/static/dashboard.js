document.addEventListener("DOMContentLoaded", () => {
  const dadosPorTurma = window.dadosDashboard; // setado no HTML como variável global
  const turmaSelect = document.getElementById("turmaSelect");
  const grafico = document.getElementById("grafico");
  const tabelaMensagens = document.getElementById("tabelaMensagens");

  function renderizarDashboard(turma) {
    const dados = dadosPorTurma[turma];
    if (!dados) return;

    // Gráfico de sentimentos
    const sentimentos = {
      "feliz": 0,
      "triste": 0,
      "ansioso": 0,
      "nervoso": 0,
      "outro": 0
    };

    dados.forEach(msg => {
      const sentimento = msg.sentimento.toLowerCase();
      if (sentimentos[sentimento] !== undefined) {
        sentimentos[sentimento]++;
      }
    });

    const labels = Object.keys(sentimentos);
    const valores = Object.values(sentimentos);

    grafico.innerHTML = `<canvas id="graficoSentimentos"></canvas>`;
    new Chart(document.getElementById("graficoSentimentos"), {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Sentimentos",
          data: valores,
          backgroundColor: ["#005bab", "#f58220", "#e65c00", "#aaa", "#888"]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          title: { display: true, text: `Sentimentos da turma ${turma}` }
        }
      }
    });

    // Tabela de mensagens
    tabelaMensagens.innerHTML = `
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Sentimento</th>
            <th>Turno</th>
          </tr>
        </thead>
        <tbody>
          ${dados.map(msg => `
            <tr>
              <td>${msg.nome}</td>
              <td>${msg.sentimento}</td>
              <td>${msg.turno}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    `;
  }

  turmaSelect.addEventListener("change", () => {
    renderizarDashboard(turmaSelect.value);
  });

  renderizarDashboard(turmaSelect.value); // render inicial
});
