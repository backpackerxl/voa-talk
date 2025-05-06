class ResultCode:
    SUCCESS = (200, "成功")
    FAIL = (-1, "失败")
    JSON_PARSE_ERROR = (400, "传递的json数据格式错误")
    PARAM_IS_INVALID = (-10001, "参数无效")
    PLAN_ISSUED_ERROR = (-10002, "当前计划状态异常,无法下发")
    PLAN_REPORT_ERROR = (-10003, "当前计划状态异常,无法上报")
    PLAN_REPORT_TIME_ERROR = (-10004, "当前计划已超截止时间,无法上报")
    USER_NOT_LOGGED_ID = (-20001, "用户未登录")
    USER_LOGIN_ERROR = (-20002, "用户不存在或密码错误")
    USER_ACCOUNT_FORBIDDEN = (-20003, "账号已被禁用")
    USER_NOT_EXIST = (-20004, "用户不存在")
    USER_HAS_EXISTED = (-20005, "用户名已存在")
    USER_CHECK_CODE_ERROR = (-20006, "验证码错误")
    PASSWORD_DECRYPTION_FAILED = (-20016, "密码解密失败")
    LOGIN_ERROR = (-20007, "登录异常")
    LOGIN_OUT_ERROR = (-20012, "登录退出异常")
    USER_ROLE_ERROR = (-20013, "用户未分配角色")
    SYSROLE_ID_ERROR = (-20014, "角色ID异常")
    USER_DELETED = (-20008, "用户已删除")
    TOEKN_PARSE_ERROR = (-20009, "token解析异常")
    TOEKN_NOT_EXIST = (-20010, "token不能为空")
    CLOUD_USER_INVALID_TOKEN = (401, "token无效")
    USER_TYPE_NOT_EXIST = (-20011, "用户类型不存在")
    CHECK_CODE_EXCEPTION = (-21008, "获取验证码异常")
    TWO_PWD_DIFFERENT = (-22001, "两次输入的密码不一致")
    OLD_NEW_PWD_EQUALLY = (-22002, "新旧密码一样")
    CURRENT_USER_NOT_UPDATE = (-22003, "非当前用户不能修改密码")
    OLD_PWD_ERROR = (-22004, "原密码不正确")
    ROLE_HAS_EXISTED = (-23001, "角色名称已存在")
    NOT_MATCH_AUTHORITY = (-24001, "权限不匹配")
    USER_NOT_CURRENT_AUTHORITY = (-24002, "当前用户不具备该权限")
    USER_NOT_AUTHORITY = (-24003, "当前用户没有权限")
    USER_NOT_TOKEN = (-24004, "当前用户登录信息异常，无权操作")
    DATA_EXIST = (-30503, "数据已经在")
    DATA_NOT_EXIST = (-30504, "数据不存在")
    NAME_NOT_REPEAT = (-30505, "名称不能重复")
    SYSTEM_INNER_ERROR = (-40001, "系统繁忙，请稍后重试")
    SYSTEM_SERVER_ERROR = (500, "服务器内部错误")
    PERMISSION_NO_ACCESS = (-70001, "无访问权限")
    CLOUD_USER_LOGGED = (705, "当前用户已登录")
    REQUIRED_PARAMS = (5001, "缺少必填参数")
    DICT_DOMAIN_CODE_EXIST = (-1001, "编码已存在")
    DICT_DOMAIN_VALUE_EXIST = (-1002, "同一字典大类下，已存在当前字典值")
    MENU_CODE_EXIST = (-1003, "菜单编码已存在")
    INFO_CODE_EXIST = (-1005, "编码重复")
    DICT_NULL = (-1004, "NGINX数据字典为空，请检查！")
    ERROR_CREATING_TEMPORARY_FILE = (-1006, "创建临时文件错误！")
    IMPORTED_DATA_FORMAT_ERROR = (-1007, "导入数据格式错误！")
    SYS_CHILD_EXIS = (-1101, "存在子集不能此操作")
    THE_DATE_IS_WRONG = (-11015, "未来日期不能操作")
    THE_CONTRACT_NUMBER_IS_BLANK = (-11016, "没有在流水表中查询到该合同编号，请检查合同编号是否正确")

    @classmethod
    def get_code(cls, name):
        return getattr(cls, name)[0]

    @classmethod
    def get_msg(cls, name):
        return getattr(cls, name)[1]

    @classmethod
    def get_data(cls, name):
        return getattr(cls, name)


class BusinessException(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.error_code} - {self.message}"


if __name__ == '__main__':
    print(ResultCode.get_data('PASSWORD_DECRYPTION_FAILED'))

"""
使用方法：
抛出异常：
try:
    key = b"hnciquewhngfo1qc"
except:
    # 密码解密失败
    error_code, message = ResultCode.get_code('PASSWORD_DECRYPTION_FAILED'), ResultCode.get_msg(
        'PASSWORD_DECRYPTION_FAILED')
    raise BusinessException(error_code, message)
    
捕获异常：
try:
    # 调用服务层处理业务逻辑
    asset_summary_service = services.AssetSummaryService
    response = asset_summary_service.api_asset_summary_generate_service(request)
    return jsonify(response), response.get("code")
except BusinessException as e:
    # 特定的业务逻辑异常处理
    logs.setup_logger().error(f"业务错误: {str(e)}")
    return jsonify({"code": e.error_code, "msg": str(e)})
    
"""
