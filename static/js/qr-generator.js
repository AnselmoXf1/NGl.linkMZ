/*
 * qr-generator.js
 * Centralized QR generation utilities for NGL.MZ
 * - Loads QR library (primary CDN + fallback)
 * - Exposes window.generateQRCode, regenerateQR, downloadQRCode, copyQRCode
 * - Exposes window.generateCustomQR, regenerateCustomQR, downloadCustomQR
 */
(function () {
    'use strict';

    let currentQRCode = null;
    let profileLink = '';

    function loadScript(src, onload, onerror) {
        const s = document.createElement('script');
        s.src = src;
        s.async = true;
        s.onload = onload;
        s.onerror = onerror;
        document.head.appendChild(s);
    }

    function loadQRCodeLib(primary, fallback, cb) {
        if (typeof QRCode !== 'undefined') {
            return cb(null);
        }

        loadScript(primary, function () {
            // small delay to ensure global is set
            setTimeout(() => cb(null), 50);
        }, function () {
            // try fallback
            loadScript(fallback, function () {
                setTimeout(() => cb(null), 50);
            }, function () {
                cb(new Error('Failed to load QR library'));
            });
        });
    }

    // Utility to adjust color brightness
    function adjustColor(color, amount) {
        try {
            const num = parseInt(color.replace('#', ''), 16);
            const r = Math.max(0, Math.min(255, ((num >> 16) & 255) + amount));
            const g = Math.max(0, Math.min(255, ((num >> 8) & 255) + amount));
            const b = Math.max(0, Math.min(255, (num & 255) + amount));
            return '#' + ((r << 16) | (g << 8) | b).toString(16).padStart(6, '0');
        } catch (e) {
            return color;
        }
    }

    // Render QR supporting both APIs (qrcode and qrcodejs)
    function renderQRCode(container, text, size, color) {
        return new Promise((resolve, reject) => {
            container.innerHTML = '';

            // Try modern 'qrcode' library API: QRCode.toCanvas
            if (window.QRCode && typeof window.QRCode.toCanvas === 'function') {
                const canvas = document.createElement('canvas');
                container.appendChild(canvas);
                try {
                    // Options: dark/light nested object
                    const opts = { width: size, margin: 1, color: { dark: color, light: '#ffffff' } };
                    // library may accept callback or return Promise
                    const result = window.QRCode.toCanvas(canvas, text, opts, function (err) {
                        if (err) return reject(err);
                        canvas.style.borderRadius = '10px';
                        canvas.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
                        currentQRCode = canvas;
                        resolve(canvas);
                    });

                    // If it returned a Promise
                    if (result && typeof result.then === 'function') {
                        result.then(() => {
                            canvas.style.borderRadius = '10px';
                            canvas.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
                            currentQRCode = canvas;
                            resolve(canvas);
                        }).catch(reject);
                    }
                } catch (e) {
                    reject(e);
                }

                return;
            }

            // Try qrcodejs style constructor: new QRCode(container, options)
            if (typeof window.QRCode === 'function' || typeof window.QRCode === 'object') {
                try {
                    // Some builds expect 'new QRCode(element, options)'
                    const opts = {
                        text: text,
                        width: size,
                        height: size,
                        colorDark: color,
                        colorLight: '#ffffff',
                        correctLevel: window.QRCode && window.QRCode.CorrectLevel ? window.QRCode.CorrectLevel.H : undefined
                    };

                    // Constructor can throw; wrap
                    try {
                        /* eslint-disable no-new */
                        new window.QRCode(container, opts);
                        /* eslint-enable no-new */
                    } catch (ctorErr) {
                        // Some variants expect QRCode(element) then makeCode
                        if (container.QRCode) {
                            try { container.QRCode.makeCode(text); }
                            catch (e) { /* ignore */ }
                        }
                    }

                    // qrcodejs usually creates an <img> or <canvas>
                    setTimeout(() => {
                        const canvas = container.querySelector('canvas');
                        const img = container.querySelector('img');
                        const node = canvas || img;
                        if (node) {
                            node.style.borderRadius = '10px';
                            node.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
                            currentQRCode = node;
                            resolve(node);
                        } else {
                            reject(new Error('QR node not found after generation'));
                        }
                    }, 30);
                    return;
                } catch (e) {
                    return reject(e);
                }
            }

            reject(new Error('No supported QRCode API available'));
        });
    }

    // Exposed functions
    function generateQRCode() {
        const sizeEl = document.getElementById('qrSize');
        const colorEl = document.getElementById('qrColor');
        const qrContainer = document.getElementById('qrcode');

        if (!qrContainer) return;

        const size = parseInt(sizeEl ? sizeEl.value : (200), 10) || 200;
        const color = colorEl ? colorEl.value : '#000000';

        // Show loading
        qrContainer.innerHTML = '<div class="text-center mb-3"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Carregando...</span></div></div>';

        renderQRCode(qrContainer, profileLink || (document.getElementById('profileLink') && document.getElementById('profileLink').value) || '', size, color)
            .catch(err => {
                console.error('Erro ao gerar QR Code:', err);
                qrContainer.innerHTML = '<p class="text-danger"><i class="fas fa-exclamation-circle"></i> Erro ao gerar QR Code. Tente novamente.</p>';
                currentQRCode = null;
            });
    }

    function regenerateQR() { generateQRCode(); }

    function downloadQRCode() {
        if (!currentQRCode) {
            alert('QR Code não foi gerado ainda!');
            return;
        }

        if (currentQRCode.tagName === 'CANVAS') {
            const link = document.createElement('a');
            link.download = `ngl-qrcode.png`;
            link.href = currentQRCode.toDataURL();
            link.click();
            return;
        }

        if (currentQRCode.tagName === 'IMG') {
            const link = document.createElement('a');
            link.download = `ngl-qrcode.png`;
            link.href = currentQRCode.src;
            link.click();
            return;
        }

        alert('Formato de QR Code desconhecido para download');
    }

    function copyQRCode() {
        const linkInput = document.getElementById('profileLink');
        if (!linkInput) return;
        linkInput.select();
        document.execCommand('copy');
    }

    // Custom QR generation (with background/styles) and download
    function generateCustomQR() {
        const size = parseInt(document.getElementById('customQrSize')?.value || 400, 10);
        const style = document.getElementById('customQrStyle')?.value || 'gradient';
        const color = document.getElementById('qrColor')?.value || '#000000';
        const container = document.getElementById('customQRPreview');
        if (!container) return;

        container.innerHTML = '';
        const tempDiv = document.createElement('div');
        tempDiv.style.cssText = `width:${size}px;height:${size}px;position:relative;display:flex;align-items:center;justify-content:center;`;

        let backgroundStyle = '';
        switch (style) {
            case 'gradient':
                backgroundStyle = `background: linear-gradient(135deg, ${color} 0%, ${adjustColor(color, -30)} 100%);`;
                break;
            case 'solid':
                backgroundStyle = `background: ${color};`;
                break;
            case 'pattern':
                backgroundStyle = `background: ${color}; background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="white" opacity="0.1"/><circle cx="80" cy="80" r="2" fill="white" opacity="0.1"/></svg>'); background-size: 30px 30px;`;
                break;
        }

        tempDiv.innerHTML = `<div style="${backgroundStyle} width:100%; height:100%; border-radius:20px; position:relative; overflow:hidden;"><div id=\"qrCodeContainer\" style=\"position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:white;padding:20px;border-radius:15px;box-shadow:0 8px 32px rgba(0,0,0,0.1);\"></div></div>`;

        container.appendChild(tempDiv);

        const qrTarget = tempDiv.querySelector('#qrCodeContainer');

        renderQRCode(qrTarget, profileLink || (document.getElementById('profileLink') && document.getElementById('profileLink').value) || '', Math.floor(size * 0.6), '#000000')
            .then(() => {
                window.customQRCode = tempDiv; // store for download
            }).catch(err => {
                console.error('Erro ao gerar QR Code personalizado:', err);
                container.innerHTML = '<p class="text-danger">Erro ao gerar QR Code personalizado</p>';
            });
    }

    function regenerateCustomQR() { generateCustomQR(); }

    function downloadCustomQR() {
        if (!window.customQRCode) {
            alert('QR Code personalizado não foi gerado ainda!');
            return;
        }

        if (typeof html2canvas === 'undefined') {
            alert('html2canvas não carregado. Impossível baixar QR personalizado.');
            return;
        }

        html2canvas(window.customQRCode, { scale: 2, useCORS: true, backgroundColor: null }).then(canvas => {
            const link = document.createElement('a');
            link.download = `ngl-qrcode-custom.png`;
            link.href = canvas.toDataURL();
            link.click();
        }).catch(err => {
            console.error('Erro ao baixar QR Code personalizado:', err);
            alert('Erro ao baixar QR Code personalizado');
        });
    }

    // --- Social image composition (embed QR into a share-ready image) ---
    // presets: facebook (1200x630), instagram (1080x1080), telegram (800x800)
    function getPresetSize(preset) {
        switch ((preset || '').toLowerCase()) {
            case 'facebook': return { width: 1200, height: 630 };
            case 'telegram': return { width: 800, height: 800 };
            case 'instagram':
            default: return { width: 1080, height: 1080 };
        }
    }

    function nodeToCanvas(node) {
        return new Promise((resolve, reject) => {
            if (!node) return reject(new Error('No node provided'));

            // If it's already a canvas
            if (node.tagName === 'CANVAS') return resolve(node);

            // If it's an image element
            if (node.tagName === 'IMG') {
                const img = new Image();
                // preserve cross-origin if available
                img.crossOrigin = 'anonymous';
                img.onload = function () {
                    const c = document.createElement('canvas');
                    c.width = img.naturalWidth || img.width;
                    c.height = img.naturalHeight || img.height;
                    const ctx = c.getContext('2d');
                    ctx.drawImage(img, 0, 0);
                    resolve(c);
                };
                img.onerror = function (e) { reject(new Error('Failed to load image node')); };
                img.src = node.src;
                return;
            }

            // For arbitrary HTML elements (like our custom preview), use html2canvas if available
            if (typeof html2canvas !== 'undefined') {
                html2canvas(node, { scale: 2, useCORS: true, backgroundColor: null }).then(canvas => resolve(canvas)).catch(reject);
                return;
            }

            reject(new Error('Cannot convert node to canvas (no html2canvas and node is not img/canvas)'));
        });
    }

    async function composeSocialImage(options) {
        // options: { preset, width, height, backgroundUrl, backgroundNode, qrNode, qrSizePct, qrPosition }
        const preset = options.preset || 'instagram';
        const presetSize = getPresetSize(preset);
        const width = options.width || presetSize.width;
        const height = options.height || presetSize.height;
        const bgUrl = options.backgroundUrl || null;
        const bgNode = options.backgroundNode || document.getElementById('shareBackground') || null;
        const qrNode = options.qrNode || currentQRCode || window.customQRCode || document.getElementById('qrcode');
        const qrSizePct = typeof options.qrSizePct === 'number' ? options.qrSizePct : 0.25; // fraction of shorter side
        const qrPosition = options.qrPosition || 'bottom-right';

        // Create canvas
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        // Draw background: priority - bgNode (img) -> bgUrl -> solid color
        try {
            if (bgNode && bgNode.tagName === 'IMG' && bgNode.src) {
                const img = new Image();
                img.crossOrigin = 'anonymous';
                await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = bgNode.src; });
                // cover-style draw
                const ar = img.width / img.height;
                const tarAr = width / height;
                let sx = 0, sy = 0, sw = img.width, sh = img.height;
                if (ar > tarAr) {
                    // image wider, crop sides
                    sw = Math.round(img.height * tarAr);
                    sx = Math.round((img.width - sw) / 2);
                } else {
                    // image taller, crop top/bottom
                    sh = Math.round(img.width / tarAr);
                    sy = Math.round((img.height - sh) / 2);
                }
                ctx.drawImage(img, sx, sy, sw, sh, 0, 0, width, height);
            } else if (bgUrl) {
                const img = new Image();
                img.crossOrigin = 'anonymous';
                await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = bgUrl; });
                ctx.drawImage(img, 0, 0, width, height);
            } else {
                // default neutral background
                ctx.fillStyle = options.backgroundColor || '#ffffff';
                ctx.fillRect(0, 0, width, height);
            }
        } catch (e) {
            console.warn('Background draw failed, using solid background', e);
            ctx.fillStyle = options.backgroundColor || '#ffffff';
            ctx.fillRect(0, 0, width, height);
        }

        // Prepare QR canvas
        let qrCanvas = null;
        try {
            // if qrNode is our stored custom wrapper (div) it might be window.customQRCode
            if (qrNode && qrNode.nodeType && (qrNode.tagName === 'CANVAS' || qrNode.tagName === 'IMG')) {
                qrCanvas = await nodeToCanvas(qrNode);
            } else if (qrNode && qrNode.nodeType) {
                qrCanvas = await nodeToCanvas(qrNode);
            } else if (window.customQRCode) {
                qrCanvas = await nodeToCanvas(window.customQRCode);
            } else if (currentQRCode) {
                qrCanvas = await nodeToCanvas(currentQRCode);
            }
        } catch (e) {
            console.warn('Failed to obtain QR canvas:', e);
            qrCanvas = null;
        }

        if (qrCanvas) {
            // compute target size
            const short = Math.min(width, height);
            const targetSize = Math.round(short * qrSizePct);
            let dx = 0, dy = 0;
            switch (qrPosition) {
                case 'top-left': dx = Math.round(short * 0.05); dy = Math.round(short * 0.05); break;
                case 'top-right': dx = width - targetSize - Math.round(short * 0.05); dy = Math.round(short * 0.05); break;
                case 'bottom-left': dx = Math.round(short * 0.05); dy = height - targetSize - Math.round(short * 0.05); break;
                case 'center': dx = Math.round((width - targetSize) / 2); dy = Math.round((height - targetSize) / 2); break;
                case 'bottom-right':
                default:
                    dx = width - targetSize - Math.round(short * 0.05);
                    dy = height - targetSize - Math.round(short * 0.05);
                    break;
            }

            // draw white rounded card behind QR for contrast
            const padding = Math.round(targetSize * 0.06);
            const cardW = targetSize + padding * 2;
            const cardH = targetSize + padding * 2;
            const cardX = dx - padding;
            const cardY = dy - padding;

            // rounded rectangle
            const r = Math.round(cardW * 0.08);
            ctx.fillStyle = 'rgba(255,255,255,0.95)';
            ctx.beginPath();
            ctx.moveTo(cardX + r, cardY);
            ctx.lineTo(cardX + cardW - r, cardY);
            ctx.quadraticCurveTo(cardX + cardW, cardY, cardX + cardW, cardY + r);
            ctx.lineTo(cardX + cardW, cardY + cardH - r);
            ctx.quadraticCurveTo(cardX + cardW, cardY + cardH, cardX + cardW - r, cardY + cardH);
            ctx.lineTo(cardX + r, cardY + cardH);
            ctx.quadraticCurveTo(cardX, cardY + cardH, cardX, cardY + cardH - r);
            ctx.lineTo(cardX, cardY + r);
            ctx.quadraticCurveTo(cardX, cardY, cardX + r, cardY);
            ctx.closePath();
            ctx.fill();

            // draw QR scaled using nearest-neighbor (disable smoothing) to keep modules crisp
            try {
                // disable smoothing for pixel-perfect QR
                if (typeof ctx.imageSmoothingEnabled !== 'undefined') ctx.imageSmoothingEnabled = false;
                ctx.drawImage(qrCanvas, 0, 0, qrCanvas.width, qrCanvas.height, dx, dy, targetSize, targetSize);
            } finally {
                // restore smoothing
                if (typeof ctx.imageSmoothingEnabled !== 'undefined') ctx.imageSmoothingEnabled = true;
            }
        }

        return canvas;
    }

    async function generateSocialImage(preset) {
        try {
            const bgInput = document.getElementById('shareBackgroundUrl');
            const bgUrl = bgInput ? bgInput.value : null;
            const canvas = await composeSocialImage({ preset: preset || 'instagram', backgroundUrl: bgUrl, qrSizePct: 0.28, qrPosition: 'bottom-right' });
            // show preview if element exists
            const preview = document.getElementById('shareImagePreview');
            if (preview) {
                preview.innerHTML = '';
                const img = new Image(); img.src = canvas.toDataURL(); img.style.maxWidth = '100%'; preview.appendChild(img);
            }
            // store last composed canvas
            window.lastSocialCanvas = canvas;
            return canvas;
        } catch (e) {
            console.error('Erro ao compor imagem social:', e);
            alert('Erro ao gerar imagem de compartilhamento. Verifique o console.');
            throw e;
        }
    }

    function downloadSocialImage(filename) {
        const canvas = window.lastSocialCanvas;
        if (!canvas) {
            alert('Nenhuma imagem composta disponível. Gere a imagem primeiro.');
            return;
        }
        const link = document.createElement('a');
        link.download = filename || 'ngl-share-image.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    }


    // Initialization: load QR lib then wire events
    function init() {
        profileLink = document.getElementById('profileLink') ? document.getElementById('profileLink').value : profileLink;

        loadQRCodeLib('https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js', 'https://unpkg.com/qrcodejs@1.0.0/qrcode.min.js', function (err) {
            if (err) {
                const q = document.getElementById('qrcode');
                if (q) q.innerHTML = '<p class="text-danger"><i class="fas fa-exclamation-circle"></i> Erro: Falha ao carregar biblioteca QR Code. Verifique sua conexão.</p>';
                console.error(err);
                return;
            }

            // Attach events
            const sizeEl = document.getElementById('qrSize');
            const colorEl = document.getElementById('qrColor');
            if (sizeEl) sizeEl.addEventListener('change', generateQRCode);
            if (colorEl) colorEl.addEventListener('change', generateQRCode);

            // Generate initial QR
            try { generateQRCode(); } catch (e) { console.error(e); }
        });
    }

    // expose to window
    window.generateQRCode = generateQRCode;
    window.regenerateQR = regenerateQR;
    window.downloadQRCode = downloadQRCode;
    window.copyQRCode = copyQRCode;
    window.generateCustomQR = generateCustomQR;
    window.regenerateCustomQR = regenerateCustomQR;
    window.downloadCustomQR = downloadCustomQR;
    window.loadQRCodeLib = loadQRCodeLib;
    window.QRGenerator = { init: init, renderQRCode: renderQRCode };
    // expose social helpers
    window.QRGenerator.composeSocialImage = composeSocialImage;
    window.QRGenerator.generateSocialImage = generateSocialImage;
    window.QRGenerator.downloadSocialImage = downloadSocialImage;

    // Auto-init on DOMContentLoaded
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        setTimeout(init, 50);
    } else {
        document.addEventListener('DOMContentLoaded', init);
    }

})();
