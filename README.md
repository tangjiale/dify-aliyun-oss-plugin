## 阿里云OSS文件上传插件 (Aliyun OSS Upload Plugin)

**作者:** tangjiale
**版本:** 0.0.1
**类型:** tool

### 描述

这是一个用于Dify平台的阿里云对象存储服务(OSS)文件上传插件。通过此插件，您可以轻松地将文件上传到阿里云OSS存储桶中，并获取文件的访问URL。

### 功能特点

- 支持通过文件内容直接上传文件
- 支持通过文件URL上传文件
- 支持Base64编码的文件内容上传
- 自定义对象键(Object Key)，控制文件在OSS中的存储路径
- 返回上传成功后的文件访问URL

### 安装要求

- Python 3.12 或更高版本
- Dify平台
- 阿里云账号及OSS服务

### 配置说明

使用此插件前，您需要提供以下阿里云OSS凭证信息：

1. **Access Key ID**: 阿里云账号的访问密钥ID
2. **Access Key Secret**: 阿里云账号的访问密钥Secret
3. **Bucket Name**: OSS存储桶名称
4. **Endpoint**: OSS访问域名，例如 `oss-cn-hangzhou.aliyuncs.com`

### 使用方法

插件提供以下参数用于上传文件：

- **file_content**: 文件内容（字符串或Base64编码的内容）
- **file_url**: 文件URL，用于从远程位置下载文件并上传
- **file_name**: 文件名称（必填）
- **object_key**: 对象键，即文件在OSS中的存储路径（可选，默认使用file_name）

**注意**: 必须提供`file_content`或`file_url`中的一个参数。

### 返回结果

上传成功后，插件将返回以下信息：

```json
{
  "success": true,
  "message": "文件上传成功",
  "file_name": "example.txt",
  "object_key": "example.txt",
  "etag": "ETAG值",
  "file_url": "https://bucket-name.oss-cn-hangzhou.aliyuncs.com/example.txt"
}
```

### 示例

```
上传文本文件：
{
  "file_content": "这是一个测试文件的内容",
  "file_name": "test.txt"
}

上传远程文件：
{
  "file_url": "https://example.com/image.jpg",
  "file_name": "image.jpg",
  "object_key": "images/image.jpg"
}
```



