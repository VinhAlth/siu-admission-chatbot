from search import HiData
from decomposer import Decomposer

from search_path_try_nhifixed import VaultBrowser
func = VaultBrowser("/workspace/vinhnq/NCKH2025/LLM_phancap/data/Thông tin tuyển sinh trên trang SIU")

import ast
import re

class Chatbot:
    def __init__(self):
        self.decompose = Decomposer()
        self.chatbot = HiData()

    def respond(self, ques):
        out = ""
        self.decompose.clearHis()
        count = 0
        while True:
            
            respond = self.decompose.search(ques)
            print(self.decompose.history1())
            try: 
                print("-"*60)
                print("Lần:", count)
                print("-"*60)
                if count!=0:
                    match = re.search(r'\{.*\}', respond, re.DOTALL)
                    result = match.group(0) 
                    queses = ast.literal_eval(result)
                    for k, v in queses.items():
                        out += f"Câu hỏi: {k}, Đường dẫn chứa thông tin của câu hỏi: {v}\n"
                else:
                    match = re.search(r'\{.*\}', respond, re.DOTALL)
                    result = match.group(0) 
                    queses = ast.literal_eval(result)
                    for k, v in queses.items():
                        out += f"Câu hỏi: {k}, Đường dẫn chứa thông tin của câu hỏi: {v}\n"
                break
            except:
                count+=1
                if count==3:
                    
                    print("-"*60)
                    print("Lỗi")
                    print("-"*60)
                    out = f"""
Tự tìm kiếm thông tin ở dữ liệu phân cấp dưới

{func.browse_vault("start")}
"""
                    break
                pass

        out1 = f"""
# GỢI Ý TÌM KIẾM THÔNG TIN
{out}

- Bắt buộc dùng hàm func.browse_vault trước khi phản hồi

{ques}

# PHẢN HỒI
"""
               
        respond = self.chatbot.search(out1)
        return respond, self.chatbot.history1()