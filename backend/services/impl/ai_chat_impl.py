import datetime
import json
import time
import random
import string

from flask import Response
from openai import OpenAI

from dbinfo import DatabaseSession
from entity import ModelConfig, TalkUserRelation, TalkLogs, RequestLogs, TalkRecommendation
from utils import ReturnTool, DbTools, Tools
from utils.RedisUtils import RedisHandler
from utils.GetChatId import Snowflake

clientDict = {}

snowflake = Snowflake(data_center_id=1, worker_id=3)

snowflake_share = Snowflake(data_center_id=2, worker_id=6)


def getClient(model_cfg):
    if model_cfg.model_id in clientDict.keys():
        return clientDict[model_cfg.model_id]
    else:
        client = OpenAI(
            # 此为默认路径，您可根据业务所在地域进行配置
            base_url=model_cfg.req_url,
            # 从环境变量中获取您的 API Key
            api_key=model_cfg.api_key,
        )
        clientDict[model_cfg.model_id] = client
        return client


def generateContent(inputs, model_cfg):
    # 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
    # 初始化Openai客户端，从环境变量中读取您的API Key
    client = getClient(model_cfg)
    # Streaming:
    completion = client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model=model_cfg.model_id,
        messages=inputs,
    )
    return completion.choices[0].message.content


def ai_chat_dialogue_impl(session_id, user_input, model_id):
    """
    :param session_id: 对话ID
    :param user_input: 用户输入
    :param model_id: 模型ID
    :return:
    """
    if session_id == -1:
        session_id = snowflake.next_id()
    with DatabaseSession() as session:

        model_cfg = session.query(ModelConfig).filter(ModelConfig.id == model_id).first()
        if model_cfg is None:
            return ReturnTool.ErrorReturn("模型不存在")

        def generate():
            # 请确保您已将 API Key 存储在数据库中
            # 初始化Openai客户端，从数据库中中读取您的API Key
            client = getClient(model_cfg)
            # Streaming:
            stream = client.chat.completions.create(
                # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
                model=model_cfg.model_id,
                messages=[
                    {"role": "user", "content": user_input},
                ],
                # 响应内容是否流式返回
                stream=True,
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                res_dict = {
                    "model_id": model_cfg.model_id,
                    "model_name": model_cfg.name,
                    "session_id": session_id,
                    "content": chunk.choices[0].delta.content
                }
                resp_json = json.dumps(res_dict, ensure_ascii=False)
                yield f"data: {resp_json}\n\n"  # 遵循 Server-Sent Events 协议

        # 添加缓存控制头
        return Response(generate(), mimetype='text/event-stream')


def ai_save_chat_serve(user_id, request_data):
    """
        配置新增或编辑
    """
    with DatabaseSession() as session:
        # 使用 saveOrUpdate 函数
        now = datetime.datetime.fromtimestamp(time.time())
        if request_data.get('id') is None:
            request_data['create_date'] = now
        result = DbTools.saveOrUpdate(session, request_data, TalkLogs)
        save_dict = {
            "model_id": request_data['model_id'],
            "user_id": user_id,
            "create_date": now
        }
        DbTools.saveOrUpdate(session, save_dict, RequestLogs)

        if result:
            model_cfg = session.query(ModelConfig).filter(ModelConfig.id == request_data['model_id']).first()
            return ReturnTool.SuccessReturn(gen_record_list(result.id, request_data, model_cfg))
        else:
            return ReturnTool.ErrorReturn('数据没有找到')


def gen_record_list(chat_id, request_data, model_cfg):
    reco_list = []
    with DatabaseSession() as session:
        if model_cfg is not None:
            resp_rec = generateContent([
                {"role": "user", "content": request_data['req_content']},
                {"role": "system", "content": request_data['resp_content']},
                {"role": "user", "content": '''
                                                            1.要求根据这段上下文生成3个推荐问题
                                                            2.要求只提炼出三个推荐问题
                                                            3.要求推荐问题不超过20个字
                                                            4.要求只返回问题本身的纯文本不要带任何markdown语法格式的字符
                                                            5.要求站在你的角度考虑，推荐一些你比较擅长的相似问题
                                                            6.要求内容不要返回序号
                                                            7.要求请记住最终结果只需要三个，并且每个问题的字数不超过20个字
                                                            8.要求每个问题之间用英文的;分割
                                                            9.要求认真思考，不要生成一些奇怪的问题
                                                            10.要求每个问题最后一个字符不能是特殊的中文或英文符号
                                                            '''},
            ], model_cfg)
            arr = []
            if ';' in resp_rec:
                arr = resp_rec.split(";")[:3]
            if '；' in resp_rec and len(arr) == 0:
                arr = resp_rec.split("；")[:3]
            if '\n' in resp_rec and len(arr) == 0:
                arr = resp_rec.split("\n")[:3]
            if len(arr) != 0:
                talk_id = int(request_data['talk_id'])
                session.query(TalkRecommendation).filter(TalkRecommendation.talk_id == talk_id).delete()
                session.commit()
                reco_list = [{"talk_id": talk_id, "content": content[:20]} for content in
                             arr]
            DbTools.bulk_insert(session, reco_list, TalkRecommendation)
    return {
        "chat_id": chat_id,
        "reco_list": reco_list
    }


def save_chat_title(user_id, nick_name, user_input, model_id, request_data):
    """
        配置新增或编辑
    """
    with DatabaseSession() as session:
        # 使用 saveOrUpdate 函数
        model_cfg = session.query(ModelConfig).filter(ModelConfig.id == model_id).first()
        if model_cfg is None:
            return ReturnTool.ErrorReturn("模型不存在")
        now = datetime.datetime.fromtimestamp(time.time())
        if request_data.get('id') is None:
            request_data['create_date'] = now

        request_data['user_id'] = user_id
        request_data['nick_name'] = nick_name
        request_data['talk_name'] = generateContent([
            {"role": "user",
             "content": user_input + "\n" + "给这段内容取一个恰当的标题1.只返回最好的一个标题2.不要特殊符号只要纯文字3.不要超过20个字"},
        ], model_cfg)
        result = DbTools.saveOrUpdate(session, request_data, TalkUserRelation)
        if result:
            return ReturnTool.SuccessReturn({
                'title': request_data['talk_name'],
                'id': request_data['talk_id']
            })
        else:
            return ReturnTool.ErrorReturn('数据没有找到')


def api_list_impl(search_criteria, page_size, page_index):
    with DatabaseSession() as session:
        query = session.query(TalkUserRelation)
        # 使用公用方法动态添加搜索条件
        query = DbTools.apply_filters(query, TalkUserRelation, search_criteria)
        # 根据需要应用过滤器
        data = DbTools.find_list_page(query, page_size, page_index)
        # data = data['records']
        # data = [{"id": mc['talk_id'], "title": mc['talk_name']} for mc in data]
        return ReturnTool.SuccessReturn(data)


def one_chat(search_criteria):
    with DatabaseSession() as session:
        query = session.query(TalkLogs)
        # 使用公用方法动态添加搜索条件
        query = DbTools.apply_filters(query, TalkLogs, search_criteria)
        # 根据需要应用过滤器
        data = DbTools.queryAll(query)
        arr = []
        for mc in data:
            arr.append({"id": mc['id'], "type": 'user', "content": mc['req_content']})
            arr.append({"id": mc['id'], "type": 'bot', "content": mc['resp_content']})

        return ReturnTool.SuccessReturn(arr)


def api_delete_ids_impl(ids):
    """
    删除对话
    """
    id_list = ids.split(',')
    with DatabaseSession() as session:
        session.query(TalkLogs).filter(TalkLogs.talk_id.in_(id_list)).delete()
        session.query(TalkUserRelation).filter(TalkUserRelation.talk_id.in_(id_list)).delete()
        session.query(TalkRecommendation).filter(TalkRecommendation.talk_id.in_(id_list)).delete()
        session.commit()
        return ReturnTool.SuccessReturn()


def api_update_ids(talk_id, request_data):
    """
    配置新增或编辑
    """
    with DatabaseSession() as session:
        # 使用 saveOrUpdate 函数
        if request_data.get('talk_id') is None:
            return ReturnTool.ErrorReturn("数据没有找到")

        talk_user = session.query(TalkUserRelation).filter(TalkUserRelation.talk_id == talk_id).first()
        if talk_user is None:
            return ReturnTool.ErrorReturn("数据没有找到")

        request_data['id'] = talk_user.id
        result = DbTools.saveOrUpdate(session, request_data, TalkUserRelation)
        if result:
            return ReturnTool.SuccessReturn()
        else:
            return ReturnTool.ErrorReturn('数据没有找到')


def api_query_list_page_impl(page_size, page_index, search_criteria):
    with DatabaseSession() as session:
        query = session.query(TalkUserRelation)
        # 使用公用方法动态添加搜索条件
        query = DbTools.apply_filters(query, TalkUserRelation, search_criteria)
        # 根据需要应用过滤器
        paginated_data = DbTools.find_list_page(query, page_size, page_index)
        return ReturnTool.SuccessReturn(paginated_data)


def api_find_talk_name(talk_id):
    with DatabaseSession() as session:
        talk_user = session.query(TalkUserRelation).filter(TalkUserRelation.talk_id == talk_id).first()
        if talk_user is None:
            return ReturnTool.SuccessReturn("数据没有找到")

        return ReturnTool.SuccessReturn(talk_user.talk_name)


def api_find_talk_recommend(talk_id):
    with DatabaseSession() as session:
        talk_recommend = session.query(TalkRecommendation).filter(TalkRecommendation.talk_id == talk_id).all()
        if talk_recommend is None or len(talk_recommend) == 0:
            log = session.query(TalkLogs).order_by(getattr(TalkLogs, 'id').desc()).filter(
                TalkLogs.talk_id == talk_id).first()
            if log is None:
                return ReturnTool.SuccessReturn({
                    "chat_id": -1,
                    "reco_list": []
                })
            model_cfg = session.query(ModelConfig).order_by(getattr(ModelConfig, 'sort').desc()).first()
            resp_dict = gen_record_list(log.id, {
                "req_content": log.req_content,
                "resp_content": log.resp_content,
                "talk_id": log.talk_id
            }, model_cfg)
            return ReturnTool.SuccessReturn(resp_dict)
        return ReturnTool.SuccessReturn({
            "chat_id": -1,
            "reco_list": [{'talk_id': result.talk_id, 'content': result.content} for result in talk_recommend]
        })


def api_del_chat_impl(id_c):
    """
        删除单次对话
    """
    with DatabaseSession() as session:
        talk_log = session.query(TalkLogs).filter(TalkLogs.id == id_c).first()
        if talk_log is None:
            return ReturnTool.ErrorReturn("未找到此对话!")
        log = session.query(TalkLogs).order_by(getattr(TalkLogs, 'id').desc()).filter(
            TalkLogs.talk_id == talk_log.talk_id).first()
        # 先判断是否删除推荐问题
        if log.id == talk_log.id:
            session.query(TalkRecommendation).filter(TalkRecommendation.talk_id == talk_log.talk_id).delete()
        session.query(TalkLogs).filter(TalkLogs.id == id_c).delete()
        session.commit()
        talk_recommend = session.query(TalkRecommendation).filter(TalkRecommendation.talk_id == talk_log.talk_id).all()
        return ReturnTool.SuccessReturn({
            "chat_id": -1,
            "reco_list": [{'talk_id': result.talk_id, 'content': result.content} for result in talk_recommend]
        })


def share_chat_impl(params):
    with DatabaseSession() as session:
        talk_log = session.query(TalkLogs).filter(TalkLogs.id == params['ids'][0]).first()
        if talk_log is None:
            return ReturnTool.ErrorReturn("未找到此对话,链接生成失败！")

        talk_user = session.query(TalkUserRelation).filter(TalkUserRelation.talk_id == talk_log.talk_id).first()
        s_id = Tools.insert_lowercase_letters(str(snowflake_share.next_id()))
        params['share_time'] = datetime.datetime.now().strftime("%Y 年 %m 月 %d 日")
        params['title'] = talk_user.talk_name
        RedisHandler().save_key(s_id, json.dumps(params), 60 * 60 * 24)  # 链接24H保活
        return ReturnTool.SuccessReturn({
            "share_id": s_id,
        })


def get_redis_chat(r_id):
    res_str = RedisHandler().get_key(r_id)
    if res_str is None:
        return ReturnTool.ErrorReturn("无效链接！")
    res_dict = json.loads(res_str)

    with DatabaseSession() as session:
        talk_logs = session.query(TalkLogs).filter(TalkLogs.id.in_(res_dict['ids'])).all()

        arr = []
        for mc in talk_logs:
            arr.append({"id": mc.id, "type": 'user', "content": mc.req_content})
            arr.append({"id": mc.id, "type": 'bot', "content": mc.resp_content})
        res_dict['talk_logs'] = arr
        return ReturnTool.SuccessReturn(res_dict)
