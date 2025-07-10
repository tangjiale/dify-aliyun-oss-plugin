from collections.abc import Generator
import base64
import os
import tempfile
import uuid
from typing import Any, Optional
import urllib.request

import oss2
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class AliyunOssPluginTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # 获取参数
        file_content = tool_parameters.get('file_content')
        file_url = tool_parameters.get('file_url')
        file_name = tool_parameters.get('file_name')
        object_key = tool_parameters.get('object_key', file_name)
        
        # 检查必要参数
        if not file_name:
            yield self.create_text_message("错误：必须提供文件名(file_name)")
            return
            
        if not file_content and not file_url:
            yield self.create_text_message("错误：必须提供文件内容(file_content)或文件URL(file_url)")
            return
        
        # 获取凭证
        credentials = self.credentials
        access_key_id = credentials.get('access_key_id')
        access_key_secret = credentials.get('access_key_secret')
        bucket_name = credentials.get('bucket_name')
        endpoint = credentials.get('endpoint')
        
        # 创建临时文件
        temp_file_path = None
        try:
            # 创建认证对象
            auth = oss2.Auth(access_key_id, access_key_secret)
            
            # 创建存储桶对象
            bucket = oss2.Bucket(auth, endpoint, bucket_name)
            
            # 处理文件内容
            if file_content:
                # 检查是否是base64编码的内容
                if file_content.startswith('data:') and ';base64,' in file_content:
                    # 解析base64编码的数据
                    _, encoded_data = file_content.split(';base64,', 1)
                    file_content = base64.b64decode(encoded_data)
                
                # 如果提供了文件内容，直接上传
                result = bucket.put_object(object_key, file_content)
            else:
                # 如果提供了文件URL，下载后上传
                temp_file_path = self._download_file(file_url)
                with open(temp_file_path, 'rb') as f:
                    result = bucket.put_object(object_key, f)
            
            # 生成文件URL
            file_url = f"https://{bucket_name}.{endpoint}/{object_key}"
            
            # 返回结果
            yield self.create_json_message({
                "success": True,
                "message": "文件上传成功",
                "file_name": file_name,
                "object_key": object_key,
                "etag": result.etag,
                "file_url": file_url
            })
            
        except Exception as e:
            yield self.create_json_message({
                "success": False,
                "message": f"文件上传失败: {str(e)}"
            })
        finally:
            # 清理临时文件
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
    
    def _download_file(self, url: str) -> str:
        """下载文件到临时目录"""
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}.tmp")
        
        urllib.request.urlretrieve(url, temp_file_path)
        return temp_file_path
