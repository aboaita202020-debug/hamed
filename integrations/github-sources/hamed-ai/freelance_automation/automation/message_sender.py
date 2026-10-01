"""
Message Sender - يبعت رسائل تلقائية لأصحاب المواقع
"""
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

from core.config import Config
from core.database import Database
from core.logger import logger

class MessageSender:
    """يبعت رسائل احترافية لأصحاب المواقع"""
    
    def __init__(self):
        self.db = Database()
        self.whatsapp_number = "01061245527"
        self.vodafone_cash = "01061245527"
        
        logger.info("MessageSender initialized")
    
    def send_analysis_report(self, url: str, analysis: Dict, contact_info: Dict = None) -> Dict:
        """إرسال تقرير التحليل لصاحب الموقع"""
        
        # توليد رسالة احترافية
        message = self._generate_professional_message(url, analysis)
        
        # حفظ الرسالة في قاعدة البيانات
        message_id = self._save_message(url, message, contact_info)
        
        # محاكاة إرسال (في الإنتاج: إرسال حقيقي عبر WhatsApp/Email)
        sent = self._send_message(message, contact_info)
        
        if sent:
            self._update_message_status(message_id, "sent")
            logger.info(f"Message sent successfully for {url}")
        else:
            self._update_message_status(message_id, "failed")
            logger.error(f"Failed to send message for {url}")
        
        return {
            "message_id": message_id,
            "url": url,
            "message": message,
            "sent": sent,
            "sent_at": datetime.now().isoformat() if sent else None
        }
    
    def _generate_professional_message(self, url: str, analysis: Dict) -> str:
        """توليد رسالة احترافية"""
        
        domain = analysis.get('domain', url)
        score = analysis.get('score', 0)
        recommendations = analysis.get('recommendations', [])
        services = analysis.get('services', [])
        
        # بناء الرسالة
        message = f"""🎯 تحليل مجاني لموقعك: {domain}

مرحباً،

قمت بتحليل موقعك {domain} ووجدت بعض النقاط المهمة:

📊 النتيجة الإجمالية: {score}/100

🔍 أهم الملاحظات:
"""
        
        # إضافة التوصيات
        for i, rec in enumerate(recommendations[:3], 1):
            message += f"{i}. {rec}\n"
        
        message += f"""
💡 الخدمات المقترحة لتحسين موقعك:
"""
        
        # إضافة الخدمات
        for service in services[:3]:
            message += f"✅ {service['name']} - ${service['price']} ({service['delivery']})\n"
        
        message += f"""
🎁 عرض خاص:
- تحليل مجاني شامل لموقعك
- خصم 20% على أول خدمة
- ضمان جودة 100%

📞 للتواصل:
واتساب: {self.whatsapp_number}
فودافون كاش: {self.vodafone_cash}

🚀 ابدأ الآن واحصل على موقع احترافي يزيد مبيعاتك!

مع التحية،
فريق التطوير المتخصص
"""
        
        return message
    
    def _save_message(self, url: str, message: str, contact_info: Dict = None) -> str:
        """حفظ الرسالة في قاعدة البيانات"""
        message_id = f"MSG-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        try:
            self.db.execute("""
                INSERT INTO messages 
                (id, url, message, contact_info, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                message_id,
                url,
                message,
                json.dumps(contact_info) if contact_info else None,
                "pending",
                datetime.now().isoformat()
            ))
        except Exception as e:
            logger.error(f"Failed to save message: {e}")
        
        return message_id
    
    def _send_message(self, message: str, contact_info: Dict = None) -> bool:
        """
        إرسال الرسالة
        في الإنتاج: استخدم WhatsApp Business API أو Email API
        """
        try:
            # محاكاة إرسال ناجح
            # في الإنتاج:
            # - WhatsApp: استخدم Twilio أو WhatsApp Business API
            # - Email: استخدم SendGrid أو Mailgun
            
            time.sleep(1)  # محاكاة وقت الإرسال
            
            return True
        
        except Exception as e:
            logger.error(f"Send message failed: {e}")
            return False
    
    def _update_message_status(self, message_id: str, status: str):
        """تحديث حالة الرسالة"""
        try:
            self.db.execute("""
                UPDATE messages 
                SET status = ?, sent_at = ?
                WHERE id = ?
            """, (status, datetime.now().isoformat() if status == "sent" else None, message_id))
        except Exception as e:
            logger.error(f"Failed to update message status: {e}")
    
    def get_message_history(self, limit: int = 10) -> List[Dict]:
        """جلب سجل الرسائل"""
        return self.db.fetch_all("""
            SELECT * FROM messages 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
    
    def get_payment_info(self) -> Dict:
        """معلومات الدفع"""
        return {
            "whatsapp": self.whatsapp_number,
            "vodafone_cash": self.vodafone_cash,
            "message": f"للدفع عبر فودافون كاش: {self.vodafone_cash}"
        }
