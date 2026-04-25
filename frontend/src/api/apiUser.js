import request from '@/utils/request';

export function ApiUserFindListPage(params) {
    return request({
        url: 'sys_user/findListPage',
        method: 'get',
        params: params,
    })
}

export function ApiUserDel(params) {
    return request({
        url: 'sys_user/delete',
        method: 'post',
        params: params,
    })
}


export function ApiUserExit(params) {
    return request({
        url: 'sys_user/saveOrUpdate',
        method: 'post',
        params: params,
    })
}

export function updateUser(params) {
    return request({
        url: 'sys_user/updateUser',
        method: 'post',
        params: params,
    })
}

export function sendEmailCodeApi(params) {
    return request({
        url: 'sys_user/sendEmailCode',
        method: 'post',
        params: params,
    })
}

export function updateUserEmail(params) {
    return request({
        url: 'sys_user/updateUserEmail',
        method: 'post',
        params: params,
    })
}

export function singOutDevice(params) {
    return request({
        url: 'sys_user/singOutDevice',
        method: 'post',
        params: params,
    })
}

export function queryLoginUser() {
    return request({
        url: 'sys_user/queryLoginUser',
        method: 'get',
    })
}
