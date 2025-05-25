import request from '@/utils/request';

export function headerData() {
    return request({
        url: 'report/header_data',
        method: 'get',
    })
}

export function topTalk() {
    return request({
        url: 'report/top_talk',
        method: 'get',
    })
}

export function modelTalks(params) {
    return request({
        url: 'report/model_talks',
        method: 'get',
        params: params,
    })
}

export function barTalks(params) {
    return request({
        url: 'report/bar_talks',
        method: 'get',
        params: params,
    })
}

export function lineTokens(params) {
    return request({
        url: 'report/line_tokens',
        method: 'get',
        params: params,
    })
}
