import request from '@/utils/request';
import store from '@/store';
import { config } from '@/utils/config';

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

export function allData() {
    const { authorization } = store.state.app
    const url = config.BASE_URL + "/report/all_data";
    const source = new EventSource(`${url}?token=${authorization}`)
    return source;
}
