// matricula.js — Alfa Profissionalizantes
// Controle do modal de matrícula

function abrirModalMatricula(alunoId, nomeAluno) {
  document.getElementById('input-aluno-id-matricula').value = alunoId;
  document.getElementById('nome-aluno-matricula').textContent = nomeAluno;
  abrirModal('modal-matricula');
}