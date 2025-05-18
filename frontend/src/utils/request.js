import axios from 'axios'
import { ElMessage } from 'element-plus'
import store from '@/store'
import router from '@/router'
import { config } from './config.js'

// 创建 axios 实例
const service = axios.create({
  baseURL: config.BASE_URL,        // 请求的基础路径
  timeout: 100000,          // 请求超时时间
  withCredentials: true,  // 是否携带凭据（例如cookie）
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const { authorization } = store.state.app
    if (authorization && config.withToken !== false) {
      config.headers['token'] = authorization
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
    response => {
      // 响应成功处理
      if (+response.data.code === 200) {
        // console.log("拦截器==》",response)
        return response.data;  // 直接返回整个 data，而不是只返回其中的 data 字段
      } else {
        ElMessage.error(response.data.msg || '服务器错误');
        return Promise.reject(response.data.msg || '服务器错误');
      }
    },
    async error => {
      console.log("error==>", error);
      // 响应失败处理
      if (error.response && (error.response.status === 401 || error.response.status === 408)) {
        const redirect = encodeURIComponent(window.location.href);
        router.push(`/login?redirect=${redirect}`);
        store.dispatch('app/clearToken');
        return Promise.reject(error);
      }
      if (error.response.data.code !== 200) {
        ElMessage.error(error.response.data?.msg || '服务器错误');
        return Promise.reject(error);
      }
      ElMessage.closeAll();
      try {
        ElMessage.error(error.response.data.msg);
      } catch (err) {
        ElMessage.error(error.message);
      }
      return Promise.reject(error);
    }
);
/**
 * 发送请求的 async 函数
 * @param {Object} options 请求参数
 */
async function instance(options) {
  // 检查参数是否正确
  if (!options.url) throw new Error('请求必须要有url地址');
  if (!options.method) options.method = 'get';
  if (!options.params) options.params = {};
  if (typeof options.params === 'object' && options.enableNull) {
    Object.keys(options.params).forEach(key => {
      if ([null, undefined, ''].includes(options.params[key])) {
        delete options.params[key];
      }
    });
    options.params._t = new Date().getTime();
  }

  const params = {
    url: options.url,
    method: options.method.toLowerCase(),
    headers: options.headers || {},
    withToken: options.withToken,
  };

  if (options.responseType) {
    params.responseType = options.responseType;
  }

  if (options.method.toLowerCase() === 'get') {
    params['params'] = options.params;
  } else {
    params['data'] = options.params;
  }

  // 处理缓存逻辑
  if (options.cache) {
    const cacheKey = JSON.stringify(options.url);
    let data = sessionStorage.getItem(cacheKey);
    if (data) {
      try {
        data = JSON.parse(data);
        return data;
      } catch (e) {
        console.error("Error parsing cached data:", e);
        return e;
      }
    }
  }

  try {
    const result = await service(params);
    // console.log("实例结果==>", result);
    if (result) {
      return result;

    // 检查返回的数据结构
    // if (result && result.data) {
    //   return result;
    } else {
      throw new Error('Invalid response structure');
    }
  } catch (e) {
    console.error("Error in instance function:", e);
    return Promise.reject(e);
  } finally {
    window.$endLoading && window.$endLoading();
  }
}

export default instance
