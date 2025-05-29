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

export function hexToRGB(hex, alpha = 1) {
    const [r, g, b] = hex.match(/\w\w/g).map(x => parseInt(x, 16));
    return `rgb(${r}, ${g}, ${b}, ${alpha})`;
};

// 用法 import { hexToRGB } from "@/utils/tools";
// const sysThemColor = {
//   "--el-color-primary": `${hexToRGB(item.bgColor)} !important`,
//   "--el-color-primary-light-3": `${hexToRGB(item.bgColor, 0.7)} !important`,
//   "--el-color-primary-light-5": `${hexToRGB(item.bgColor, 0.5)} !important`,
//   "--el-color-primary-light-7": `${hexToRGB(item.bgColor, 0.3)} !important`,
//   "--el-color-primary-light-8": `${hexToRGB(item.bgColor, 0.2)} !important`,
//   "--el-color-primary-light-9": `${hexToRGB(item.bgColor, 0.1)} !important`,
//   "--el-color-primary-dark-2": `${hexToRGB(item.bgColor)} !important`,
// };
// let str = "";
// for (const [key, value] of Object.entries(sysThemColor)) {
//   str += `${key}: ${value};\n`;
//   // document.documentElement.classList.add().style.setProperty(key, value);
// }
// console.log(str);

export function formatDateTime(date) {
    // 如果传入的是时间戳或字符串，先转换为 Date 对象
    if (typeof date === 'number' || typeof date === 'string') {
        date = new Date(date);
    }

    // 获取年、月、日
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');

    // 返回格式化后的字符串
    return `${year}-${month}-${day}`;
}

const match = matchMedia("(prefers-color-scheme: dark)");

function followOS() {
    document.documentElement.classList.remove("light", "dark");
    document.documentElement.classList.add(match.matches ? "dark" : "light");
}

export function handleThem(item) {
    document.documentElement.classList.remove("light", "dark");
    if (item.them === "os") {
        followOS();
        document.documentElement.classList.add(match.matches ? "dark" : "light");
        match.addEventListener("change", followOS);
    } else {
        document.documentElement.classList.add(item.them);
        match.removeEventListener("change", followOS);
    }
}
