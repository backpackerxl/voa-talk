import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';  // 导入 Vuex store
// import MainLayout from '@/layouts/MainLayout.vue';

const Login = () => import('@/views/Login/index.vue');
const Register = () => import('@/views/Login/Register.vue');
const Forget = () => import('@/views/Login/Forget.vue');
const ResetPwd = () => import('@/views/Login/ResetPwd.vue');

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { requiresAuth: false },
    },
    {
        path: '/',
        redirect: '/login',
    },
    {
        path: '/home',
        component: () => import('@/views/async/home/slider.vue'),
        redirect: '/home/chat',
        meta: { requiresAuth: true },  // 如果这里设置了 requiresAuth

        children: [
            {
                path: 'user',
                component: () => import('@/views/async/user/index.vue'),
            },
            {
                path: 'chat/:id',
                component: () => import('@/views/async/Dialogue/index.vue'),
            },
            {
                path: 'chat',
                component: () => import('@/views/async/Dialogue/index.vue'),
            },
            {
                path: 'chat/history',
                component: () => import('@/views/async/chatHis/index.vue'),
            },
            {
                path: 'profile',
                component: () => import('@/views/async/profile/index.vue'),
            },
            {
                path: 'model',
                component: () => import('@/views/async/model/index.vue'),
            },
        ],
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { requiresAuth: false },
    },
    {
        path: '/forget',
        name: 'Forget',
        component: Forget,
        meta: { requiresAuth: false },
    },
    {
        path: '/resetPwd/:secretKey',
        name: 'ResetPwd',
        component: ResetPwd,
        meta: { requiresAuth: false },
    },
    // 添加更多路由
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const isAuthenticated = store.state.app.authorization !== ''; // 检查是否已认证
    const userRole = store.state.app.userRole;
    // console.log("userRole", userRole);
    // console.log("isAuthenticated", isAuthenticated);
    // console.log("Navigating to:", to.path);
    if (to.matched.some((record) => record.meta.requiresAuth) && !isAuthenticated) {
        console.log("Not authenticated, redirecting to /login");
        next({ path: '/login' });
    } else if (to.path === '/home/user' && Number(userRole) !== 1) {

        console.log("Not super admin, redirecting to /home/chat");
        // 如果不是超级管理员，重定向到其他页面
        next({ path: '/home/chat' });
    } else if (to.path === '/home/model' && Number(userRole) !== 1) {

        console.log("Not super admin, redirecting to /home/chat");
        // 如果不是超级管理员，重定向到其他页面
        next({ path: '/home/chat' });
    } else {
        // console.log("Proceeding to the requested route");
        next();
    }
});

export default router;
