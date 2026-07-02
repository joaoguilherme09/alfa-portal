// sidebar.js — Alfa Profissionalizantes

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('overlay');
  sidebar.classList.toggle('aberta');
  overlay.classList.toggle('visivel');
}


function toggleSino() {
  const dropdown = document.getElementById('sino-dropdown');
  dropdown.classList.toggle('oculto');
  if (!dropdown.classList.contains('oculto')) {
    carregarNotificacoes();
  }
}

function carregarNotificacoes() {
  fetch('/aluno/notificacoes')
    .then(r => r.json())
    .then(data => {
      const badge = document.getElementById('sino-badge');
      const conteudo = document.getElementById('sino-conteudo');

      if (data.total > 0) {
        badge.style.display = 'flex';
        badge.textContent = data.total;
      } else {
        badge.style.display = 'none';
      }

      let html = '';

      data.notas.forEach(n => {
        html += `<div class="sino-item">
          <span class="sino-item-icone">📝</span>
          <div class="sino-item-texto">
            Nova nota: <strong>${n.nome_atividade}</strong> — ${n.valor}
            <div class="sino-item-data">${n.data}</div>
          </div>
        </div>`;
      });

      data.faltas.forEach(f => {
        html += `<div class="sino-item">
          <span class="sino-item-icone">⚠️</span>
          <div class="sino-item-texto">
            Falta registrada em <strong>${f.turma}</strong>
            <div class="sino-item-data">${f.data}</div>
          </div>
        </div>`;
      });

      data.comunicados.forEach(c => {
        html += `<div class="sino-item">
          <span class="sino-item-icone">📢</span>
          <div class="sino-item-texto">
            Comunicado: <strong>${c.titulo}</strong>
            <div class="sino-item-data">${c.data}</div>
          </div>
        </div>`;
      });

      conteudo.innerHTML = html || '<p class="sino-vazio">Nenhuma notificação recente.</p>';
    });
}

// Fechar ao clicar fora
document.addEventListener('click', function(e) {
  const wrapper = document.getElementById('sino-wrapper');
  if (wrapper && !wrapper.contains(e.target)) {
    document.getElementById('sino-dropdown')?.classList.add('oculto');
  }
});

// Carregar badge ao abrir a página
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('sino-badge')) {
    fetch('/aluno/notificacoes')
      .then(r => r.json())
      .then(data => {
        if (data.total > 0) {
          const badge = document.getElementById('sino-badge');
          badge.style.display = 'flex';
          badge.textContent = data.total;
        }
      });
  }
});