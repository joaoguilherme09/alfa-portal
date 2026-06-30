// chamada.js — Alfa Profissionalizantes

let turmaSelecionadaId = null;
let dataSelecionada    = null;
let statusAlunos       = {};

const DIAS_SEMANA = {
  'Segunda': 1, 'Terça': 2, 'Quarta': 3,
  'Quinta': 4, 'Sexta': 5, 'Sábado': 6, 'Domingo': 0
};

const MESES_PT = [
  'Janeiro','Fevereiro','Março','Abril','Maio','Junho',
  'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'
];

// ===== ABRIR CALENDÁRIO =====
function abrirCalendario() {
  const select = document.getElementById('select-turma-falta');
  turmaSelecionadaId = select.value;
  const turmaLabel   = select.options[select.selectedIndex].text;
  const diasStr      = select.options[select.selectedIndex].dataset.dias;

  if (!turmaSelecionadaId) { alert('Selecione uma turma!'); return; }

  const diasTurma = diasStr.split(',').map(d => d.trim());
  const hoje      = new Date();
  const ano       = hoje.getFullYear();
  const mes       = hoje.getMonth(); // 0-indexado

  document.getElementById('cal-titulo').textContent    = turmaLabel;
  document.getElementById('cal-subtitulo').textContent = `${MESES_PT[mes]} ${ano}`;

  // Buscar chamadas já feitas para essa turma no mês
  fetch(`/professor/chamadas_mes/${turmaSelecionadaId}/${ano}/${mes + 1}`)
    .then(r => r.json())
    .then(chamadas => {
      const datasFeitas = chamadas.map(c => c.data_aula);
      gerarCalendario(diasTurma, ano, mes, datasFeitas, hoje);
    });

  document.getElementById('card-selecao').classList.add('oculto');
  document.getElementById('card-calendario').classList.remove('oculto');
}

// ===== GERAR CALENDÁRIO =====
function gerarCalendario(diasTurma, ano, mes, datasFeitas, hoje) {
  const container = document.getElementById('calendario-dias');
  container.innerHTML = '';

  const diasNumericos = diasTurma.map(d => DIAS_SEMANA[d]);
  const totalDias     = new Date(ano, mes + 1, 0).getDate();
  const hojeStr       = formatarData(hoje);

  for (let d = 1; d <= totalDias; d++) {
    const data    = new Date(ano, mes, d);
    const diaSem  = data.getDay();
    if (!diasNumericos.includes(diaSem)) continue;

    const dataStr = formatarData(data);
    const feita   = datasFeitas.includes(dataStr);
    const ehHoje  = dataStr === hojeStr;
    const futuro  = data > hoje;

    const btn = document.createElement('button');
    btn.className = 'dia-chamada';
    btn.innerHTML = `
      <span class="dia-numero">${d}</span>
      <span class="dia-semana">${nomeDiaSemana(diaSem)}</span>
      <span class="dia-status">${feita ? '✅' : ehHoje ? '📋' : futuro ? '' : '⚠️'}</span>
    `;

    if (feita)   btn.classList.add('feita');
    if (ehHoje)  btn.classList.add('hoje');
    if (futuro)  btn.classList.add('futuro');
    if (!feita && !futuro) btn.classList.add('pendente');

    if (!futuro) {
      btn.onclick = () => abrirChamada(dataStr, d, feita);
    }

    container.appendChild(btn);
  }
}

// ===== ABRIR CHAMADA DO DIA =====
function abrirChamada(dataStr, dia, jaFeita) {
  dataSelecionada = dataStr;

  const [ano, mes, d] = dataStr.split('-');
  document.getElementById('chamada-data-label').textContent =
    `${d}/${mes}/${ano}${jaFeita ? ' — Editar chamada' : ' — Nova chamada'}`;

  fetch(`/professor/alunos_chamada/${turmaSelecionadaId}/${dataStr}`)
    .then(r => r.json())
    .then(alunos => {
      const lista = document.getElementById('lista-alunos');
      lista.innerHTML = '';
      statusAlunos    = {};

      alunos.forEach(a => {
        statusAlunos[a.id] = a.status || 'P';
        const isPresente   = statusAlunos[a.id] === 'P';

        lista.innerHTML += `
          <div class="card-chamada" id="card-${a.id}">
            <div class="chamada-aluno-info">
              ${a.foto ? `<img src="${a.foto}" class="aluno-avatar-foto"/>` : `<div class="aluno-avatar">${a.nome[0]}</div>`}
                    <div>
                <p class="aluno-nome">${a.nome}</p>
                <p class="aluno-faltas-mes">${a.faltas_mes} falta${a.faltas_mes !== 1 ? 's' : ''} no mês</p>
              </div>
            </div>
            <button class="btn-status ${isPresente ? 'presente' : 'falta'}"
                    id="btn-${a.id}" onclick="toggleStatus(${a.id})">
              <span class="status-icone">${isPresente ? '✅' : '❌'}</span>
              <span class="status-texto">${isPresente ? 'Presente' : 'Falta'}</span>
            </button>
          </div>`;
      });

      document.getElementById('card-calendario').classList.add('oculto');
      document.getElementById('card-chamada').classList.remove('oculto');
    });
}

// ===== TOGGLE STATUS =====
function toggleStatus(id) {
  const btn  = document.getElementById('btn-' + id);
  const card = document.getElementById('card-' + id);

  if (statusAlunos[id] === 'P') {
    statusAlunos[id] = 'F';
    btn.className = 'btn-status falta';
    btn.querySelector('.status-icone').textContent = '❌';
    btn.querySelector('.status-texto').textContent = 'Falta';
    card.classList.add('card-falta-ativo');
  } else {
    statusAlunos[id] = 'P';
    btn.className = 'btn-status presente';
    btn.querySelector('.status-icone').textContent = '✅';
    btn.querySelector('.status-texto').textContent = 'Presente';
    card.classList.remove('card-falta-ativo');
  }
}

// ===== SALVAR CHAMADA =====
function salvarChamada() {
  const msg = document.getElementById('msg-chamada');

  fetch('/professor/salvar_chamada', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      turma_id: turmaSelecionadaId,
      data:     dataSelecionada,
      status:   statusAlunos
    })
  })
  .then(r => r.json())
  .then(data => {
    msg.style.display = 'block';
    if (data.ok) {
      msg.style.background = '#dcfce7';
      msg.style.color      = '#16a34a';
      msg.textContent      = '✅ Chamada salva com sucesso!';
      setTimeout(() => voltarCalendario(), 1500);
    } else {
      msg.style.background = '#fee2e2';
      msg.style.color      = '#dc2626';
      msg.textContent      = 'Erro ao salvar chamada.';
    }
  });
}

// ===== NAVEGAÇÃO =====
function voltarSelecao() {
  document.getElementById('card-calendario').classList.add('oculto');
  document.getElementById('card-selecao').classList.remove('oculto');
}

function voltarCalendario() {
  document.getElementById('card-chamada').classList.add('oculto');
  document.getElementById('card-calendario').classList.remove('oculto');
  // Recarregar calendário para atualizar status
  abrirCalendario();
}

// ===== UTILITÁRIOS =====
function formatarData(data) {
  const ano = data.getFullYear();
  const mes = String(data.getMonth() + 1).padStart(2, '0');
  const dia = String(data.getDate()).padStart(2, '0');
  return `${ano}-${mes}-${dia}`;
}

function nomeDiaSemana(num) {
  return ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'][num];
}