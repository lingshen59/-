<script>
  // Bloquear clic derecho
  document.addEventListener('contextmenu', event => event.preventDefault());

  // Bloquear teclas como F12, Ctrl+Shift+I, Ctrl+U
  document.addEventListener('keydown', function(e) {
    if (
      e.key === "F12" ||
      (e.ctrlKey && e.shiftKey && ["I", "C", "J"].includes(e.key)) ||
      (e.ctrlKey && e.key === "U")
    ) {
      e.preventDefault();
    }
  });
</script>
