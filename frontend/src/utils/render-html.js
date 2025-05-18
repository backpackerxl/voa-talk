import renderMathInElement from "katex/dist/contrib/auto-render";
import { marked } from "marked";
import DOMPurify from "dompurify";
import hljs from "highlight.js";
import html from 'highlight.js/lib/languages/xml';
import javascript from 'highlight.js/lib/languages/javascript';
import css from 'highlight.js/lib/languages/css';
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
export function markdwonToHTML(content) {
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
        hljs.highlightElement(block);
        // 确保每个代码块只有一个图标
        if (!block.parentNode.querySelector(".copy-icon")) {
            const oDivC = document.createElement("div");
            const oDivH = document.createElement("div");
            const oButton = document.createElement("button");

            oButton.innerText = block.classList[0].split('-')[1] || 'code';

            const copyIcon = document.createElement("i");
            const upIcon = document.createElement("i");
            oDivC.className = 'pre-container'
            oDivH.className = 'pre-header'
            oButton.className = 'pre-button';
            copyIcon.className = "copy-icon fa-solid fa-copy"; // Font Awesome 复制图标
            upIcon.className = "fas fa-angle-up"; // Font Awesome 复制图标

            oButton.appendChild(upIcon);

            // 将图标插入到 <pre> 元素中
            oDivH.appendChild(oButton);
            oDivH.appendChild(copyIcon);
            oDivC.appendChild(oDivH);
            let preBefore = block.parentNode.previousElementSibling;
            oDivC.appendChild(block.parentNode);
            preBefore.after(oDivC);

        }
    });

    return oDiv.innerHTML;
};


export function addCopy() {
    document.querySelectorAll('i.copy-icon').forEach(el => {
        // 绑定点击事件
        el.addEventListener("click", () => {
            navigator.clipboard
                .writeText(el.parentElement.nextElementSibling.innerText)
                .then(() => {
                    el.className = "copy-icon fas fa-check"; // 切换为成功图标
                    el.style.color = "#28a745"; // 成功颜色

                    setTimeout(() => {
                        el.className = "copy-icon fa-solid fa-copy";
                        el.style.color = "rgb(121, 122, 123)"; // 恢复原样
                    }, 2000); // 2 秒后恢复原样
                })
                .catch((err) => {
                    console.error("无法复制代码:", err);
                });
        });
    });

    document.querySelectorAll('button.pre-button').forEach(el => {
        // 绑定点击事件
        el.addEventListener("click", () => {
            const oI = el.querySelector('i');
            if (oI) {
                if (oI.classList.contains('fa-angle-up')) {
                    oI.classList.remove('fa-angle-up');
                    oI.classList.add('fa-angle-down');
                    el.parentElement.parentElement.style.width = el.getBoundingClientRect().width + 20 + 'px';
                    el.parentElement.parentElement.style.height = '30px';
                    el.parentElement.parentElement.style.overflow = 'hidden';
                    el.parentElement.querySelector('i.copy-icon').style.display = 'none';
                } else {
                    oI.classList.remove('fa-angle-down');
                    oI.classList.add('fa-angle-up');
                    el.parentElement.parentElement.style.width = '';
                    el.parentElement.parentElement.style.overflow = '';
                    el.parentElement.parentElement.style.height = '';
                    el.parentElement.querySelector('i.copy-icon').style.display = '';
                }
            }
        });
    });
}

