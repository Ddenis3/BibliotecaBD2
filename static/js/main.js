(() => {
  const menu = document.getElementById('mobileMenu');
  const sidebar = document.getElementById('appSidebar');
  const scrim = document.getElementById('sidebarScrim');
  const close = () => {sidebar?.classList.remove('is-open');scrim?.classList.remove('is-open');};
  menu?.addEventListener('click', () => {sidebar?.classList.toggle('is-open');scrim?.classList.toggle('is-open');});
  scrim?.addEventListener('click', close);
  document.addEventListener('keydown', e => {if(e.key === 'Escape') close();});
  const password = document.getElementById('parola');
  const toggle = document.getElementById('togglePassword');
  toggle?.addEventListener('click', () => {if(!password) return; password.type = password.type === 'password' ? 'text' : 'password';toggle.setAttribute('aria-label',password.type === 'password'?'Arata parola':'Ascunde parola');});
})();
