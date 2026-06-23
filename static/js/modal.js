// modal.js — Alfa Profissionalizantes
// Controle genérico de modais

function abrirModal(id) {
  document.getElementById('overlay-' + id).classList.remove('oculto');
  document.getElementById(id).classList.remove('oculto');
}

function fecharModal(id) {
  document.getElementById('overlay-' + id).classList.add('oculto');
  document.getElementById(id).classList.add('oculto');
}