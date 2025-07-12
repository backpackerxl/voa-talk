import katex from 'katex';
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
    breaks: true,
    gfm: true,
});

function preprocessMarkdown(text) {
    // 处理所有嵌套在 **...** 中的星号
    return text.replace(/\*\*(.*?)\*\*/g, (match, content) => {
        // 转义内容中的星号
        const escapedContent = content.replace(/\*/g, '\\*');
        return `**${escapedContent}**`;
    });
}

// 扩展 marked 支持多种数学公式格式

const mathExtensions = [
    // 1. 行内公式：$...$（基础格式）
    {
        name: 'inlineMathDollar',
        level: 'inline',
        start(src) {
            const index = src.indexOf('$');
            if (index === -1) return null;
            if (index > 0 && src[index - 1] === '\\') return null; // 跳过转义的$
            return index;
        },
        tokenizer(src) {
            // 匹配$...$，允许括号和转义字符
            const match = src.match(/^\$((?:\\\$|\\\(|\\\)|\\.|[^$])+?)\$/);
            if (!match) return null;
            return {
                type: 'inlineMathDollar',
                raw: match[0],
                text: match[1].trim()
            };
        },
        renderer(token) {
            try {
                return katex.renderToString(token.text, {
                    throwOnError: false,
                    displayMode: false,
                    extensions: ['mhchem', 'phy']
                });
            } catch (error) {
                return `<span class="katex-error">行内公式错误: ${formatErrorMsg(error.message)}</span>`;
            }
        }
    },

    // 2. 块级公式：$$...$$（基础格式）
    {
        name: 'blockMathDollar',
        level: 'block',
        start(src) {
            const index = src.indexOf('$$');
            if (index === -1) return null;
            if (index > 0 && src[index - 1] !== '\n') return null; // 确保$$在行首或换行后
            return index;
        },
        tokenizer(src) {
            // 匹配$$...$$，支持多行和LaTeX环境
            const match = src.match(/^\$\$((?:\\\$|\\\(|\\\)|\\.|[\s\S])+?)\$\$/);
            if (!match) return null;
            return {
                type: 'blockMathDollar',
                raw: match[0],
                text: match[1].trim()
            };
        },
        renderer(token) {
            try {
                return `<div class="katex-block">${katex.renderToString(token.text, {
                    displayMode: true,
                    throwOnError: false,
                    extensions: ['mhchem', 'phy']
                })}</div>`;
            } catch (error) {
                return `<div class="katex-error">块级公式错误: ${formatErrorMsg(error.message)}</div>`;
            }
        }
    },

    // 3. 行内公式：\(...\)（LaTeX标准格式）
    {
        name: 'inlineMathParenthesis',
        level: 'inline',
        start(src) {
            const index = src.indexOf('\\(');
            if (index === -1) return null;
            // 确保\(前不是字母或数字（避免误匹配函数名如f\(x\)）
            if (index > 0 && /[a-zA-Z0-9]/.test(src[index - 1])) return null;
            return index;
        },
        tokenizer(src) {
            // 匹配\(...\)，允许嵌套括号和转义字符
            const match = src.match(/^\\\(((?:\\\)|\\\(|\\.|[\s\S])+?)\\\)/);
            if (!match) return null;
            return {
                type: 'inlineMathParenthesis',
                raw: match[0],
                text: match[1].trim()
            };
        },
        renderer(token) {
            try {
                return katex.renderToString(token.text, {
                    throwOnError: false,
                    displayMode: false
                });
            } catch (error) {
                return `<span class="katex-error">行内公式错误: ${formatErrorMsg(error.message)}</span>`;
            }
        }
    },

    // 4. 块级公式：\[...\]（LaTeX标准格式）
    {
        name: 'blockMathBracket',
        level: 'block',
        start(src) {
            const index = src.indexOf('\\[');
            if (index === -1) return null;
            if (index > 0 && src[index - 1] !== '\n') return null; // 确保\[在行首或换行后
            return index;
        },
        tokenizer(src) {
            // 匹配\[...\]，支持多行和复杂环境
            const match = src.match(/^\\\[((?:\\\]|\\.|[\s\S])+?)\\\]/);
            if (!match) return null;
            return {
                type: 'blockMathBracket',
                raw: match[0],
                text: match[1].trim()
            };
        },
        renderer(token) {
            try {
                return `<div class="katex-block">${katex.renderToString(token.text, {
                    displayMode: true,
                    throwOnError: false
                })}</div>`;
            } catch (error) {
                return `<div class="katex-error">块级公式错误: ${formatErrorMsg(error.message)}</div>`;
            }
        }
    },

    // 5. 增强版：LaTeX 环境公式处理器
    {
        name: 'multilineMath',
        level: 'block',
        start(src) {
            return Math.min(
                src.indexOf('\\begin{align'),
                src.indexOf('\\begin{gather'),
                src.indexOf('\\begin{aligned'),
                src.indexOf('\\begin{split')
            );
        },
        tokenizer(src) {
            // 匹配多行数学环境，包括带星号的版本
            const envMatch = src.match(/^\\begin\{(\*?[a-zA-Z]+)\*?\}([\s\S]*?)\\end\{\1\*?\}/);
            if (envMatch) {
                return {
                    type: 'multilineMath',
                    raw: envMatch[0],
                    env: envMatch[1],
                    content: envMatch[2].trim()
                };
            }
            return null;
        },
        renderer(token) {
            try {
                let content = token.content;

                // 优化反斜杠处理：只在必要的地方添加额外的反斜杠
                // 这里使用更精确的正则表达式，只处理行末的 \\
                content = content.replace(/\\\s*$/gm, '\\\\');

                // 特殊处理 align 环境，保留星号信息
                let renderEnv = token.env;
                if (renderEnv.startsWith('align')) {
                    renderEnv = renderEnv === 'align' ? 'aligned' : 'aligned*';
                }

                // 创建 KaTeX 渲染元素
                const container = document.createElement('div');
                container.className = 'katex-multiline-container';

                // 使用 KaTeX 渲染
                katex.render(
                    `\\begin{${renderEnv}}${content}\\end{${renderEnv}}`,
                    container,
                    {
                        displayMode: true,
                        throwOnError: false,
                        fleqn: false,
                        maxSize: Infinity,
                        maxExpand: Infinity,
                        macros: {
                            "\\RR": "\\mathbb{R}",
                            "\\C": "\\mathbb{C}",
                            "\\N": "\\mathbb{N}",
                            "\\Z": "\\mathbb{Z}"
                        }
                    }
                );

                // 修复 KaTeX 自动添加的换行样式
                const katexElements = container.querySelectorAll('.katex > .katex-html');
                if (katexElements.length > 0) {
                    katexElements[0].style.display = 'inline-block';
                    katexElements[0].style.width = 'auto';
                }

                return container.innerHTML;
            } catch (error) {
                return `<div class="katex-error">多行公式错误: ${error.message.replace(/^KaTeX parse error: /, '').slice(0, 100)
                    }</div>`;
            }
        }
    }
];

// 辅助函数：格式化错误信息
function formatErrorMsg(msg) {
    if (msg.includes('Undefined control sequence')) {
        return '未知命令（检查拼写，如\\abc）';
    } else if (msg.includes('Missing delimiter')) {
        return '缺失闭合符号（如)、]、}）';
    } else if (msg.includes('Expected')) {
        return '语法错误（可能缺少符号）';
    } else {
        return msg.replace(/KaTeX parse error: /, '');
    }
}

marked.use({
    extensions: mathExtensions,
    breaks: true,  // 允许换行符
    gfm: true      // GitHub风格Markdown
});

function parseMarkdown(markdown) {
    // 预处理：保护算法名称中的星号
    const protectedText = preprocessMarkdown(markdown);
    return DOMPurify.sanitize(marked.parse(protectedText));
}


// 添加复制图标的方法
export function markdwonToHTML(content, showPlayIcon) {
    const oDiv = document.createElement("div");
    oDiv.innerHTML = parseMarkdown(content);

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
            const oDivHC = document.createElement("div");
            const oDivHCB = document.createElement("div");
            const oDivTools = document.createElement("div");
            const oButton = document.createElement("button");

            oButton.innerText = block.classList[0].split('-')[1] || 'code';

            const copyIcon = document.createElement("i");
            const upIcon = document.createElement("i");
            oDivC.className = 'pre-container'
            oDivH.className = 'pre-header'
            oDivHC.className = 'pre-header-container'
            oDivHCB.className = 'pre-header-block'
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
            oDivHCB.appendChild(oDivH);
            oDivHC.appendChild(oDivHCB);
            oDivC.appendChild(oDivHC);
            let preBefore = block.parentNode.previousElementSibling;
            oDivC.appendChild(block.parentNode);
            preBefore && preBefore.after(oDivC);
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
            clipboard.writeText(el.parentElement.parentElement.parentElement.parentElement.nextElementSibling.innerText).then(
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
            const code = el.parentElement.parentElement.parentElement.parentElement.nextElementSibling.innerText;
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
            oAside && oAside.classList.add("code-play");
            oMain.appendChild(oDivC);

            oI.addEventListener('click', function () {
                oAside && oAside.classList.remove("code-play");
                oDivC.remove();
            });
        }

        if (el.tagName == "I" && el.classList.contains("prebtn-arrow")) {
            const oP = el.parentElement.parentElement.parentElement.parentElement;
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
            const oP = el.parentElement.parentElement.parentElement.parentElement;
            changeTools(oP);
        }

        if (el.tagName == "I" && el.classList.contains("mermaid-scale-big")) {
            const oP = el.parentElement.parentElement.parentElement.parentElement;
            const MC = oP.nextElementSibling.querySelector('div.mermaid');
            let st = MC.dataset.scale * 1.2;
            MC.dataset.scale = st > 10 ? 10 : st;
            updateTransform(MC);
            if (st > 10) {
                ElMessage.warning("不能再放大了！");
            }
        }

        if (el.tagName == "I" && el.classList.contains("mermaid-scale-small")) {
            const oP = el.parentElement.parentElement.parentElement.parentElement;
            const MC = oP.nextElementSibling.querySelector('div.mermaid');
            let st = MC.dataset.scale * 0.8;
            MC.dataset.scale = st < 0.3 ? 0.3 : st;
            updateTransform(MC);
            if (st < 0.3) {
                ElMessage.warning("不能再缩小了！");
            }
        }

        if (el.tagName == "I" && el.classList.contains("mermaid-reset-chart")) {
            const oP = el.parentElement.parentElement.parentElement.parentElement;
            const MC = oP.nextElementSibling.querySelector('div.mermaid');
            MC.dataset.scale = 1;
            MC.dataset.posx = 0;
            MC.dataset.posy = 0;
            updateTransform(MC);
            ElMessage.success("已重置！");
        }

        if (el.tagName == "I" && el.classList.contains("mermaid-down-png")) {
            const oP = el.parentElement.parentElement.parentElement.parentElement;
            const MC = oP.nextElementSibling.querySelector('div.mermaid');
            downloadPNG(MC);
        }

        if (el.tagName == "BUTTON" && el.classList.contains("pre-button")) {
            const oI = el.querySelector('i');
            const preC = el.parentElement.parentElement.parentElement.parentElement;
            if (oI) {
                if (oI.classList.contains('fa-angle-up')) {
                    oI.classList.remove('fa-angle-up');
                    oI.classList.add('fa-angle-down');
                    preC.style.width = el.getBoundingClientRect().width + 20 + 'px';
                    preC.style.height = '32px';
                    preC.style.overflow = 'hidden';
                    el.parentElement.querySelector('.pre-header-tools').style.display = 'none';
                } else {
                    oI.classList.remove('fa-angle-down');
                    oI.classList.add('fa-angle-up');
                    preC.style.width = '';
                    preC.style.overflow = '';
                    preC.style.height = '';
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

