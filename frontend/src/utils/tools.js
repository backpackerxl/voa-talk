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

/**
 * 让滚动条以"前慢中快后慢"的效果移动（自动计算时间）
 * @param el 操作节点
 * @param targetY 目标点的高度
 */
export function smoothScroll(el, targetY, func = null) {
    const start = el.scrollTop;
    const distance = targetY - start;

    // 根据滚动距离自动计算持续时间（距离越大，时间越长）
    // 这里的系数可以根据需要调整，控制整体速度
    const duration = Math.min(Math.max(Math.abs(distance) * 0.5, 300), 2000); // 最小300ms，最大2000ms

    const startTime = performance.now();

    // 自定义缓动函数 - 前慢中快后慢
    function easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    }

    function animateScroll(currentTime) {
        const elapsedTime = currentTime - startTime;
        const progress = Math.min(elapsedTime / duration, 1);
        const easedProgress = easeInOutQuad(progress);

        el.scrollTo(0, start + distance * easedProgress);

        if (progress < 1) {
            requestAnimationFrame(animateScroll);
        } else {
            if (func && func instanceof Function) {
                func();
            }
        }
    }

    requestAnimationFrame(animateScroll);
}
