from services.impl import sys_report_impl


def header_data():
    return sys_report_impl.header_data()


def top_talk():
    return sys_report_impl.top_talk()


def bar_talks(request):
    stm = request.args.get('stm')
    etm = request.args.get('etm')
    return sys_report_impl.bar_talks(stm, etm)


def model_talks(request):
    """
    饼图数据
    """
    stm = request.args.get('stm')
    etm = request.args.get('etm')
    return sys_report_impl.model_talks(stm, etm)


def line_tokens(request):
    """
    折线图数据
    """
    stm = request.args.get('stm')
    etm = request.args.get('etm')
    return sys_report_impl.line_tokens(stm, etm)
