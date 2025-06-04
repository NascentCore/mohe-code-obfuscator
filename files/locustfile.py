from locust import HttpUser, task, between
import os
import uuid

class FileServiceUser(HttpUser):
    wait_time = between(1, 3)
    file_id = None
    test_filename = "test.txt"
    test_content = "This is a test file for performance testing."
    test_extra = {"desc": "locust test"}
    user_id = "00000000-0000-0000-0000-000000000000"  # UUID 格式
    headers = {"X-User-Id": user_id}

    def on_start(self):
        # 创建测试文件
        with open(self.test_filename, "w") as f:
            f.write(self.test_content)
        # 上传文件，获取 file_id
        with open(self.test_filename, "rb") as f:
            files = {"files": (self.test_filename, f, "text/plain")}
            response = self.client.post("/v1/files", files=files, headers=self.headers)
            if response.status_code == 200 and response.json():
                self.file_id = response.json()[0]["id"]
            else:
                print("Failed to upload test file", response.text)

    @task(2)
    def get_file_list(self):
        self.client.get("/v1/files", headers=self.headers)

    @task(2)
    def get_file_details(self):
        if self.file_id:
            self.client.get(f"/v1/files/{self.file_id}", headers=self.headers)

    @task(1)
    def get_file_content(self):
        if self.file_id:
            self.client.get(f"/v1/files/{self.file_id}/content", headers=self.headers)

    @task(1)
    def update_file(self):
        if self.file_id:
            data = {"extra": {"desc": "updated by locust"}}
            self.client.put(f"/v1/files/{self.file_id}", json=data, headers=self.headers)

    @task(1)
    def soft_delete_file(self):
        if self.file_id:
            self.client.post(f"/v1/files/{self.file_id}/soft-delete", headers=self.headers)

    # @task(1)
    # def batch_get_files(self):
    #     if self.file_id:
    #         data = [{"file_id": self.file_id}]
    #         self.client.post("/v1/files/batch-get", json=data, headers=self.headers)

    # @task(1)
    # def batch_details(self):
    #     if self.file_id:
    #         data = {"file_ids": [self.file_id]}
    #         self.client.post("/v1/files/details", json=data, headers=self.headers)

    @task(1)
    def upload_file(self):
        # 每次上传新文件，便于测试 POST
        filename = f"test_{uuid.uuid4().hex}.txt"
        with open(filename, "w") as f:
            f.write(self.test_content)
        with open(filename, "rb") as f:
            files = {"files": (filename, f, "text/plain")}
            self.client.post("/v1/files", files=files, headers=self.headers)
        os.remove(filename)

    @task(1)
    def delete_file(self):
        # 删除当前 file_id，并重新上传一个，保证后续接口可用
        if self.file_id:
            self.client.delete(f"/v1/files/{self.file_id}", headers=self.headers)
            # 重新上传
            with open(self.test_filename, "rb") as f:
                files = {"files": (self.test_filename, f, "text/plain")}
                response = self.client.post("/v1/files", files=files, headers=self.headers)
                if response.status_code == 200 and response.json():
                    self.file_id = response.json()[0]["id"]
                else:
                    self.file_id = None

    def on_stop(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename) 