import gradio as gr
import pandas as pd
import os
import time
import uuid
from main import Chatbot as AI

ai = AI()

# Tạo thư mục lưu lịch sử nếu chưa có
if not os.path.exists("chat_logs"):
    os.makedirs("chat_logs")

def generate_session_id():
    """Tạo ID phiên làm việc dựa trên timestamp + UUID"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6]  # Lấy 6 ký tự từ UUID ngẫu nhiên
    return f"{timestamp}_{unique_id}"

def save_to_csv(user_message, bot_response, session_id):
    """Lưu hội thoại vào file CSV riêng theo session ID"""
    file_path = f"chat_logs/chat_{session_id}.csv"
    
    new_data = pd.DataFrame([[user_message, bot_response]], columns=["User", "Bot"])

    # Ghi dữ liệu vào file CSV, không ghi đè dữ liệu cũ
    new_data.to_csv(file_path, mode="a", index=False, header=not os.path.exists(file_path), encoding="utf-8")

def chatbot_response(message, history, session_id):
    """
    Xử lý tin nhắn chatbot và lưu vào file hội thoại riêng (CSV).
    """
    his = ""
    for m, r in history[::-1]:
        his = "SIUBOT:" + "\n" + r  + "\n" +  his
        his = "USER: " + "\n" + m + "\n" + his + "\n"
        if len(his) > 8000:
            break

    inp = f"""
# Hội thoại 
{his}

# Tin nhắn hiện tại :
USER: {message}
"""
    response, debug_info = ai.respond(inp)
    
    # Lưu vào file CSV riêng theo session ID
    save_to_csv(message, response, session_id)

    history = history + [(message, response)]
    return "", history, debug_info, history  # Trả về lịch sử mới để cập nhật state

def initialize_session():
    """Chỉ tạo session ID khi mở giao diện, không có tin nhắn chào"""
    return "", generate_session_id()  # Trả về session ID

css = '''
.info {text-align: center; font-size: 5em; !important}
'''

with gr.Blocks(theme=gr.themes.Soft(), css = css) as demo:
    chatbot = gr.Chatbot(height=500, elem_classes="info")

    msg = gr.Textbox(label="Nhập tin nhắn")
    submit_btn = gr.Button("Gửi")
    debug_output = gr.Textbox(label="Thông tin xử lý")
    state = gr.State([])  # Lưu lịch sử hội thoại
    session_id = gr.State("")  # Khởi tạo session ID rỗng

    def on_submit(message, history, session_id):
        return chatbot_response(message, history, session_id)

    # Khi mở giao diện, bot nhắn trước và tạo session ID
    demo.load(initialize_session, inputs=[], outputs=[debug_output, session_id])

    submit_btn.click(on_submit, inputs=[msg, state, session_id], outputs=[msg, chatbot, debug_output, state])
    msg.submit(on_submit, inputs=[msg, state, session_id], outputs=[msg, chatbot, debug_output, state])

demo.launch(share=True)
