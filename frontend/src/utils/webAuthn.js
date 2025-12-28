/**
 * 检测浏览器是否支持WebAuthn基础API
 */
function isWebAuthnSupported() {
    // 兼容不同浏览器的前缀（如Chrome的webkit、Firefox的moz）
    const publicKeyCredential = window.PublicKeyCredential || window.webkitPublicKeyCredential || window.mozPublicKeyCredential;
    // 核心：是否存在PublicKeyCredential且支持isUserVerifyingPlatformAuthenticatorAvailable
    return !!publicKeyCredential && typeof publicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable === 'function';
}

/**
 * 辅助：判断操作系统类型
 */
function getOS() {
    const userAgent = navigator.userAgent.toLowerCase();
    const platform = navigator.platform.toLowerCase();

    if (userAgent.includes('mac')) {
        return 'macos';
    } else if (userAgent.includes('win')) {
        return 'windows';
    } else if (userAgent.includes('linux') && !userAgent.includes('android')) {
        return 'linux';
    } else if (userAgent.includes('android')) {
        return 'android';
    } else if (userAgent.includes('iphone') || userAgent.includes('ipad')) {
        return 'ios';
    } else {
        return 'unknown';
    }
}

/**
 * 辅助：判断设备类型（PC/Mobile）
 */
function getDeviceType() {
    const os = getOS();

    // 如果是iOS或Android，则为移动设备
    if (os === 'ios' || os === 'android') {
        return 'mobile';
    }
    // macOS、Windows、Linux都视为PC
    return 'pc';
}

/**
 * 获取浏览器信息
 */
function getBrowserInfo() {
    const userAgent = navigator.userAgent;

    if (userAgent.includes('Chrome') && !userAgent.includes('Edg') && !userAgent.includes('OPR')) {
        return 'chrome';
    } else if (userAgent.includes('Safari') && !userAgent.includes('Chrome')) {
        return 'safari';
    } else if (userAgent.includes('Firefox')) {
        return 'firefox';
    } else if (userAgent.includes('Edg')) {
        return 'edge';
    } else {
        return 'unknown';
    }
}

/**
 * 完整检测设备是否支持生物验证
 * @returns {Object} 包含是否支持、设备类型、操作系统、浏览器、原因等信息
 */
export async function checkBiometricSupport() {
    const os = getOS();
    const deviceType = getDeviceType();
    const browser = getBrowserInfo();

    // 步骤1：检测WebAuthn基础支持
    if (!isWebAuthnSupported()) {
        let reason = '浏览器不支持WebAuthn API，无法使用生物验证';

        // 针对macOS Safari的特定检查
        if (os === 'macos' && browser === 'safari') {
            // Safari 13+ 支持 WebAuthn，但需要特定版本
            reason += '。macOS Safari 13+ 版本支持WebAuthn，请升级浏览器版本';
        }

        return {
            supported: false,
            deviceType,
            os,
            browser,
            reason,
        };
    }

    const publicKeyCredential = window.PublicKeyCredential || window.webkitPublicKeyCredential || window.mozPublicKeyCredential;

    try {
        // 步骤2：检测是否存在支持用户验证的平台验证器（核心）
        const hasPlatformAuthenticator = await publicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();

        // 步骤3：根据操作系统和设备类型提供详细反馈
        let detailReason = '';
        let biometricType = 'unknown';

        if (hasPlatformAuthenticator) {
            // 支持生物验证，区分设备类型和操作系统
            if (deviceType === 'mobile') {
                if (os === 'ios') {
                    detailReason = 'iOS设备支持面容ID或触控ID';
                    biometricType = 'Face/Touch ID';
                } else if (os === 'android') {
                    detailReason = 'Android设备支持指纹、面部或虹膜识别';
                    biometricType = '指纹/面部';
                }
            } else if (deviceType === 'pc') {
                if (os === 'macos') {
                    detailReason = 'Mac设备支持触控ID(Touch ID)';
                    biometricType = 'Touch ID';

                    // 检查是否可能是较新的Mac设备（可能支持Face ID，但目前Apple还未在Mac上引入Face ID）
                    // 这里可以添加更多检测逻辑
                    const isNewerMac = /Macintosh.*(MacBookPro|MacBookAir|iMac).*2018|2019|2020|2021|2022|2023|2024/i.test(navigator.userAgent);
                    if (isNewerMac) {
                        detailReason = 'Mac设备支持触控ID(Touch ID)';
                    }
                } else if (os === 'windows') {
                    detailReason = 'Windows设备支持Windows Hello（面部、指纹或虹膜识别）';
                    biometricType = 'Windows Hello';
                } else if (os === 'linux') {
                    detailReason = 'Linux设备可能支持生物验证（取决于硬件和配置）';
                    biometricType = 'biometric';
                }
            }

            // 浏览器特定提示
            if (os === 'macos') {
                if (browser === 'safari') {
                    detailReason += '，建议在Safari设置中确保"自动填充"已启用';
                } else if (browser === 'chrome') {
                    detailReason += '，Chrome在macOS上需要使用macOS钥匙串';
                }
            }

            return {
                supported: true,
                deviceType,
                os,
                browser,
                biometricType,
                reason: detailReason,
            };
        } else {
            // 不支持生物验证，提供详细原因
            if (deviceType === 'mobile') {
                if (os === 'ios') {
                    detailReason = 'iOS设备未设置面容ID或触控ID，或未开启生物验证权限';
                } else if (os === 'android') {
                    detailReason = 'Android设备无生物验证模块，或未设置生物验证，或权限未开启';
                }
            } else if (deviceType === 'pc') {
                if (os === 'macos') {
                    detailReason = 'Mac设备无触控ID(Touch ID)，或未在系统偏好设置中设置指纹';

                    // 检查是否可能是MacBook Air/Pro（通常有Touch ID）
                    const isMacBook = /Macintosh.*(MacBookPro|MacBookAir)/i.test(navigator.userAgent);
                    if (isMacBook) {
                        detailReason = 'MacBook设备可能支持触控ID，但未在系统偏好设置中设置，或浏览器不支持';
                    }
                } else if (os === 'windows') {
                    detailReason = 'Windows设备无Windows Hello兼容硬件，或未设置生物验证';
                } else if (os === 'linux') {
                    detailReason = 'Linux设备通常需要额外配置才能支持生物验证';
                }
            }

            return {
                supported: false,
                deviceType,
                os,
                browser,
                reason: detailReason,
            };
        }
    } catch (error) {
        // 异常场景（如浏览器禁用WebAuthn、权限不足）
        let reason = `检测失败：${error.message}`;

        // 针对macOS的特定错误处理
        if (os === 'macos') {
            if (browser === 'safari') {
                reason += '。请确保Safari设置中的"自动填充"功能已启用';
            } else if (browser === 'chrome') {
                reason += '。Chrome在macOS上需要访问钥匙串权限，请检查系统隐私设置';
            }
        }

        return {
            supported: false,
            deviceType,
            os,
            browser,
            reason,
        };
    }
}

/**
 * 额外检测：检查macOS设备是否可能支持触控ID
 * 注意：这是一个启发式检测，不是100%准确
 */
export function guessMacTouchIDSupport() {
    const os = getOS();
    if (os !== 'macos') {
        return {
            possible: false,
            reason: '非macOS设备'
        };
    }

    const userAgent = navigator.userAgent;
    // 检查是否为较新的Mac设备（2016年及以后的MacBook Pro/Air通常有Touch ID）
    const newerMacPatterns = [
        /MacBookPro(1[5-9]|2[0-9])/,  // MacBook Pro 2015+
        /MacBookAir(1[0-9]|2[0-9])/,   // MacBook Air 2018+
        /iMac(2[0-9],)/,               // iMac 2020+
    ];

    const isLikelyHasTouchID = newerMacPatterns.some(pattern => pattern.test(userAgent));

    return {
        possible: isLikelyHasTouchID,
        reason: isLikelyHasTouchID
            ? '您的Mac设备可能支持触控ID(Touch ID)，请确保已在系统设置中设置指纹'
            : '您的Mac设备可能不支持触控ID(Touch ID)，或需要检查系统设置'
    };
}