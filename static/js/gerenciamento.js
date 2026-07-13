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

  if (id === 'modal-aluno') {
    fetch('/professor/ultima_matricula')
      .then(r => r.json())
      .then(data => {
        document.getElementById('hint-matricula').textContent =
          `Última: ${data.ultima} — Próxima sugerida: ${data.proxima}`;
        document.getElementById('input-matricula-manual').placeholder =
          `Sugerida: ${data.proxima}`;
      });
  }
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
      document.getElementById('edit-matricula').value = a.matricula;

      // Marcar turmas
      document.querySelectorAll('.edit-turma-check').forEach(cb => {
        cb.checked = a.turmas.includes(parseInt(cb.value));
      });

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
      document.getElementById('edit-turma-id').value      = t.id;
      document.getElementById('edit-turma-nome').value    = t.nome;
      document.getElementById('edit-turma-curso').value   = t.curso_id;
      document.getElementById('edit-turma-horario').value = t.horario;
      document.getElementById('edit-turma-periodo').value = t.periodo;

      // Marcar dias da semana
      const dias = t.dias_semana.split(',');
      document.querySelectorAll('.edit-dia-check').forEach(cb => {
        cb.checked = dias.includes(cb.value);
      });

      // Marcar professores
      document.querySelectorAll('.edit-prof-check').forEach(cb => {
        cb.checked = t.professores.includes(parseInt(cb.value));
      });

      abrirModal('modal-editar-turma');
    });
}

// ===== FOTO =====
document.addEventListener('change', function(e) {
  if (e.target.type === 'file' && e.target.accept.includes('image')) {
    const label = e.target.parentElement.querySelector('span');
    if (label) {
      label.textContent = e.target.files[0] ? e.target.files[0].name : 'Selecionar foto';
    }
  }
});


function confirmarDesativar(alunoId, nomeAluno) {
  if (confirm(`Deseja realmente desativar o aluno "${nomeAluno}"? Ele não conseguirá mais acessar o portal.`)) {
    fetch(`/professor/desativar_aluno/${alunoId}`, { method: 'POST' })
      .then(r => r.json())
      .then(data => {
        if (data.ok) {
          alert('Aluno desativado com sucesso!');
          location.reload();
        }
      });
  }
}




// ===== FILTROS DE ALUNOS =====
function filtrarAlunos() {
  const nome  = document.getElementById('filtro-nome').value.toLowerCase().trim();
  const curso = document.getElementById('filtro-curso').value.toLowerCase();
  const dia   = document.getElementById('filtro-dia').value.toLowerCase();

  document.querySelectorAll('#painel-alunos .card-ger').forEach(card => {
    const titulo = card.querySelector('.card-ger-titulo').textContent.toLowerCase();
    const sub    = card.querySelector('.card-ger-sub').textContent.toLowerCase();

    const matchNome  = !nome  || titulo.includes(nome) || sub.includes(nome);
    const matchCurso = !curso || sub.includes(curso);
    const matchDia   = !dia   || card.dataset.dias?.toLowerCase().includes(dia);

    card.style.display = (matchNome && matchCurso && matchDia) ? '' : 'none';
  });
}


function limparFiltros() {
  document.getElementById('filtro-nome').value  = '';
  document.getElementById('filtro-curso').value = '';
  document.getElementById('filtro-dia').value   = '';
  document.querySelectorAll('#painel-alunos .card-ger').forEach(card => {
    card.style.display = '';
  });
}


// ===== FILTROS DE TURMAS =====
function filtrarTurmas() {
  const nome    = document.getElementById('filtro-turma-nome').value.toLowerCase().trim();
  const curso   = document.getElementById('filtro-turma-curso').value.toLowerCase();
  const periodo = document.getElementById('filtro-turma-periodo').value.toLowerCase();
  const dia     = document.getElementById('filtro-turma-dia').value.toLowerCase();

  document.querySelectorAll('#lista-turmas .card-ger').forEach(card => {
    const titulo = card.querySelector('.card-ger-titulo').textContent.toLowerCase();
    const sub    = card.querySelector('.card-ger-sub').textContent.toLowerCase();

    const matchNome    = !nome    || titulo.includes(nome) || sub.includes(nome);
    const matchCurso   = !curso   || sub.includes(curso);
    const matchPeriodo = !periodo || sub.includes(periodo);
    const matchDia     = !dia     || sub.includes(dia);

    card.style.display = (matchNome && matchCurso && matchPeriodo && matchDia) ? '' : 'none';
  });
}

function limparFiltrosTurmas() {
  document.getElementById('filtro-turma-nome').value    = '';
  document.getElementById('filtro-turma-curso').value   = '';
  document.getElementById('filtro-turma-periodo').value = '';
  document.getElementById('filtro-turma-dia').value     = '';
  document.querySelectorAll('#lista-turmas .card-ger').forEach(card => {
    card.style.display = '';
  });
}