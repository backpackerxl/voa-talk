import request from '@/utils/request';

export function findListPage(params) {
    return request({
        url: 'email_logs/findListPage',
        method: 'get',
        params: params,
    })
}

export function getEmailBody(eid) {
    return request({
        url: 'email_logs/getEmailBody/' + eid,
        method: 'get',
    })
}

export function findUsers(params) {
    return request({
        url: 'email_logs/findUsers',
        method: 'get',
        params: params,
    })
}

export function emailDel(params) {
    return request({
        url: 'email_logs/delete',
        method: 'post',
        params: params,
    })
}


export function sendEmail(params) {
    return request({
        url: 'email_logs/sendEmail',
        method: 'post',
        params: params,
    })
}