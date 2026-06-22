// faltas.js — Alfa Profissionalizantes

function toggleMes(num) {
  const detalhe = document.getElementById('detalhe-' + num);
  const seta    = document.getElementById('seta-'    + num);

  detalhe.classList.toggle('oculto');
  seta.classList.toggle('aberta');
}