// cadastro_aluno.js — Máscaras e validações do cadastro de aluno
// Alfa Profissionalizantes

// ===== MÁSCARAS =====

function mascaraCPF(input) {
  let v = input.value.replace(/\D/g, '').slice(0, 11);
  v = v.replace(/(\d{3})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  input.value = v;
}

function mascaraRG(input) {
  let v = input.value.replace(/\D/g, '').slice(0, 9);
  v = v.replace(/(\d{2})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  input.value = v;
}

function mascaraTelefone(input) {
  let v = input.value.replace(/\D/g, '').slice(0, 11);
  if (v.length <= 10) {
    v = v.replace(/(\d{2})(\d)/, '($1) $2');
    v = v.replace(/(\d{4})(\d)/, '$1-$2');
  } else {
    v = v.replace(/(\d{2})(\d)/, '($1) $2');
    v = v.replace(/(\d{5})(\d)/, '$1-$2');
  }
  input.value = v;
}

// ===== VALIDAÇÕES =====

function apenasLetras(input) {
  input.value = input.value.replace(/[0-9]/g, '');
}

function validarDataNascimento(input) {
  const hoje = new Date();
  const data  = new Date(input.value);
  if (data > hoje) {
    input.setCustomValidity('A data de nascimento não pode ser no futuro.');
    input.reportValidity();
    input.value = '';
  } else {
    input.setCustomValidity('');
  }
}

// ===== APLICAR AO CARREGAR =====
document.addEventListener('DOMContentLoaded', function () {

  // CPF
  const cpf = document.getElementById('input-cpf');
  if (cpf) cpf.addEventListener('input', () => mascaraCPF(cpf));

  // RG
  const rg = document.getElementById('input-rg');
  if (rg) rg.addEventListener('input', () => mascaraRG(rg));

  // Telefone
  const tel = document.getElementById('input-telefone');
  if (tel) tel.addEventListener('input', () => mascaraTelefone(tel));

  // Nomes (apenas letras)
  ['input-nome-responsavel', 'input-nome-aluno'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', () => apenasLetras(el));
  });

  // Datas de nascimento
  ['input-nasc-responsavel', 'input-nasc-aluno'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      // Bloquear datas futuras no atributo max
      el.max = new Date().toISOString().split('T')[0];
      el.addEventListener('change', () => validarDataNascimento(el));
    }
  });

});