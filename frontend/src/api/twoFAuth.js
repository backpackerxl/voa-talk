import request from '@/utils/request';

export function registerBegin(params) {
    return request({
        url: 'two_auth/register/begin',
        method: 'post',
        params: params,
    });
}

export function registerComplete(params) {
    return request({
        url: 'two_auth/register/complete',
        method: 'post',
        params: params,
    });
}

export function generateOtpQrcode(username) {
    return request({
        url: 'two_auth/otp/qrcode/' + encodeURIComponent(username),
        method: 'get',
    });
}

export function loginBegin(params) {
    return request({
        url: 'two_auth/login/begin',
        method: 'post',
        params: params,
    });
}


export function loginComplete(params) {
    return request({
        url: 'two_auth/login/complete',
        method: 'post',
        params: params,
    });
}

export function verifyOtp(params) {
    return request({
        url: 'two_auth/otp/verify',
        method: 'post',
        params: params,
    });
}