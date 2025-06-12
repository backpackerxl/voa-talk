import request from '@/utils/request';

export function verify(params) {
    return request({
        url: 'captcha/verify',
        method: 'post',
        params: params,
    });
}

export function refresh() {
    return request({
        url: 'captcha/refresh',
        method: 'get',
    });
}