// 确保AiEditor全局可用
(function() {
    if (typeof window.AiEditor === 'undefined' && typeof require === 'function') {
        try {
            window.AiEditor = require('aieditor').AiEditor;
        } catch (e) {
            console.error('Failed to load AiEditor:', e);
        }
    }
})(); 