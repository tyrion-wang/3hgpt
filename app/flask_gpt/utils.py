from .config import CHAT_CONTEXT_NUMBER_MAX
from .config import STREAM_FLAG
from .config import API_KEY
import openai
from flask import request
import flask
from flask import current_app as app
def get_message_context(message_history, have_chat_context, chat_with_history):
    """
    获取上下文
    :param message_history:
    :param have_chat_context:
    :param chat_with_history:
    :return:
    """
    message_context = []
    total = 0
    if chat_with_history:
        num = min([len(message_history), CHAT_CONTEXT_NUMBER_MAX, have_chat_context])
        # 获取所有有效聊天记录
        valid_start = 0
        valid_num = 0
        for i in range(len(message_history) - 1, -1, -1):
            message = message_history[i]
            if message['role'] in {'assistant', 'user'}:
                valid_start = i
                valid_num += 1
            if valid_num >= num:
                break

        for i in range(valid_start, len(message_history)):
            message = message_history[i]
            if message['role'] in {'assistant', 'user'}:
                message_context.append(message)
                total += len(message['content'])
    else:
        message_context.append(message_history[-1])
        total += len(message_history[-1]['content'])

    # print(f"len(message_context): {len(message_context)} total: {total}", )
    return message_context

def get_response_stream_generate_from_ChatGPT_API_V2(message_context):
    """
    从ChatGPT API获取回复
    :param apikey:
    :param message_context: 上下文
    :return: 回复
    """
    print("1231231312")
    def stream():
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=message_context,
            stream=True)
        for line in completion:
            if line['choices'][0]['finish_reason'] is not None:
                chunk = '[DONE]'
            else:
                chunk = line['choices'][0].get('delta', {}).get('content', '')
            if chunk:
                print(chunk)
                yield 'event: delta\ndata: %s\n\n' % chunk
                # yield "{'event: delta\n\n, 'data: %s\n\n' % chunk}";
    return stream

def get_response_from_ChatGPT_API_V2(message_context):
    """
    从ChatGPT API获取回复
    :param message_context: 上下文
    :return: 回复
    """
    def stream():
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # temperature=temperature,
            stream=False,
            messages=message_context
        )
        # 判断是否含 choices[0].message.content
        if "choices" in response \
                and len(response["choices"]) > 0 \
                and "message" in response["choices"][0] \
                and "content" in response["choices"][0]["message"]:
            yield 'data: %s\n\n' % response["choices"][0]["message"]["content"]
            yield 'data: [DONE]\n\n'
        else:
            yield 'data: %s\n\n' % str(response)
    return stream

def handle_messages_get_response(message, message_history, have_chat_context, chat_with_history):
    """
    处理用户发送的消息，获取回复
    :param message: 用户发送的消息
    :param apikey:
    :param message_history: 消息历史
    :param have_chat_context: 已发送消息数量上下文(从重置为连续对话开始)
    :param chat_with_history: 是否连续对话
    """
    message_history.append({"role": "user", "content": message})
    message_context = get_message_context(message_history, have_chat_context, chat_with_history)
    response = get_response_from_ChatGPT_API_V2(message_context)
    print(response)
    return response


def handle_messages_get_response_stream(message, message_history, have_chat_context, chat_with_history):
    message_history.append({"role": "user", "content": message})
    message_context = get_message_context(message_history, have_chat_context, chat_with_history)
    generate = get_response_stream_generate_from_ChatGPT_API_V2(message_context)
    return generate


# @app.route('/returnMessage', methods=['GET', 'POST'])
def return_message():
    """
    获取用户发送的消息，调用get_chat_response()获取回复，返回回复，用于更新聊天框
    :return:
    """
    send_message = ""
    if request.method == 'GET':
        send_message = request.values.get("send_message").strip()
    if request.method == 'POST':
        send_message = request.json["content"]

    messages_history = [{"role": "assistant", "content": "1.有2个苹果"},
                        {"role": "assistant", "content": "2.有3个梨子"},
                        {"role": "assistant", "content": "3.有2只鸡"}]
    chat_with_history = True


    if STREAM_FLAG:
        generate = handle_messages_get_response_stream(send_message, messages_history, CHAT_CONTEXT_NUMBER_MAX, chat_with_history)
        return flask.Response(generate(), mimetype='text/event-stream')
    else:
        generate = handle_messages_get_response(send_message, messages_history, CHAT_CONTEXT_NUMBER_MAX, chat_with_history)
        return flask.Response(generate(), mimetype='text/event-stream')