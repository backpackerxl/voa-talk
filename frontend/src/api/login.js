import request from '@/utils/request';

export function loginUser(userName, passWord, platform) {
    return request({
        url: '/login/pt_login',
        method: 'post',
        params: { userName, passWord, platform },
    });
}

export function otherLogin(params) {
    return request({
        url: '/login/other_login',
        method: 'post',
        params: params,
    });
}

// 注册用户
export function enrollUser(params) {
    return request({
        url: '/sys_user/enroll',
        method: 'post',
        params: params,
    });
}

export function sendEnrollCode(params) {
    return request({
        url: '/sys_user/enroll/code',
        method: 'post',
        params: params,
    });
}

// 找回密码
export function forgetPwd(params) {
    return request({
        url: '/sys_user/forgetPwd',
        method: 'post',
        params: params,
    });
}

// 修改密码
export function resetPWD(params) {
    return request({
        url: '/sys_user/resetPWD',
        method: 'post',
        params: params,
    });
}
