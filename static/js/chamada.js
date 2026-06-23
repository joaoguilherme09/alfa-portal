// chamada.js — Alfa Profissionalizantes
// Controle da tela de chamada do professor

function toggleStatus(id) {
  const btn  = document.getElementById('btn-' + id);
  const card = document.getElementById('card-' + id);

  if (btn.classList.contains('presente')) {
    btn.classList.replace('presente', 'falta');
    btn.querySelector('.status-icone').textContent = '❌';
    btn.querySelector('.status-texto').textContent = 'Falta';
    card.classList.add('card-falta-ativo');
  } else {
    btn.classList.replace('falta', 'presente');
    btn.querySelector('.status-icone').textContent = '✅';
    btn.querySelector('.status-texto').textContent = 'Presente';
    card.classList.remove('card-falta-ativo');
  }
}