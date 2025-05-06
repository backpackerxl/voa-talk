import CryptoJS from "crypto-js";

export function encryptAes(pwd) {
    // 对密码进行加密处理
    const key = CryptoJS.enc.Utf8.parse("hnciquewhngfo1qc"); // 用于 AES 加密的密钥
    const iv = CryptoJS.enc.Utf8.parse("\x00".repeat(16)); // IV

    // 使用CryptoJS库的填充方式进行填充
    let encrypted = CryptoJS.AES.encrypt(pwd, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.ZeroPadding, // 使用零填充
    });
    return encrypted.toString(); // 获取 base64 编码的密文
}

export function getGreeting() {
    const now = new Date();
    const hour = now.getHours();

    if (hour >= 5 && hour < 12) {
        return '早上好';
    } else if (hour >= 12 && hour < 18) {
        return '下午好';
    } else {
        return '晚上好';
    }
}
