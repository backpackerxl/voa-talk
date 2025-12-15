// ArrayBuffer 转 Base64URL
export function arrayBufferToBase64Url(buffer) {
    const bytes = new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    // 转换为 Base64，然后替换字符以符合 Base64URL 标准
    return btoa(binary)
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
}

// Base64URL 转 ArrayBuffer
export function base64UrlToArrayBuffer(base64Url) {
    // 将 Base64URL 转换为标准 Base64
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');

    // 添加 padding（=）
    const pad = base64.length % 4;
    if (pad) {
        if (pad === 1) {
            throw new Error('Invalid Base64URL string');
        }
        base64 += '==='.slice(0, 4 - pad);
    }

    // 解码为二进制字符串
    const binary = atob(base64);

    // 转换为 ArrayBuffer
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
    }

    return bytes.buffer;
}

// 验证字符串是否为有效的 Base64URL
export function isValidBase64Url(str) {
    try {
        // 尝试转换来验证
        this.base64UrlToArrayBuffer(str);
        return /^[A-Za-z0-9\-_]+$/.test(str);
    } catch (e) {
        return false;
    }
}

// 获取服务器基础 URL
export function getServerUrl() {
    // 自动检测协议和端口
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    const port = window.location.port ? `:${window.location.port}` : '';
    return `${protocol}//${hostname}${port}`;
}
