from typing import Dict, Any, Optional, List
from kirara_ai.workflow.core.block import Block, Input, Output, ParamMeta
from kirara_ai.logger import get_logger
import json
from pathlib import Path
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import decode_header
import datetime
import re
from kirara_ai.ioc.container import DependencyContainer
import requests
from urllib.parse import urlparse, unquote

logger = get_logger("QQEmail")
def get_options_provider(container: DependencyContainer, block: Block) -> List[str]:
    return ["ALL", "UNSEEN"]

class QQEmailBlock(Block):
    name = "send_qq_email"
    description = "发送QQ邮件"


    inputs = {
        "from_email": Input(name="from_email", label="发件人QQ邮箱", data_type=str, description="发件人QQ邮箱", nullable=True),
        "password": Input(name="password", label="QQ邮箱授权码", data_type=str, description="QQ邮箱授权码", nullable=True),
        "to_email": Input(name="email", label="收件人邮箱", data_type=str, description="收件人邮箱", nullable=True),
        "subject": Input(name="subject", label="邮件主题", data_type=str, description="邮件主题"),
        "body": Input(name="body", label="邮件正文", data_type=str, description="邮件正文")
    }

    outputs = {
        "result": Output(name="result", label="发送结果", data_type=str, description="发送结果")
    }

    def __init__(self):
        super().__init__()
        self.from_email: str = None
        self.password: str = None
        self.smtp_server = "smtp.qq.com"
        self.smtp_port = 587
        # Set config_path to be in the same directory as the script
        self.config_path = Path(__file__).parent / 'config.json'

    def execute(self, **kwargs) -> Dict[str, Any]:
        to_email = kwargs.get("to_email", "")
        if not to_email:
            return {"result": "邮件发送失败，请提供收件人邮箱地址"}
        subject = kwargs.get("subject", "")
        body = kwargs.get("body", "")

        # Process URLs in the body
        urls = self.coverAndSendMessage(body)

        # Try to get credentials in order: input params -> instance vars -> config file
        from_email = kwargs.get("from_email")
        password = kwargs.get("password")

        # If input params are provided, save them
        if from_email and password:
            self.from_email = from_email
            self.password = password
            self.save_credentials(from_email, password)

        # Use instance variables if available
        if not (from_email and password) and self.from_email and self.password:
            from_email = self.from_email
            password = self.password

        # Fall back to config file if needed
        if not (from_email and password):
            credentials = self._load_credentials()
            if credentials:
                from_email = credentials['email']
                password = credentials['password']

        # Check if we have valid credentials
        if not (from_email and password):
            return {"result": "邮件发送失败，请先设置邮箱账号和授权码（授权码获取路径：qq邮箱-设置-账号与安全-安全设置-开启服务-获取授权码）"}

        if from_email and not from_email.endswith("@qq.com"):
            return {"result": "邮件发送失败，请先设置邮箱账号和授权码（授权码获取路径：qq邮箱-设置-账号与安全-安全设置-开启服务-获取授权码）"}
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 添加URL作为附件
            if urls:
                for i, url in enumerate(urls):
                    try:
                        response = requests.get(url, timeout=10)
                        filename = f"attachment_{i+1}"

                        # Add appropriate extension based on content type
                        content_type = response.headers.get('Content-Type', '').lower()

                        # Determine file extension from content type if missing
                        if '.' not in filename:
                            if 'image/jpeg' in content_type:
                                filename += '.jpg'
                            elif 'image/png' in content_type:
                                filename += '.png'
                            elif 'image/gif' in content_type:
                                filename += '.gif'
                            elif 'image/' in content_type:
                                filename += '.jpg'
                            elif 'video/mp4' in content_type:
                                filename += '.mp4'
                            elif 'video/' in content_type:
                                filename += '.mp4'
                            elif 'audio/mpeg' in content_type:
                                filename += '.mp3'
                            elif 'audio/' in content_type:
                                filename += '.mp3'
                            elif 'application/pdf' in content_type:
                                filename += '.pdf'
                            else:
                                # Default extension based on binary content
                                filename += '.bin'

                        # Create attachment
                        attachment = MIMEApplication(response.content)
                        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                        msg.attach(attachment)
                    except Exception as e:
                        logger.warning(f"添加URL附件时出错: {str(e)}")

            # 连接SMTP服务器并发送邮件
            server = None
            try:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()  # 启用TLS加密
                server.login(from_email, password)
                server.send_message(msg)
                return {"result": "邮件发送成功"}
            except Exception as e:
                logger.error(f"发送邮件时出错: {str(e)}")
                return {"result": f"发送邮件时出错: {str(e)}"}
            finally:
                if server:
                    try:
                        server.quit()
                    except Exception as e:
                        logger.warning(f"关闭SMTP连接时出错: {str(e)}")

        except Exception as e:
            logger.error(f"发送邮件时出错: {e}")
            return {"result": str(e)}

    def coverAndSendMessage(self, message: str) -> List[str]:
        # 首先替换掉转义的换行符为实际换行符
        message = message.replace('\\n', '\n')
        # 修改正则表达式以正确处理换行符分隔的URL
        url_pattern = r'https?://[^\s\n<>\"\']+|www\.[^\s\n<>\"\']+'
        # 文件扩展名列表
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.ico', '.tiff'}
        audio_extensions = {'.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac', '.midi', '.mid'}
        video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v', '.3gp'}

        try:
            urls = re.findall(url_pattern, message)
            # If no URLs found, return None
            if not urls:
                return None

            available_urls = []
            for url in urls:
                try:
                    # Parse URL
                    parsed = urlparse(url)
                    path = unquote(parsed.path)

                    # Get extension from path
                    ext = None
                    if '.' in path:
                        ext = '.' + path.split('.')[-1].lower()
                        if '/' in ext or len(ext) > 10:
                            ext = None

                    # 使用URL直接创建消息对象，而不是下载内容
                    if ext in image_extensions:
                        available_urls.append(url)
                        continue
                    elif ext in audio_extensions:
                        available_urls.append(url)
                        continue
                    elif ext in video_extensions:
                        available_urls.append(url)
                        continue

                    try:
                        response = requests.head(url, allow_redirects=True, timeout=5)
                        content_type = response.headers.get('Content-Type', '').lower()
                    except Exception as e:
                        logger.warning(f"Failed to get headers for {url}: {str(e)}")
                        content_type = ''

                    logger.debug(content_type)
                    # Check content type first, then fall back to extension
                    if any(x in content_type for x in ['image', 'png', 'jpg', 'jpeg', 'gif']):
                        available_urls.append(url)
                    elif any(x in content_type for x in ['video', 'mp4', 'avi', 'mov']):
                        available_urls.append(url)
                    elif any(x in content_type for x in ['audio', 'voice', 'mp3', 'wav']):
                        available_urls.append(url)
                except Exception as e:
                    logger.error(f"Error processing URL {url}: {str(e)}")
                    continue

            return available_urls
        except Exception as e:
            logger.error(f"Error in coverAndSendMessage: {str(e)}")
        return None

    def _load_credentials(self) -> Optional[Dict[str, Any]]:
        """从本地加载邮箱凭据"""
        try:
            if not self.config_path.exists():
                return None

            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载凭据时出错: {e}")
            return None

    def save_credentials(self, email: str, password: str) -> bool:
        """保存邮箱凭据到本地"""
        try:
            # 确保配置目录存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # 保存凭据
            credentials = {
                "email": email,
                "password": password
            }

            with open(self.config_path, 'w') as f:
                json.dump(credentials, f)

            return True
        except Exception as e:
            logger.error(f"保存凭据时出错: {e}")
            return False

class QQEmailFetchBlock(Block):
    name = "find_qq_emails"
    description = "查看QQ邮件"

    inputs = {
        "from_email": Input(name="from_email", label="QQ邮箱", data_type=str, description="发言人的QQ邮箱账号", nullable=True),
        "password": Input(name="password", label="QQ邮箱授权码", data_type=str, description="QQ邮箱授权码", nullable=True),
        "email_status": Input(name="email_status", label="要查看的邮件状态", data_type=str, description="要查看的邮件状态，状态列表如下['ALL', 'UNSEEN']", nullable=True, default="UNSEEN"),
        "num_emails": Input(name="num_emails", label="获取邮件数量", data_type=int, description="要获取的邮件数量", default=5)
    }

    outputs = {
        "emails": Output(name="emails", label="邮件列表", data_type=List[Dict], description="获取到的邮件列表"),
        "result": Output(name="result", label="获取结果", data_type=str, description="获取结果说明")
    }

    def __init__(self):
        super().__init__()
        self.from_email: str = None
        self.password: str = None
        self.imap_server = "imap.qq.com"
        self.imap_port = 993
        self.config_path = Path(__file__).parent / 'config.json'

    def _remove_urls(self, text: str) -> str:
        """移除文本中的URL"""
        # 匹配URL的正则表达式
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        # 移除URL
        text = re.sub(url_pattern, '', text)
        # 移除多余的空行和空格
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def _extract_date_from_received(self, message) -> Optional[datetime.datetime]:
        """从Received头中提取日期"""
        try:
            # 获取所有的Received头
            received_headers = message.get_all('Received')
            if not received_headers:
                return None

            # 使用第一个Received头（最后一个接收服务器的时间）
            received = received_headers[0]

            # 查找日期部分，通常在分号后面
            date_part = received.split(';')[-1].strip()

            # 解析日期
            return email.utils.parsedate_to_datetime(date_part)
        except Exception as e:
            logger.warning(f"从Received头提取日期失败: {str(e)}")
            return None

    def execute(self, **kwargs) -> Dict[str, Any]:
        # Get credentials similar to send email block
        from_email = kwargs.get("from_email")
        password = kwargs.get("password")
        num_emails = kwargs.get("num_emails", 5)
        email_status = "UNSEEN"

        # If input params are provided, save them
        if from_email and password:
            self.from_email = from_email
            self.password = password
            self.save_credentials(from_email, password)

        # Use instance variables if available
        if not (from_email and password) and self.from_email and self.password:
            from_email = self.from_email
            password = self.password

        # Fall back to config file if needed
        if not (from_email and password):
            credentials = self._load_credentials()
            if credentials:
                from_email = credentials['email']
                password = credentials['password']

        # Check if we have valid credentials
        if not (from_email and password):
            return {
                "emails": [],
                "result": "获取邮件失败，请先设置邮箱账号和授权码（授权码获取路径：qq邮箱-设置-账号与安全-安全设置-开启服务-获取授权码）"
            }

        try:
            # 连接IMAP服务器
            imap_server = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            imap_server.login(from_email, password)

            # 选择收件箱
            imap_server.select('INBOX')

            # 搜索未读邮件
            _, message_numbers = imap_server.search(None, email_status)
            email_ids = message_numbers[0].split()

            if not email_ids:
                return {
                    "emails": [],
                    "result": "没有未读邮件"
                }

            emails_list = []
            email_with_dates = []

            # 获取所有未读邮件的信息
            for email_id in email_ids:
                try:
                    _, msg_data = imap_server.fetch(email_id, '(RFC822)')
                    email_body = msg_data[0][1]
                    message = email.message_from_bytes(email_body)
                    # 获取日期并转换为datetime对象
                    date = None
                    try:
                        date = email.utils.parsedate_to_datetime(message["date"])
                    except (TypeError, ValueError):
                        # 如果date字段为空或格式错误，尝试从Received头获取
                        date = self._extract_date_from_received(message)
                        if not date:
                            continue
                    # 解码邮件主题
                    subject = decode_header(message["subject"])[0]
                    subject = subject[0].decode(subject[1]) if subject[1] else subject[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    # 获取发件人
                    from_header = decode_header(message["from"])[0]
                    sender = from_header[0].decode(from_header[1]) if from_header[1] else from_header[0]
                    if isinstance(sender, bytes):
                        sender = sender.decode()

                    # 获取邮件内容
                    content = ""
                    if message.is_multipart():
                        for part in message.walk():
                            if part.get_content_type() == "text/plain":
                                try:
                                    content = part.get_payload(decode=True).decode()
                                    content = self._remove_urls(content)  # 移除URL
                                    break
                                except:
                                    continue
                    else:
                        try:
                            content = message.get_payload(decode=True).decode()
                            content = self._remove_urls(content)  # 移除URL
                        except:
                            content = "无法解析邮件内容"

                    # 将邮件信息和日期一起存储
                    email_with_dates.append({
                        "id": email_id.decode(),
                        "date": date,
                        "date_str": date.strftime("%Y-%m-%d %H:%M:%S"),
                        "subject": subject,
                        "sender": sender,
                        "content": content
                    })
                except Exception as e:
                    logger.error(f"解析邮件时出错: {str(e)}")
                    continue

            # 按日期降序排序
            email_with_dates.sort(key=lambda x: x["date"], reverse=True)

            # 只取指定数量的邮件
            email_with_dates = email_with_dates[:num_emails]

            # 处理最终结果并标记为已读
            for email_info in email_with_dates:
                email_id = email_info["id"].encode()
                imap_server.store(email_id, '+FLAGS', '\\Seen')

                # 移除datetime对象，只保留字符串格式的日期
                del email_info["date"]
                emails_list.append(email_info)

            imap_server.close()
            imap_server.logout()

            return {
                "emails": emails_list,
                "result": f"成功获取{len(emails_list)}封未读邮件"
            }

        except Exception as e:
            logger.error(f"获取邮件时出错: {str(e)}")
            return {
                "emails": [],
                "result": f"获取邮件失败: {str(e)}"
            }

    def _load_credentials(self) -> Optional[Dict[str, Any]]:
        """从本地加载邮箱凭据"""
        try:
            if not self.config_path.exists():
                return None

            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载凭据时出错: {e}")
            return None

    def save_credentials(self, email: str, password: str) -> bool:
        """保存邮箱凭据到本地"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            credentials = {
                "email": email,
                "password": password
            }
            with open(self.config_path, 'w') as f:
                json.dump(credentials, f)
            return True
        except Exception as e:
            logger.error(f"保存凭据时出错: {e}")
            return False
