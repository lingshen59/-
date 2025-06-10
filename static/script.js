<script>
  // Bloquear clic derecho
  document.addEventListener('contextmenu', e => e.preventDefault());

  // Bloquear combinaciones de teclas comunes para abrir herramientas dev
  document.addEventListener('keydown', function(e) {
    if (
      e.key === 'F12' ||
      (e.ctrlKey && e.key.toLowerCase() === 'u') || // Ctrl+U
      (e.ctrlKey && e.shiftKey && ['i', 'j', 'c'].includes(e.key.toLowerCase()))
    ) {
      e.preventDefault();
    }
  });

  // Intentar detectar apertura de herramientas de desarrollador
  setInterval(() => {
    const before = new Date().getTime();
    debugger; // puede causar pausa si está abierto
    const after = new Date().getTime();
    if (after - before > 100) {
      window.close(); // opcional: cierra la pestaña
    }
  }, 1000);
</script>
