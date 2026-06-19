// sidebar.js — Alfa Profissionalizantes

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('overlay');
  sidebar.classList.toggle('aberta');
  overlay.classList.toggle('visivel');
}