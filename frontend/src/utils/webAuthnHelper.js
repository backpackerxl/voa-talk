// 工具函数：确保base64Url转换安全（兜底空值）
export function base64UrlToArrayBuffer(base64Url) {
    if (!base64Url) return new ArrayBuffer(0); // 空值兜底
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const padLength = (4 - (base64.length % 4)) % 4;
    const padded = base64.padEnd(base64.length + padLength, '=');
    const binary = atob(padded);
    const buffer = new ArrayBuffer(binary.length);
    const view = new Uint8Array(buffer);
    for (let i = 0; i < binary.length; i++) {
        view[i] = binary.charCodeAt(i);
    }
    return buffer;
}

// 工具函数：ArrayBuffer转Base64Url（兜底空值）
export function arrayBufferToBase64Url(buffer) {
    if (!buffer || buffer.byteLength === 0) return ''; // 空值兜底
    const binary = String.fromCharCode(...new Uint8Array(buffer));
    const base64 = btoa(binary);
    return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

