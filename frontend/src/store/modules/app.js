const state = {
    authorization: localStorage.getItem('token') || '', // 初始化时从 localStorage 获取 token
    userRole: Number(localStorage.getItem('userRole')) || 0, // 初始化时从 localStorage 获取用户角色，默认 0 表示非超级管理员
    nickName: localStorage.getItem('nickName') || '', // 初始化
    avatar: localStorage.getItem('avatar') || '', // 初始化
    sliderData: null,
    them: localStorage.getItem('them') || 'light', // 初始化
    mainColor: localStorage.getItem('mainColor') || null,
    sliderMenu: localStorage.getItem('sliderMenu') || true,
};

const mutations = {
    SET_AUTHORIZATION(state, token) {
        state.authorization = token;
    },
    CLEAR_AUTHORIZATION(state) {
        state.authorization = '';
    },
    SET_USER_ROLE(state, role) {
        state.userRole = role;
    },
    CLEAR_USER_ROLE(state) {
        state.userRole = 0; // 重置为默认值
    },
    SET_NICK_NAME(state, nickName) {
        state.nickName = nickName;
    },
    CLEAR_NICK_NAME(state) {
        state.nickName = '';
    },
    SET_AVATAR(state, avatar) {
        state.avatar = avatar;
    },
    CLEAR_AVATAR(state) {
        state.avatar = '';
    },
    SET_SLIDER_DATA(state, sliderData) {
        state.sliderData = sliderData;
    },
    CLEAR_SLIDER_DATA(state) {
        state.sliderData = null;
    },
    SET_THEM(state, them) {
        state.them = them;
    },
    CLEAR_THEM(state) {
        state.them = 'light';
    },
    SET_MAIN_COLOR(state, colorObj) {
        state.mainColor = colorObj;
    },
    CLEAR_MAIN_COLOR(state) {
        state.mainColor = null
    },
    SET_SLIDER_MENU(state, sliderMenu) {
        state.sliderMenu = sliderMenu;
    },
    CLEAR_SLIDER_MENU(state) {
        state.sliderMenu = true
    },
};

const actions = {
    setAuthorization({ commit }, token) {
        commit('SET_AUTHORIZATION', token);
        localStorage.setItem('token', token); // 同步保存到 localStorage
    },
    clearAuthorization({ commit }) {
        commit('CLEAR_AUTHORIZATION');
        localStorage.removeItem('token'); // 清除 localStorage 中的 token
    },
    setUserRole({ commit }, role) {
        commit('SET_USER_ROLE', role);
        localStorage.setItem('userRole', role); // 同步保存到 localStorage
    },
    clearUserRole({ commit }) {
        commit('CLEAR_USER_ROLE');
        localStorage.removeItem('userRole'); // 清除 localStorage 中的用户角色
    },
    setNickName({ commit }, nickName) {
        commit('SET_NICK_NAME', nickName);
        localStorage.setItem('nickName', nickName); // 同步保存到 localStorage
    },
    clearNickName({ commit }) {
        commit('CLEAR_NICK_NAME');
        localStorage.removeItem('nickName'); // 清除 localStorage 中的用户角色
    },
    setAvatar({ commit }, avatar) {
        commit('SET_AVATAR', avatar);
        localStorage.setItem('avatar', avatar); // 同步保存到 localStorage
    },
    clearAvatar({ commit }) {
        commit('CLEAR_AVATAR');
        localStorage.removeItem('avatar'); // 清除 localStorage 中的用户角色
    },
    setSliderData({ commit }, sliderData) {
        commit('SET_SLIDER_DATA', sliderData);
    },
    clearSliderData({ commit }) {
        commit('CLEAR_SLIDER_DATA');
    },
    setThem({ commit }, them) {
        commit('SET_THEM', them);
        localStorage.setItem('them', them); // 同步保存到 localStorage
    },
    clearThem({ commit }) {
        commit('CLEAR_THEM');
        localStorage.setItem('them', 'light'); // 同步保存到 localStorage
    },
    setMainColor({ commit }, colorObj) {
        commit('SET_MAIN_COLOR', colorObj);
        localStorage.setItem('mainColor', colorObj); // 同步保存到 localStorage
    },
    clearMainColor({ commit }) {
        commit('CLEAR_MAIN_COLOR');
    },
    setSliderMenu({ commit }, sliderMenu) {
        commit('SET_SLIDER_MENU', sliderMenu);
        localStorage.setItem('sliderMenu', sliderMenu); // 同步保存到 localStorage
    },
    clearSliderMenu({ commit }) {
        commit('CLEAR_SLIDER_MENU');
        localStorage.setItem('sliderMenu', true);
    },
};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
};
