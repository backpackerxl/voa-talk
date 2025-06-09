import renderMathInElement from "katex/dist/contrib/auto-render";
import { marked } from "marked";
import DOMPurify from "dompurify";
import hljs from "highlight.js";
import html from 'highlight.js/lib/languages/xml';
import javascript from 'highlight.js/lib/languages/javascript';
import css from 'highlight.js/lib/languages/css';
import * as clipboard from "clipboard-polyfill";
import { ElMessage } from "element-plus";
import device from "current-device";
import mermaid from 'mermaid';

// 配置 Mermaid
mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',
    theme: 'default',
});

// 注册语言
hljs.registerLanguage('html', html);
hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('css', css);

// 自定义 Vue 语法处理
hljs.registerLanguage('vue', (hljs) => {
    return {
        subLanguage: 'html',
        contains: [
            {
                begin: /<script\b/,
                end: /<\/script>/,
                subLanguage: 'javascript',
                contains: [
                    hljs.inherit(hljs.APOS_STRING_MODE, { className: 'string' }),
                    hljs.inherit(hljs.QUOTE_STRING_MODE, { className: 'string' })
                ]
            },
            {
                begin: /<style\b/,
                end: /<\/style>/,
                subLanguage: 'css'
            }
        ]
    };
});

marked.setOptions({
    highlight: function (code, language) {
        const validLanguage = hljs.getLanguage(language) ? language : "plaintext";
        return hljs.highlight(code, { language: validLanguage }).value;
    },
});

// 添加复制图标的方法
export function markdwonToHTML(content, showPlayIcon) {
    const oDiv = document.createElement("div");
    oDiv.innerHTML = DOMPurify.sanitize(marked.parse(content));
    renderMathInElement(oDiv, {
        delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\(", right: "\\)", display: false },
            { left: "\\[", right: "\\]", display: true },
        ],
    });
    oDiv.querySelectorAll("pre code").forEach((block) => {
        // 处理流程图
        const ismermaid = block.classList.contains('language-mermaid');
        if (ismermaid) {
            block.innerHTML = `<div data-scale="1" data-posX="0" data-posY="0" class="mermaid">${block.innerText}</div>`;
            block.dataset.code = block.innerText;
        } else {
            hljs.highlightElement(block);
        }
        // 确保每个代码块只有一个图标
        if (!block.parentNode.querySelector(".copy-icon")) {
            const oDivC = document.createElement("div");
            const oDivH = document.createElement("div");
            const oDivTools = document.createElement("div");
            const oButton = document.createElement("button");

            oButton.innerText = block.classList[0].split('-')[1] || 'code';

            const copyIcon = document.createElement("i");
            const upIcon = document.createElement("i");
            oDivC.className = 'pre-container'
            oDivH.className = 'pre-header'
            oDivTools.className = 'pre-header-tools'
            oButton.className = 'pre-button';
            if (ismermaid) {
                const code = document.createElement("i")
                code.className = "mermaid-show-code fa-solid fa-code";
                const scaleBig = document.createElement("i");
                scaleBig.className = "mermaid-scale-big fa-solid fa-magnifying-glass-plus";
                const scaleSmall = document.createElement("i");
                scaleSmall.className = "mermaid-scale-small fa-solid fa-magnifying-glass-minus";
                const resetChart = document.createElement("i");
                resetChart.className = "mermaid-reset-chart fa-solid fa-expand";
                oDivTools.appendChild(code);
                oDivTools.appendChild(scaleBig);
                oDivTools.appendChild(scaleSmall);
                oDivTools.appendChild(resetChart);
                oDivTools.dataset.scode = '0';
                copyIcon.style.display = "none";
            }
            copyIcon.className = "copy-icon fa-solid fa-copy"; // Font Awesome 复制图标
            upIcon.className = "prebtn-arrow fas fa-angle-up"; // Font Awesome 复制图标
            oDivTools.appendChild(copyIcon);
            if (oButton.innerText === "html" && !device.mobile() && showPlayIcon) {
                const playIcon = document.createElement("i");
                playIcon.className = "play-icon fa-regular fa-circle-play"; // 播放图标
                oDivTools.appendChild(playIcon);
            }

            oButton.appendChild(upIcon);

            // 将图标插入到 <pre> 元素中
            oDivH.appendChild(oButton);
            oDivH.appendChild(oDivTools);
            oDivC.appendChild(oDivH);
            let preBefore = block.parentNode.previousElementSibling;
            oDivC.appendChild(block.parentNode);
            preBefore.after(oDivC);

        }
    });

    return oDiv.innerHTML;
};

export async function renderMermaid() {
    await mermaid.run({
        nodes: document.querySelectorAll('.mermaid'),
    });
    setupZoomAndDrag();
}

export function addCopy(chatPage) {
    chatPage.addEventListener("click", function (e) {
        const el = e.target;
        if (el.tagName == "I" && el.classList.contains("copy-icon")) {
            clipboard.writeText(el.parentElement.parentElement.nextElementSibling.innerText).then(
                () => {
                    el.className = "copy-icon fas fa-check"; // 切换为成功图标
                    el.style.color = "#28a745"; // 成功颜色
                    ElMessage.success("复制成功");

                    setTimeout(() => {
                        el.className = "copy-icon fa-solid fa-copy";
                        el.style.color = "rgb(121, 122, 123)"; // 恢复原样
                    }, 2000); // 2 秒后恢复原样
                },
                () => { ElMessage.error("复制失败"); console.error("无法复制代码:", err); }
            );
        }

        if (el.tagName == "I" && el.classList.contains("play-icon")) {
            const oAside = chatPage.parentElement.parentElement.previousElementSibling;
            const oMain = chatPage.parentElement.parentElement.parentElement;
            const code = el.parentElement.parentElement.nextElementSibling.innerText;
            const oCC = oMain.querySelector("#me-code-container");
            let ifr = document.createElement('iframe');
            if (oCC) {
                ifr = oCC.querySelector("iframe");
                ifr.srcdoc = code;
                return;
            }
            const oDivC = document.createElement("div");
            const oDivH = document.createElement("div");
            const oI = document.createElement("i");
            oI.className = "fa-solid fa-xmark";
            oDivC.className = "code-container";
            oDivC.id = "me-code-container";
            oDivH.className = "code-container-header";
            oDivH.appendChild(oI);
            ifr.className = 'code-play';
            ifr.srcdoc = code;
            oDivC.appendChild(oDivH);
            oDivC.appendChild(ifr);
            oAside.classList.add("code-play");
            oMain.appendChild(oDivC);

            oI.addEventListener('click', function () {
                oAside.classList.remove("code-play");
                oDivC.remove();
            });
        }

        if (el.tagName == "I" && el.classList.contains("prebtn-arrow")) {
            const oP = el.parentElement.parentElement;
            if (el.classList.contains('fa-angle-up')) {
                el.classList.remove('fa-angle-up');
                el.classList.add('fa-angle-down');
                oP.parentElement.style.width = el.parentElement.getBoundingClientRect().width + 20 + 'px';
                oP.parentElement.style.height = '32px';
                oP.parentElement.style.overflow = 'hidden';
                oP.querySelector('.pre-header-tools').style.display = 'none';
            } else {
                el.classList.remove('fa-angle-down');
                el.classList.add('fa-angle-up');
                oP.parentElement.style.width = '';
                oP.parentElement.style.overflow = '';
                oP.parentElement.style.height = '';
                oP.querySelector('.pre-header-tools').style.display = '';
            }
        }

        if (el.tagName == "I" && el.classList.contains("mermaid-show-code")) {
            const oP = el.parentElement.parentElement;
            changeTools(oP);
        }

        if (el.tagName == "I" && el.classList.contains("mermaid-scale-big")) {
            const oP = el.parentElement.parentElement;
            const MC = oP.nextElementSibling.querySelector('div.mermaid');
            let st = MC.dataset.scale * 1.2;
            MC.dataset.scale = st > 10 ? 10 : st;
            updateTransform(MC);
            if (st > 10) {
                ElMessage.warning("不能再放大了！");
            }
        }

        if (el.tagName == "I" && el.classList.contains("mermaid-scale-small")) {
            const oP = el.parentElement.parentElement;
            const MC = oP.nextElementSibling.querySelector('div.mermaid');
            let st = MC.dataset.scale * 0.8;
            MC.dataset.scale = st < 0.3 ? 0.3 : st;
            updateTransform(MC);
            if (st < 0.3) {
                ElMessage.warning("不能再缩小了！");
            }
        }

        if (el.tagName == "I" && el.classList.contains("mermaid-reset-chart")) {
            const oP = el.parentElement.parentElement;
            const MC = oP.nextElementSibling.querySelector('div.mermaid');
            MC.dataset.scale = 1;
            MC.dataset.posx = 0;
            MC.dataset.posy = 0;
            updateTransform(MC);
            ElMessage.success("已重置！");
        }

        if (el.tagName == "I" && el.classList.contains("mermaid-down-png")) {
            const oP = el.parentElement.parentElement;
            const MC = oP.nextElementSibling.querySelector('div.mermaid');
            downloadPNG(MC);
        }

        if (el.tagName == "BUTTON" && el.classList.contains("pre-button")) {
            const oI = el.querySelector('i');
            if (oI) {
                if (oI.classList.contains('fa-angle-up')) {
                    oI.classList.remove('fa-angle-up');
                    oI.classList.add('fa-angle-down');
                    el.parentElement.parentElement.style.width = el.getBoundingClientRect().width + 20 + 'px';
                    el.parentElement.parentElement.style.height = '32px';
                    el.parentElement.parentElement.style.overflow = 'hidden';
                    el.parentElement.querySelector('.pre-header-tools').style.display = 'none';
                } else {
                    oI.classList.remove('fa-angle-down');
                    oI.classList.add('fa-angle-up');
                    el.parentElement.parentElement.style.width = '';
                    el.parentElement.parentElement.style.overflow = '';
                    el.parentElement.parentElement.style.height = '';
                    el.parentElement.querySelector('.pre-header-tools').style.display = '';
                }
            }
        }
    });
}

function changeTools(oP) {
    const preHeaderTools = oP.querySelector('.pre-header-tools');
    const code = oP.nextElementSibling.querySelector('code');
    preHeaderTools.dataset.scode = preHeaderTools.dataset.scode === "0" ? "1" : "0";
    if (preHeaderTools.dataset.scode === "0") {
        preHeaderTools.querySelector(".copy-icon").style.display = "none";
        preHeaderTools.querySelector(".mermaid-scale-big").style.display = "inline-block";
        preHeaderTools.querySelector(".mermaid-scale-small").style.display = "inline-block";
        preHeaderTools.querySelector(".mermaid-reset-chart").style.display = "inline-block";
        code.innerHTML = `<div data-scale="1" data-posX="0" data-posY="0" class="mermaid">${code.dataset.code}</div>`;
        renderMermaid();
    } else {
        preHeaderTools.querySelector(".copy-icon").style.display = "inline-block";
        preHeaderTools.querySelector(".mermaid-scale-big").style.display = "none";
        preHeaderTools.querySelector(".mermaid-scale-small").style.display = "none";
        preHeaderTools.querySelector(".mermaid-reset-chart").style.display = "none";
        code.innerHTML = `<div class="mermaid-code">${code.dataset.code}</div>`;
    }
}

// 更新变换
function updateTransform(container) {
    container.style.transform = `translate(${container.dataset.posx}px, ${container.dataset.posy}px) scale(${container.dataset.scale})`;
}

// 添加缩放和拖动功能
function setupZoomAndDrag() {
    const containers = document.querySelectorAll('.pre-container .mermaid');
    if (containers.length <= 0) return;
    let startX, startY;
    let posX = 0;
    let posY = 0;
    let isDragging = false;
    containers.forEach(container => {
        // 鼠标按下事件 - 开始拖动

        let moveContainer = null;
        container.style.backgroundColor = '#fff';

        container.addEventListener('mousedown', (e) => {
            if (e.button !== 0) return; // 只响应左键
            isDragging = true;
            container.classList.add('dragging');
            startX = e.clientX - posX;
            startY = e.clientY - posY;
            moveContainer = container;
            e.preventDefault();
        });

        // 鼠标移动事件 - 拖动中
        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            posX = e.clientX - startX;
            posY = e.clientY - startY;
            if (moveContainer) {
                const scale = moveContainer.dataset.scale;
                moveContainer.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
            }
        });

        // 鼠标抬起事件 - 结束拖动
        document.addEventListener('mouseup', () => {
            isDragging = false;
            moveContainer && moveContainer.classList.remove('dragging');
        });

        // 鼠标离开窗口事件 - 结束拖动
        document.addEventListener('mouseleave', () => {
            isDragging = false;
            moveContainer && moveContainer.classList.remove('dragging');
        });

        // 触摸事件支持
        container.addEventListener('touchstart', (e) => {
            if (e.touches.length !== 1) return;
            isDragging = true;
            container.classList.add('dragging');
            startX = e.touches[0].clientX - posX;
            startY = e.touches[0].clientY - posY;
            moveContainer = container;
            e.preventDefault();
        }, { passive: true });

        document.addEventListener('touchmove', (e) => {
            if (!isDragging || e.touches.length !== 1) return;
            posX = e.touches[0].clientX - startX;
            posY = e.touches[0].clientY - startY;
            if (moveContainer) {
                const scale = moveContainer.dataset.scale;
                moveContainer.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
            }
            e.preventDefault();
        }, { passive: false });

        document.addEventListener('touchend', () => {
            isDragging = false;
            moveContainer && moveContainer.classList.remove('dragging');
        }, { passive: true });
    });
}

