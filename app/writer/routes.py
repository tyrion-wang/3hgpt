from flask import render_template, request
from app.writer import bp
from app.flask_gpt import chat_manager
import flask
from app import flask_gpt

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('writer/index.html')

@bp.route('/returnMessage', methods=['GET', 'POST'])
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
    generate = flask_gpt.handle_messages_get_response_stream(send_message, messages_history, 12,
                                                   chat_with_history)
    return flask.Response(generate(), mimetype='text/event-stream')

