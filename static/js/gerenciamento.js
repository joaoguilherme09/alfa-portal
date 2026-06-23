// gerenciamento.js — Alfa Profissionalizantes

// ===== ABAS =====
function trocarAba(aba, botao) {
  document.querySelectorAll('.painel-aba').forEach(p => p.classList.add('oculto'));
  document.querySelectorAll('.aba').forEach(b => b.classList.remove('ativa'));
  document.getElementById('painel-' + aba).classList.remove('oculto');
  botao.classList.add('ativa');
}

// ===== MODAIS =====
function abrirModal(id) {
  document.getElementById('overlay-' + id).classList.remove('oculto');
  document.getElementById(id).classList.remove('oculto');
}

function fecharModal(id) {
  document.getElementById('overlay-' + id).classList.add('oculto');
  document.getElementById(id).classList.add('oculto');
}

// ===== MATRÍCULA =====
function abrirModalMatricula(alunoId, nomeAluno) {
  document.getElementById('input-aluno-id-matricula').value = alunoId;
  document.getElementById('nome-aluno-matricula').textContent = nomeAluno;
  abrirModal('modal-matricula');
}

// ===== EDITAR ALUNO =====
function abrirModalEditar(alunoId) {
  fetch(`/professor/buscar_aluno/${alunoId}`)
    .then(r => r.json())
    .then(a => {
      document.getElementById('edit-aluno-id').value             = a.id;
      document.getElementById('edit-nome-responsavel').value     = a.nome_responsavel;
      document.getElementById('edit-nasc-responsavel').value     = a.nascimento_responsavel;
      document.getElementById('edit-cpf').value                  = a.cpf_responsavel;
      document.getElementById('edit-rg').value                   = a.rg_responsavel;
      document.getElementById('edit-telefone').value             = a.telefone_responsavel;
      document.getElementById('edit-nome-aluno').value           = a.nome;
      document.getElementById('edit-nasc-aluno').value           = a.nascimento;
      document.getElementById('edit-endereco').value             = a.endereco;
      document.getElementById('edit-numero').value               = a.numero;
      document.getElementById('edit-bairro').value               = a.bairro;
      document.getElementById('edit-cidade').value               = a.cidade;
      document.getElementById('edit-cep').value                  = a.cep;
      document.getElementById('edit-senha').value                = a.senha;
      document.getElementById('edit-periodo').value              = a.periodo;
      if (a.turma_id) document.getElementById('edit-turma').value = a.turma_id;
      abrirModal('modal-editar-aluno');
    });
}

// ===== EDITAR PROFESSOR =====
function abrirModalEditarProfessor(profId) {
  fetch(`/professor/buscar_professor/${profId}`)
    .then(r => r.json())
    .then(p => {
      document.getElementById('edit-prof-id').value        = p.id;
      document.getElementById('edit-prof-nome').value      = p.nome;
      document.getElementById('edit-prof-matricula').value = p.matricula;
      document.getElementById('edit-prof-cargo').value     = p.cargo;
      abrirModal('modal-editar-professor');
    });
}

// ===== EDITAR TURMA =====
function abrirModalEditarTurma(turmaId) {
  fetch(`/professor/buscar_turma/${turmaId}`)
    .then(r => r.json())
    .then(t => {
      document.getElementById('edit-turma-id').value       = t.id;
      document.getElementById('edit-turma-nome').value     = t.nome;
      document.getElementById('edit-turma-curso').value    = t.curso_id;
      document.getElementById('edit-turma-professor').value = t.professor_id;
      document.getElementById('edit-turma-horario').value  = t.horario;
      document.getElementById('edit-turma-periodo').value  = t.periodo;

      // Marcar dias da semana
      const dias = t.dias_semana.split(',');
      document.querySelectorAll('.edit-dia-check').forEach(cb => {
        cb.checked = dias.includes(cb.value);
      });

      abrirModal('modal-editar-turma');
    });
}

// Atualiza editar aluno para marcar turmas
function abrirModalEditar(alunoId) {
  fetch(`/professor/buscar_aluno/${alunoId}`)
    .then(r => r.json())
    .then(a => {
      document.getElementById('edit-aluno-id').value             = a.id;
      document.getElementById('edit-nome-responsavel').value     = a.nome_responsavel;
      document.getElementById('edit-nasc-responsavel').value     = a.nascimento_responsavel;
      document.getElementById('edit-cpf').value                  = a.cpf_responsavel;
      document.getElementById('edit-rg').value                   = a.rg_responsavel;
      document.getElementById('edit-telefone').value             = a.telefone_responsavel;
      document.getElementById('edit-nome-aluno').value           = a.nome;
      document.getElementById('edit-nasc-aluno').value           = a.nascimento;
      document.getElementById('edit-endereco').value             = a.endereco;
      document.getElementById('edit-numero').value               = a.numero;
      document.getElementById('edit-bairro').value               = a.bairro;
      document.getElementById('edit-cidade').value               = a.cidade;
      document.getElementById('edit-cep').value                  = a.cep;
      document.getElementById('edit-senha').value                = a.senha;
      document.getElementById('edit-periodo').value              = a.periodo;

      // Marcar turmas
      document.querySelectorAll('.edit-turma-check').forEach(cb => {
        cb.checked = a.turmas.includes(parseInt(cb.value));
      });

      abrirModal('modal-editar-aluno');
    });
}