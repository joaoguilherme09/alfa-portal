// notas.js — Alfa Profissionalizantes

function trocarAba(aba, botao) {
  document.querySelectorAll('.painel-aba').forEach(p => p.classList.add('oculto'));
  document.querySelectorAll('.aba').forEach(b => b.classList.remove('ativa'));
  document.getElementById('painel-' + aba).classList.remove('oculto');
  botao.classList.add('ativa');
}