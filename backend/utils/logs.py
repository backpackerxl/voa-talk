import logging
import os
from datetime import datetime


class DailyFileHandler(logging.FileHandler):
    """一个日志处理程序，它每天创建一个新的日志文件。"""

    def __init__(self, dir_name, mode='a', encoding=None, delay=False):
        self.dir_name = dir_name
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        filename = self.get_filename()
        super().__init__(filename, mode, encoding, delay)

    def get_filename(self):
        """根据当前日期生成日志文件名。"""
        date_str = datetime.now().strftime("%Y/%m/%d")
        log_dir = os.path.join(self.dir_name, date_str)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, "log.log")

    def emit(self, record):
        """在写入日志记录之前，检查是否需要滚动文件。"""
        new_date = datetime.now().strftime("%Y-%m-%d")
        if new_date != self.current_date:
            self.current_date = new_date
            self.baseFilename = self.get_filename()
            self.stream = self._open()
        super().emit(record)


def setup_logger():
    """
    设置日志记录器并返回它。日志文件按年/月/日的层级结构保存。
    :return: 日志记录器。
    """
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    # 创建自定义的日志处理程序
    file_handler = DailyFileHandler("logfile", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - line %(lineno)d - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_api_module_and_description(api_name):
    # API名称映射到其模块和描述
    api_to_module = {
        "ApiUserFindListPage": ("用户管理", "平台用户分页查询"),
        "get_role": ("角色权限管理", "角色查询"),
        "get_menu": ("菜单管理", "获取菜单分页查询"),
        "api_admin_menu_deletebyids": ("菜单管理", "菜单删除"),
        "post_menu": ("菜单管理", "新增或者修改菜单"),
        "ApiSysRoleSaveOrUpdate": ("角色权限管理", "角色新增或者修改"),
        "ApiSysRoleDeleteByIds": ("角色权限管理", "角色删除"),
        "get_menu_by_role": ("角色权限管理", "根据角色获取菜单"),
        "ApiSysRoleGetRoleMenuByRoleId": ("角色权限管理", "获取角色菜单权限"),
        "ApiSysRoleSetRoleMenu": ("角色权限管理", "角色设置菜单"),
        "get_dict_domain": ("数据字典管理", "数据字典分页查询"),
        "get_dict": ("数据字典管理", "数据字典子类分页查询"),
        "save_or_update_dict": ("数据字典管理", "数据字典新增或修改"),
        "ApiSysDictDeleteByIds": ("数据字典管理", "数据字典删除"),
        "ApiUserSaveOrUpdate": ("用户管理", "添加用户"),
        "ApiUserDeleteByIds": ("用户管理", "删除用户"),
        "ApiUserResetPassword": ("用户管理", "重置密码"),
        "ApiUserUpdatePassword": ("用户管理", "修改密码"),
        "ApiSysUnitList": ("单位部门管理", "单位部门分页查询"),
        "ApiSysUnitRegionListByLevel": ("单位部门管理", "获取地区"),
        "apiAdminSysUnitUpdate": ("单位部门管理", "编辑单位"),
        "apiAdminSysUnitdelete": ("单位部门管理", "删除单位"),
        "apiAdminSysDepartmentList": ("单位部门管理", "部门查询"),
        "apiAdminSysDepartmentDelete": ("单位部门管理", "部门删除"),
        "apiAdminSysDepartmentAdd": ("单位部门管理", "部门新增"),
        "apiAdminSysDepartmentUpdate": ("单位部门管理", "部门编辑"),
        "api_admin_syslog_list": ("系统监控", "系统日志分页查询"),
        "api_bank_transaction_findListPage": ("银行流水处理", "银行流水查询"),
        "api_bank_transaction_save_or_update": ("银行流水处理", "银行流水新增"),
        "api_bank_transaction_submit": ("银行流水处理", "银行流水提交"),
        "api_bank_transaction_audit": ("银行流水处理", "银行流水审核"),
        "api_bank_transaction_export": ("银行流水处理", "银行流水导出"),
        "api_bank_transaction_update": ("银行流水处理", "银行流水编辑"),
        "api_bank_transaction_delete": ("银行流水处理", "银行流水删除"),
        "api_cash_flow_find_list_page": ("财务管理", "净现金流表分页查询"),
        "api_cash_flow_export": ("财务管理", "净现金流表导出"),
        "api_cash_flow_generate": ("财务管理", "净现金流表生成"),
        "api_bank_audit_find_list_page": ("财务管理", "银行审核表分页查询"),
        "api_bank_audit_export": ("财务管理", "银行审核表导出"),
        "api_bank_audit_audit": ("财务管理", "银行审核表审核"),
        "api_bank_account_find_list_page": ("银行账户信息", "银行账户信息表分页查询"),
        "api_bank_account_save_or_update": ("银行账户信息", "银行账户信息表新增和修改"),
        "api_accounts_bankaccount_delete": ("银行账户信息", "银行账户信息表删除"),
        "api_accounts_receivable_payable_find_list_page": ("应收应付管理", "应收应付表分页查询"),
        "api_accounts_receivable_payable_export": ("应收应付管理", "应收应付表导出"),
        "api_accounts_receivable_payable_detail_export": ("应收应付管理", "应收应付表明细导出"),
        "api_accounts_receivable_payable_generate": ("应收应付管理", "应收应付表生成"),
        "api_asset_summary_generate": ("资产管理", "资产汇总表生成"),
        "api_asset_summary_find_list_page": ("资产管理", "资产汇总表分页查询"),
        "api_asset_summary_export": ("资产管理", "资产汇总表导出"),
        "api_cash_flow_delete": ("财务管理", "净现金流表删除"),
        "api_accounts_receivable_payable_delete": ("财务管理", "应收应付表删除"),
        "api_asset_summary_delete": ("财务管理", "资产汇总表删除"),
        "api_product_profit_find_list_page": ("产品管理", "产品利润表分页查询"),
        "api_product_find_list_page": ("产品管理", "产品表分页查询"),
        "api_product_save_or_update": ("产品管理", "产品表新增或者修改"),
        "api_investment_profit_find_list_page": ("产品管理", "投资利润汇总表分页查询"),
        "api_investment_profit_delete": ("产品管理", "投资利润汇总表删除"),
        "api_product_profit_save_or_update": ("产品管理", "产品利润表新增或者修改"),
        "api_product_delete": ("产品管理", "产品表删除"),
        "api_productprofit_export": ("产品管理", "投资利润表导出"),
        "api_upload": ("其他", "图片上传"),
    }

    # 返回API名称对应的模块和描述
    return api_to_module.get(api_name, ("未知模块", "未知描述"))


if __name__ == '__main__':
    # 测试函数
    api_name = "api_asset_summary_find_list_page"
    module, description = get_api_module_and_description(api_name)
    print(f"模块: {module}, 描述: {description}")