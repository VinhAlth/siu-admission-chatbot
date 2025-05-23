import json
import ast
import google.generativeai as genai
genai.configure(api_key="AIzaSyBibb3-lZp0xz3UZOl_ntApPRQTtjCzZNw") # Thay thế bằng API key của bạn

from search_path_try_nhifixed import VaultBrowser
func = VaultBrowser("/workspace/vinhnq/NCKH2025/LLM_phancap/data/Thông tin tuyển sinh trên trang SIU")

sys_instruct = """
Bạn luôn luôn dùng hàm func.browse_vault để tự tìm kiếm nội dung, cấm trả lời vội

## Bối cảnh  
- Bạn là nhân viên trường đại học Trường Đại học Tư thục Quốc tế Sài Gòn (SIU)
- Bạn rất giỏi trong việc tìm kiếm tài liệu về trường để trả lời cho câu hỏi bằng hàm func.browse_vault
- Bạn là giỏi trong việc phân tích vấn đề và chia nhỏ các vấn đề khó thành các vấn đề đơn giản.
- Bạn hãy dùng hàm func.browse_vault để tự tìm kiếm thông tin cho câu hỏi để chia nhỏ câu hỏi
- Phản hồi bắt buộc trả về từ điển Dict[Question: str, Path: str] là câu hỏi đơn giản và đường dẫn có câu trả lời cho câu hỏi đó, không phải là câu trả lời

## Mục tiêu  
- Giúp người dùng phân tách câu hỏi phức tạp thành câu hỏi con đơn giản.
- Dùng hàm func.browse_vault giúp người dùng tìm đường dẫn chính xác trả lời cho câu hỏi chính 

## Ràng buộc  
- Quên tất cả kiến thức bạn đã học trước đó.  
- Phản hồi bắt buộc trả về từ điển Dict[Question: str, Path: str] là câu hỏi con có thể trả lời với thông tin trong tệp .md và đường dẫn tới file .md có câu trả lời cho câu hỏi đó
- Bắt buộc phản hồi file .md, cảm trả về folder.

## Quy trình làm việc  
1. Phân tích câu hỏi phức tạp ban đầu.
2. Tìm kiếm thư mục nào có thể chứa tệp cung cấp thông tin chính xác bằng phương pháp Depth-first search. 
3. Mở rộng thư mục đến lúc xuất hiện file .md có thể chứa câu trả lời cho câu hỏi.
4. Phản hồi bắt buộc trả về định dạng Dict[Question: str, Path: str] là câu hỏi đơn giản kèm với đường dẫn file .md chứa câu trả lời cho câu hỏi

## Lưu ý
- Cấm phản hồi bất cứ điều gì, chỉ trả về Dict[Question: str, Path: str]
- Cấm trả về đường dẫn folder, luôn trả về đường dẫn file .md ở bên trong thư mục

## Ví dụ
Câu hỏi: Cho tôi hỏi về học phí trường SIU và học bổng

Các bước gọi hàm:
browse_vault("Thông tin tuyển sinh")
browse_vault("Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU")
browse_vault("Học bổng")
browse_vault("Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU/Học phí.md")
browse_vault("Học bổng/ĐỐI VỚI HỌC SINH THPT TOÀN QUỐC.md")
browse_vault("Học bổng/ĐỐI VỚI HỌC SINH TRƯỜNG QUỐC TẾ Á CHÂU.md")

Phản hồi:
\"\"\"
\{
    "Học phí trường SIU": "Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU/Học phí.md", 
    "Học bổng đối với học sinh THPT toàn quốc": "Học bổng/ĐỐI VỚI HỌC SINH THPT TOÀN QUỐC.md", 
    "Học bổng đối với học sinh trường quốc tế Á Châu": "Học bổng/ĐỐI VỚI HỌC SINH TRƯỜNG QUỐC TẾ Á CHÂU.md"
\}
\"\"\"
"""

class Decomposer:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash", 
            tools=[func.browse_vault], 
            system_instruction=sys_instruct,
        )

        self.chat = self.model.start_chat(enable_automatic_function_calling=True)
        self.chat.history = [
            {"role": "user","parts": [{"text": "Xin chào"}]},
            {"role": "model","parts": [{"function_call": {"name": "browse_vault","args": {"choice": "start"},"id": ""}}]},
            {"role": "user","parts": [{"function_response": {"name": "browse_vault","response": {"result": func.browse_vault("start")},"id": ""}}]},
            {"role": "model","parts": [{"text": "{\"Xin chào\": \"Các câu hỏi về chatbot và câu hỏi ngoài lề.md\"}"}]},
            {"role": "user","parts": [{"text": "Nộp hồ sơ vào trường như thế nào?"}]},
            {"role": "model","parts": [{"function_call": {"name": "browse_vault","args": {"choice": "start"},"id": ""}}]},
            {"role": "user","parts": [{"function_response": {"name": "browse_vault","response": {"result": func.browse_vault("start")},"id": ""}}]},
            {"role": "model","parts": [{"function_call": {"name": "browse_vault","args": {"choice": "Thông tin tuyển sinh"},"id": ""}}]},
            {"role": "user","parts": [{"function_response": {"name": "browse_vault","response": {"result": func.browse_vault("Thông tin tuyển sinh")},"id": ""}}]},
            {"role": "model","parts": [{"function_call": {"name": "browse_vault","args": {"choice": 'Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU'},"id": ""}}]},
            {"role": "user","parts": [{"function_response": {"name": "browse_vault","response": {"result": func.browse_vault('Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU')},"id": ""}}]},
            {"role": "model","parts": [{"text": "{\"Trường SIU có những phương thức xét tuyển nào?\": \"Thông tin tuyển sinh/Các phương thức xét tuyển\", \"Hồ sơ xét tuyển gồm những gì?\": \"Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU/\", \"Thời gian xét tuyển của trường SIU là khi nào?\": \"Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU/Thời gian xét tuyển.md\", \"Lệ phí xét tuyển của trường SIU là bao nhiêu?\": \"Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU/Lệ phí xét tuyển 2024.md\"}"}]}
        ]
        self.count = len(self.chat.history)
        self.respond = ""
    def clearHis(self):
        self.chat.history = [
            {"role": "user","parts": [{"text": "Xin chào"}]},
            {"role": "model","parts": [{"function_call": {"name": "browse_vault","args": {"choice": "start"},"id": ""}}]},
            {"role": "user","parts": [{"function_response": {"name": "browse_vault","response": {"result": func.browse_vault("start")},"id": ""}}]},
            {"role": "model","parts": [{"text": "{\"Xin chào\": \"Các câu hỏi về chatbot và câu hỏi ngoài lề.md\"}"}]},
            {"role": "user","parts": [{"text": "Nộp hồ sơ vào trường như thế nào?"}]},
            {"role": "model","parts": [{"function_call": {"name": "browse_vault","args": {"choice": "start"},"id": ""}}]},
            {"role": "user","parts": [{"function_response": {"name": "browse_vault","response": {"result": func.browse_vault("start")},"id": ""}}]},
            {"role": "model","parts": [{"function_call": {"name": "browse_vault","args": {"choice": "Thông tin tuyển sinh"},"id": ""}}]},
            {"role": "user","parts": [{"function_response": {"name": "browse_vault","response": {"result": func.browse_vault("Thông tin tuyển sinh")},"id": ""}}]},
            {"role": "model","parts": [{"function_call": {"name": "browse_vault","args": {"choice": 'Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU'},"id": ""}}]},
            {"role": "user","parts": [{"function_response": {"name": "browse_vault","response": {"result": func.browse_vault('Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU')},"id": ""}}]},
            {"role": "model","parts": [{"text": "{\"Trường SIU có những phương thức xét tuyển nào?\": \"Thông tin tuyển sinh/Các phương thức xét tuyển\", \"Hồ sơ xét tuyển gồm những gì?\": \"Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU/\", \"Thời gian xét tuyển của trường SIU là khi nào?\": \"Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU/Thời gian xét tuyển.md\", \"Lệ phí xét tuyển của trường SIU là bao nhiêu?\": \"Thông tin tuyển sinh/thông tin đăng ký, nộp hồ sơ và xét tuyển vào trường SIU/Lệ phí xét tuyển 2024.md\"}"}]}
        ]
        self.count = len(self.chat.history)
    def hitory(self):
        for content in self.chat.history:
            parts_data = [type(part).to_dict(part) for part in content.parts]
            print(content.role, "->", json.dumps(parts_data, indent=4, ensure_ascii=False))
            print("-" * 80)
    def history1(self):
        out = ""
        for content in self.chat.history[self.count:]:
            parts_data = [type(part).to_dict(part) for part in content.parts]
            result = json.dumps(parts_data, indent=4, ensure_ascii=False)
            data = json.loads(result)
            
            if "function_response" in data[0]:
                out += str("**Function**") +"\n"
                out += str(data[0]["function_response"]["response"]["result"]) +"\n"
            elif "function_call" in data[0]:
                out += str("**Chatbot**") +"\n"
                out += str(data[0]["function_call"]["args"]["choice"]) +"\n"
            else:
                out += str(f"**{content.role}**") +"\n"
                try:
                    out += str(json.dumps(ast.literal_eval(data[0]["text"]), indent=2, ensure_ascii=False)) +"\n"
                except:
                    out += str(data[0]["text"]) +"\n"
            out += str("-" * 40) +"\n"
        
        return out
                
    def search(self, message):
        self.count = len(self.chat.history)
        self.response = self.chat.send_message(message)
        return self.response.text
