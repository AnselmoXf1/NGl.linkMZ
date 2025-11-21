// Script para instalar PWA
let deferredPrompt;
const installButton = document.getElementById('installPWA');
const installBanner = document.getElementById('installBanner');

// Esconde o botão inicialmente
if (installButton) {
    installButton.style.display = 'none';
}
if (installBanner) {
    installBanner.style.display = 'none';
}

// Registra o service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/service-worker.js')
            .then(registration => {
                console.log('ServiceWorker registrado com sucesso:', registration.scope);
            })
            .catch(error => {
                console.log('Falha ao registrar ServiceWorker:', error);
            });
    });
}

// Captura evento beforeinstallprompt
window.addEventListener('beforeinstallprompt', (e) => {
    // Previne Chrome 67+ de mostrar prompt automático
    e.preventDefault();
    // Guarda evento para usar depois
    deferredPrompt = e;
    
    // Verifica se é dispositivo móvel
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        // Mostra banner personalizado
        if (installBanner) {
            installBanner.style.display = 'block';
        }
    }
    
    // Mostra botão de instalação
    if (installButton) {
        installButton.style.display = 'block';
        
        installButton.addEventListener('click', installPWA);
    }
});

// Função para instalar PWA
function installPWA(e) {
    if (installBanner) {
        installBanner.style.display = 'none';
    }
    
    if (deferredPrompt) {
        // Mostra prompt de instalação
        deferredPrompt.prompt();
        
        // Espera usuário responder ao prompt
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('Usuário aceitou instalação do PWA');
                // Esconde botão/banner após instalação
                if (installButton) {
                    installButton.style.display = 'none';
                }
            }
            // Limpa prompt guardado
            deferredPrompt = null;
        });
    }
}

// Detecta se PWA já está instalado
window.addEventListener('appinstalled', (evt) => {
    console.log('PWA instalado com sucesso');
    // Esconde botão/banner após instalação
    if (installButton) {
        installButton.style.display = 'none';
    }
    if (installBanner) {
        installBanner.style.display = 'none';
    }
});