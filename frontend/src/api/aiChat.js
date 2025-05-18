import store from '@/store';
import request from '@/utils/request';
import { config } from '@/utils/config'

export function AiChat(params) {
    const { authorization } = store.state.app
    const url = config.BASE_URL + "/ai_chat/stream";

    return fetch(url, {
        method: 'POST',
        headers: {
            'Token': authorization,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    });
}

export function saveAiChat(params) {
    return request({
        url: 'ai_chat/save_chat',
        method: 'post',
        params: params,
    });
}


export function saveAiChatTitle(params) {
    return request({
        url: 'ai_chat/save_chat_title',
        method: 'post',
        params: params,
    });
}

export function aiChatList(params) {
    return request({
        url: 'ai_chat/list',
        method: 'get',
        params: params,
    });
}

export function aiOneChat(params) {
    return request({
        url: 'ai_chat/one_chat',
        method: 'get',
        params: params,
    });
}

export function deleteOneChat(params) {
    return request({
        url: 'ai_chat/delOneChat',
        method: 'post',
        params: params,
    });
}

export function deleteChat(params) {
    return request({
        url: 'ai_chat/delete',
        method: 'post',
        params: params,
    });
}

export function editChatName(params) {
    return request({
        url: 'ai_chat/update',
        method: 'post',
        params: params,
    });
}

export function queryChat(params) {
    return request({
        url: 'ai_chat/query',
        method: 'get',
        params: params,
    });
}

export function queryTalkName(params) {
    return request({
        url: 'ai_chat/queryTalkName',
        method: 'get',
        params: params,
    });
}

export function queryRecommend(params) {
    return request({
        url: 'ai_chat/queryRecommend',
        method: 'get',
        params: params,
    });
}

export function shareChat(params) {
    return request({
        url: 'ai_chat/shareChat',
        method: 'post',
        params: params,
    });
}

export function getRedisChat(params) {
    return request({
        url: 'ai_chat/getRedisChat',
        method: 'get',
        params: params,
    });
}