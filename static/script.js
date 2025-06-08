document.addEventListener('contextmenu', event => event.preventDefault());
document.onkeydown = function(e) {
    if (e.keyCode == 123 || 
        (e.ctrlKey && e.shiftKey && ['I','C','J'].includes(e.key.toUpperCase())) || 
        (e.ctrlKey && e.key === 'u')) {
        return false;
    }
};