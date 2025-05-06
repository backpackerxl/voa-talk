import request from '@/utils/request';

export function ApiModelFindListPage(params) {
    return request({
        url: 'model_config/query',
        method: 'get',
        params:params,
    })
}

export function ApiModelDel(params) {
    return request({
        url: 'model_config/delete',
        method: 'post',
        params:params,
    })
}


export function ApiModelExit(params) {
    return request({
        url: 'model_config/saveOrUpdate',
        method: 'post',
        params:params,
    })
}

export function ApiModelList(params) {
    return request({
        url: 'model_config/list',
        method: 'get',
        params:params,
    })
}
