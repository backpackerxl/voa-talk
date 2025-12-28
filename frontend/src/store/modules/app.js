const state = {
    authorization: localStorage.getItem('token') || '', // 初始化时从 localStorage 获取 token
    userRole: Number(localStorage.getItem('userRole')) || 0, // 初始化时从 localStorage 获取用户角色，默认 0 表示非超级管理员
    nickName: localStorage.getItem('nickName') || '', // 初始化
    userName: localStorage.getItem('userName') || '', // 初始化
    userEmail: localStorage.getItem('userEmail') || '', // 初始化
    avatar: localStorage.getItem('avatar') || '', // 初始化
    loginType: localStorage.getItem('loginType') || '', // 初始化
    noKeyLogin: localStorage.getItem('noKeyLogin') || '', // 初始化
    bindOtherAccount: localStorage.getItem('bindOtherAccount') || '', // 初始化
    bindQQ: localStorage.getItem('bindQQ') || 0, // 初始化
    bindGitHub: localStorage.getItem('bindGitHub') || 0, // 初始化
    sliderData: null,
    them: localStorage.getItem('them') || JSON.stringify({
        them: "light",
        label: "浅色",
        icon: "fa-solid fa-sun",
    }), // 初始化
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
    SET_USER_NAME(state, userName) {
        state.userName = userName;
    },
    CLEAR_USER_NAME(state) {
        state.userName = '';
    },
    SET_USER_EMAIL(state, userEmail) {
        state.userEmail = userEmail;
    },
    CLEAR_USER_EMAIL(state) {
        state.userEmail = '';
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
        state.them = JSON.stringify({
            them: "light",
            label: "浅色",
            icon: "fa-solid fa-sun",
        });
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
    SET_LOGIN_TYPE(state, loginType) {
        state.loginType = loginType;
    },
    CLEAR_LOGIN_TYPE(state) {
        state.loginType = '';
    },
    SET_NO_KEY_LOGIN(state, noKeyLogin) {
        state.noKeyLogin = noKeyLogin;
    },
    CLEAR_NO_KEY_LOGIN(state) {
        state.noKeyLogin = '';
    },
    SET_BIND_OTHER_ACCOUNT(state, bindOtherAccount) {
        state.bindOtherAccount = bindOtherAccount;
    },
    CLEAR_BIND_OTHER_ACCOUNT(state) {
        state.bindOtherAccount = '';
    },
    SET_BIND_QQ(state, bindQQ) {
        state.bindQQ = bindQQ;
    },
    CLEAR_BIND_QQ(state) {
        state.bindQQ = 0;
    },
    SET_BIND_GITHUB(state, bindGitHub) {
        state.bindGitHub = bindGitHub;
    },
    CLEAR_BIND_GITHUB(state) {
        state.bindGitHub = 0;
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
    setUserName({ commit }, userName) {
        commit('SET_USER_NAME', userName);
        localStorage.setItem('userName', userName); // 同步保存到 localStorage
    },
    clearUserName({ commit }) {
        commit('CLEAR_USER_NAME');
        localStorage.removeItem('userName'); // 清除 localStorage 中的用户
    },
    setUserEmail({ commit }, userEmail) {
        commit('SET_USER_EMAIL', userEmail);
        localStorage.setItem('userEmail', userEmail); // 同步保存到 localStorage
    },
    clearUserEmail({ commit }) {
        commit('CLEAR_USER_EMAIL');
        localStorage.removeItem('userEmail'); // 清除 localStorage 中的用户邮箱
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
        localStorage.setItem('them', JSON.stringify({
            them: "light",
            label: "浅色",
            icon: "fa-solid fa-sun",
        })); // 同步保存到 localStorage
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
    setLoginType({ commit }, loginType) {
        commit('SET_LOGIN_TYPE', loginType);
        localStorage.setItem('loginType', loginType); // 同步保存到 localStorage
    },
    clearLoginType({ commit }) {
        commit('CLEAR_LOGIN_TYPE');
        localStorage.removeItem('loginType'); // 清除 localStorage 中的登录类型
    },
    setNoKeyLogin({ commit }, noKeyLogin) {
        commit('SET_NO_KEY_LOGIN', noKeyLogin);
        localStorage.setItem('noKeyLogin', noKeyLogin); // 同步保存到 localStorage
    },
    clearNoKeyLogin({ commit }) {
        commit('CLEAR_NO_KEY_LOGIN');
        localStorage.removeItem('noKeyLogin'); // 清除 localStorage 中的免密登录
    },
    setBindOtherAccount({ commit }, bindOtherAccount) {
        commit('SET_BIND_OTHER_ACCOUNT', bindOtherAccount);
        localStorage.setItem('bindOtherAccount', bindOtherAccount); // 同步保存到 localStorage
    },
    clearBindOtherAccount({ commit }) {
        commit('CLEAR_BIND_OTHER_ACCOUNT');
        localStorage.removeItem('bindOtherAccount'); // 清除 localStorage 中的绑定其他账号
    },
    setBindQQ({ commit }, bindQQ) {
        commit('SET_BIND_QQ', bindQQ);
        localStorage.setItem('bindQQ', bindQQ); // 同步保存到 localStorage
    },
    clearBindQQ({ commit }) {
        commit('CLEAR_BIND_QQ');
        localStorage.removeItem('bindQQ'); // 清除 localStorage 中的绑定QQ账号
    },
    setBindGitHub({ commit }, bindGitHub) {
        commit('SET_BIND_GITHUB', bindGitHub);
        localStorage.setItem('bindGitHub', bindGitHub); // 同步保存到 localStorage
    },
    clearBindGitHub({ commit }) {
        commit('CLEAR_BIND_GITHUB');
        localStorage.removeItem('bindGitHub'); // 清除 localStorage 中的绑定GitHub账号
    },
};



export default {
    namespaced: true,
    state,
    mutations,
    actions,
};
