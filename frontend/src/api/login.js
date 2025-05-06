import request from '@/utils/request';

export function loginUser(userName, passWord, verifyCode) {
    return request({
        url: '/login/login',
        method: 'post',
        params: {userName, passWord, verifyCode},
    });
}


export function loginCode() {
    return request({
        url: '/login/getVerifyCode',
        method: 'get'
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
