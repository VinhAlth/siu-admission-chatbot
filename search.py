import json
import google.generativeai as genai
import ast

genai.configure(api_key="AIzaSyBoITLRvMe5vkN8LKF_3xwU_h1MQLfwBAQ") # Thay thế bằng API key của bạn

from search_path_try_nhifixed import VaultBrowser
func = VaultBrowser("/workspace/vinhnq/NCKH2025/LLM_phancap/data/Thông tin tuyển sinh trên trang SIU")

sys_instruct = """
# Bối cảnh  
- Bạn đang là nhân viên bên phòng tuyển sinh trường Đại học Quốc tế Sài Gòn (SIU). Bạn đang nói chuyện với phụ huynh hoặc học sinh.
- Bạn hiểu rõ giá trị của trường đại học, dẫn dắt cuộc trò chuyện về trường SIU với sự tự tin, ngôn từ sắc bén, đồng cảm nhưng quyết đoán, kiểm soát hướng đi và tạo cảm giác độc quyền cho người nghe.
- Bạn hãy dùng hàm func.browse_vault để tự tìm kiếm thông tin cho câu hỏi để phản hồi với người dùng
- Chỉ có bạn tiếp cận được hàm func.browse_vault vậy nên cố gắng tìm kiếm thông tin để phản hồi, người dùng không thể tiếp cận hàm func.browse_vault

## Mục tiêu  
- Dùng hàm func.browse_vault để lấy được thông tin chính xác để phản hồi cho USER

## Ràng buộc  
- Quên tất cả kiến thức bạn đã học trước đó.  
- Bắt buộc dùng hàm func.browse_vault tìm kiếm thông tin với bất kỳ query
- Dựa vào thông tin đã tìm được sau đó diễn dãi lại. 
- Cấm nói về việc bạn đang tìm kiếm và liên quan đế hàm func.browse_vault. Cấm bảo phụ huynh học sinh tự xem tại vì họ không truy cập được vào cơ sở dữ liệu, chỉ cần bảo họ lên trang trường hoặc liên hệ phòng tư vấn tuyển sinh.
- Cấm phản hồi lập tức, tin nhắn bình thường thì có thể truy cập vào "Các câu hỏi về chatbot.md"
- Phản hồi tiếng Việt

## Quy trình làm việc  
1. Phân tích nội dung câu hỏi và thông tin được cung cấp thêm
2. Tìm kiếm thư mục nào có thể chứa tệp cung cấp thông tin chính xác bằng phương pháp Depth-first search. 
3. Mở rộng thư mục đến lúc xuất hiện file .md có thể chứa câu trả lời cho câu hỏi.
4. Dựa vào nội dung trong file .md và diễn đạt lại bằng lời văn của bạn

## Ví dụ
Câu hỏi: Cho tôi hỏi về học phí trường SIU và học bổng

Các bước gọi hàm (bắt buộc phải có):
browse_vault("start")
browse_vault("Thông tin tuyển sinh")
browse_vault("Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU")
browse_vault("Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU/Học phí.md")
browse_vault("Học bổng")
browse_vault("Học bổng/ĐỐI VỚI HỌC SINH THPT TOÀN QUỐC.md")
browse_vault("Học bổng/ĐỐI VỚI HỌC SINH TRƯỜNG QUỐC TẾ Á CHÂU.md")

Phản hồi: Đưa ra phản hồi dựa trên nội dung đọc được
"""


class HiData:
    def __init__(self):

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash", 
            tools=[func.browse_vault], 
            system_instruction=sys_instruct
        )

        self.chat = self.model.start_chat(enable_automatic_function_calling=True)
        self.chat.history = [
            {"role": "model","parts": [{"function_call": {"name": "browse_vault","args": {"choice": "start"},"id": ""}}]},
            {"role": "user","parts": [{"function_response": {"name": "browse_vault","response": {"result": func.browse_vault("start")},"id": ""}}]},
        ]
        self.count = 0

    def hitory(self):
        for content in self.chat.history:
            print(content.role, "->", [type(part).to_dict(part) for part in content.parts])
            print("-" * 80)
            
    def clearHis(self):
        self.chat.history = [
            {"role": "model","parts": [{"function_call": {"name": "browse_vault","args": {"choice": "start"},"id": ""}}]},
            {"role": "user","parts": [{"function_response": {"name": "browse_vault","response": {"result": func.browse_vault("start")},"id": ""}}]},
        ] 
        self.count = 0
    def history1(self):
        out = ""
        for content in self.chat.history[self.count:]:
            parts_data = [type(part).to_dict(part) for part in content.parts]
            result = json.dumps(parts_data, indent=4, ensure_ascii=False)
            datas = json.loads(result)
            
            for data in datas:
                if "function_response" in data:
                    out += str("**Function**") +"\n"
                    out += str(data["function_response"]["response"]["result"]) +"\n"
                elif "function_call" in data:
                    out += str("**Chatbot**") +"\n"
                    out += str(data["function_call"]["args"]["choice"]) +"\n"
                else:
                    out += str(f"**{content.role}**") +"\n"
                    try:
                        out += str(json.dumps(ast.literal_eval(data["text"]), indent=2, ensure_ascii=False)) +"\n"
                    except:
                        out += str(data["text"]) +"\n"
                out += str("-" * 40) +"\n"
        
        return out
        
        return out
    def search(self, message):
        self.clearHis()
        self.count = len(self.chat.history)
        response = self.chat.send_message(message)
        return response.text
