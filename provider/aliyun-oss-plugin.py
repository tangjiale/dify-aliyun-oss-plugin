from typing import Any

import oss2
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class AliyunOssPluginProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            # 验证阿里云OSS凭证
            access_key_id = credentials.get('access_key_id')
            access_key_secret = credentials.get('access_key_secret')
            bucket_name = credentials.get('bucket_name')
            endpoint = credentials.get('endpoint')
            
            # 检查必要的凭证是否存在
            if not access_key_id or not access_key_secret or not bucket_name or not endpoint:
                raise ValueError("Missing required credentials: access_key_id, access_key_secret, bucket_name, endpoint")
            
            # 创建认证对象
            auth = oss2.Auth(access_key_id, access_key_secret)
            
            # 创建存储桶对象
            bucket = oss2.Bucket(auth, endpoint, bucket_name)
            
            # 尝试列出文件，验证凭证是否有效
            list(bucket.list_objects(max_keys=1))
            
        except oss2.exceptions.OssError as e:
            raise ToolProviderCredentialValidationError(f"OSS credential validation failed: {str(e)}")
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
