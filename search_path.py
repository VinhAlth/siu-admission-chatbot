import sys
from pathlib import Path
import os


class VaultBrowser:
    def __init__(self, base_path: Path):
        self.out = []
        self.expanded_paths = set()
        self.base_path = Path(base_path)

    def list_directory_contents(self, path: Path) -> list:
        """Liệt kê nội dung của thư mục, sắp xếp theo tên."""
        try:
            contents = sorted(path.iterdir(), key=lambda p: p.name.lower())
            result = []
            for item in contents:
                relative_path = item.relative_to(self.base_path).as_posix()
                result.append(relative_path)
            return result
        except FileNotFoundError:
            self.out.append(f"Lỗi: Thư mục không tồn tại - {path}")
            return []
        except PermissionError:
            self.out.append(f"Lỗi: Không đủ quyền truy cập thư mục - {path}")
            return []

    def display_tree_structure(self, current_path: Path, expanded_paths: set, prefix: str = "") -> None:
        """Hiển thị cấu trúc cây thư mục."""
        contents = self.list_directory_contents(current_path)
        total_items = len(contents)

        for index, relative_item in enumerate(contents):
            full_item_path = self.base_path / relative_item
            is_last = (index == total_items - 1)
            branch = "└── " if is_last else "├── "

            self.out.append(prefix + branch + full_item_path.name)

            if full_item_path.is_dir():
                if relative_item in expanded_paths:
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    self.display_tree_structure(full_item_path, expanded_paths, new_prefix)

    def browse_vault(self, choice: str = "") -> str:
        """
        Hàm cung cấp cấu trúc dữ liệu phân cấp
        Tên thư mục và tệp đã được thu gọn, dùng hàm để mở rộng và xem nội dung dữ liệu

        Args:
            choice (str): Đường dẫn thư mục hoặc tệp 

        Returns:
            str: Cấu trúc cây thư mục hoặc nội dung tệp dưới 
            
        Example: 
            >>> browse_vault('start')
            ├── folder1
            └── folder2
            
            >>> browse_vault('folder1')
            ├── folder1
            │   ├── subfolder1
            │   └── subfolder2
            └── folder2

            >>> browse_vault('folder1/subfolder1')
            ├── folder1
            │   ├── subfolder1
            │   │   └──file.md
            │   └── subfolder2
            └── folder2
            
            >>> browse_vault('folder/subfolder/file.md')
            Nội dung của file.md
        """
        lchoice = choice.split("/")

        for i in range(len(lchoice)):
            inp = "/".join(lchoice[:i+1])
            out = self._browse_vault(inp)
        
        return out

    
    def _browse_vault(self, choice: str = "") -> str:
        if choice == "0":
            return "Thoát chương trình."

        # Xử lý duyệt thư mục
        self.out = []
        if choice == None or choice=="start":
            self.display_tree_structure(self.base_path, self.expanded_paths)
            return "\n".join(self.out)
        
        # Xử lý việc đọc tệp markdown
        if choice.endswith(".md"):
            try:
                file_path = os.path.join(self.base_path, choice)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                return f"Nội dung tại đường dẫn: {file_path}\n\n{content}"
            except Exception:
                self.out = []
                self.display_tree_structure(self.base_path, self.expanded_paths)
                return (
                    "Đường dẫn tệp không tồn tại. Vui lòng chọn từ cây thư mục dưới đây.\n"
                    + "\n".join(self.out)
                )

        selected_path = self.base_path / choice
        if selected_path.is_dir():
            # Thu gọn các thư mục cấp cao khác nếu chọn thư mục cấp cao mới
            if "/" not in choice:
                to_remove = {
                    path for path in self.expanded_paths
                    if ("/" not in path and path != choice) or
                       ("/" in path and path.split("/")[0] != choice)
                }
                self.expanded_paths.difference_update(to_remove)

            relative_choice = selected_path.relative_to(self.base_path).as_posix()
            if relative_choice not in self.expanded_paths:
                self.expanded_paths.add(relative_choice)
            else:
                self.out.append(f"Thư mục '{choice}' đã được mở rộng trước đó.")
        else:
            self.out.append("Đường dẫn không hợp lệ hoặc không tồn tại. Vui lòng thử lại.")

        self.display_tree_structure(self.base_path, self.expanded_paths)
        return "\n".join(self.out)



def main():
    # vault_path = Path("/workspace/vinhnq/NCKH2025/LLM_phancap/data/Thông tin tuyển sinh trên trang SIU")
    
    # if not vault_path.exists():
    #     print(f"Thư mục không tồn tại: {vault_path}")
    #     sys.exit(1)
    
    run = VaultBrowser("/workspace/vinhnq/NCKH2025/LLM_phancap/data/Thông tin tuyển sinh trên trang SIU")
    while True:
        inp = input("Nhập đường dẫn: ")
        print(run.browse_vault(inp))
        print()

if __name__ == "__main__":
    main()
    
