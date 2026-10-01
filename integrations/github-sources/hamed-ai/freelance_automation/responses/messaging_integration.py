"""
WhatsApp & Telegram Integration - نظام التكامل مع واتساب وتيليجرام
ردود احترافية تلقائية على جميع الرسائل
"""
from typing import Dict, Optional
from datetime import datetime
from .professional_responses import ProfessionalResponseDB

class MessagingIntegration:
    """نظام التكامل مع واتساب وتيليجرام"""
    
    def __init__(self):
        self.db = ProfessionalResponseDB()
        self.phone_number = "01061245527"
    
    def detect_intent(self, message: str) -> Dict:
        """تحليل نية الرسالة"""
        message_lower = message.lower()
        
        # نوايا عامة
        if any(word in message_lower for word in ['مرحبا', 'اهلا', 'السلام', 'هاي', 'صباح', 'مساء']):
            return {'intent': 'greeting', 'confidence': 0.95}
        
        elif any(word in message_lower for word in ['شكر', 'ممتاز', 'رائع', 'جزاك']):
            return {'intent': 'thank_you', 'confidence': 0.90}
        
        elif any(word in message_lower for word in ['مشكلة', 'خطأ', 'لا يعمل', 'عطل']):
            return {'intent': 'complaint', 'confidence': 0.85}
        
        # نوايا الخدمات
        elif any(word in message_lower for word in ['سعر', 'تكلفة', 'كم', 'ثمن']):
            return {'intent': 'price_inquiry', 'confidence': 0.90}
        
        elif any(word in message_lower for word in ['دفع', 'تحويل', 'فودافون', 'كاش']):
            return {'intent': 'payment_inquiry', 'confidence': 0.90}
        
        elif any(word in message_lower for word in ['متى', 'موعد', 'تسليم', 'وقت']):
            return {'intent': 'delivery_inquiry', 'confidence': 0.90}
        
        # خدمات محددة
        elif any(word in message_lower for word in ['تحليل', 'موقع', 'site']):
            return {'intent': 'service_inquiry', 'service_type': 'website_analysis', 'confidence': 0.85}
        
        elif any(word in message_lower for word in ['seo', 'سيو', 'محركات البحث']):
            return {'intent': 'service_inquiry', 'service_type': 'seo_optimization', 'confidence': 0.85}
        
        elif any(word in message_lower for word in ['كتابة', 'مقال', 'محتوى', 'content']):
            return {'intent': 'service_inquiry', 'service_type': 'content_writing', 'confidence': 0.85}
        
        # خدمة مخصصة
        elif any(word in message_lower for word in ['خدمة', 'تقدم', 'توفر', 'عندكم']):
            return {'intent': 'service_inquiry', 'service_type': 'custom', 'confidence': 0.80}
        
        # نية غير معروفة
        else:
            return {'intent': 'unknown_service', 'confidence': 0.50}
    
    def process_message(self, client_id: str, platform: str, message: str) -> str:
        """معالجة رسالة العميل والرد عليها"""
        
        # تحليل النية
        intent_data = self.detect_intent(message)
        intent = intent_data['intent']
        service_type = intent_data.get('service_type')
        
        # الحصول على الرد الاحترافي
        response = self.db.get_response(intent, service_type)
        
        # إذا لم يوجد رد محدد، استخدم الرد العام
        if not response:
            response = self.db.get_response('unknown_service')
        
        # تخصيص الرد بالمعلومات الشخصية
        response = self._personalize_response(response, client_id, platform)
        
        # تسجيل المحادثة
        self.db.record_conversation(
            client_id=client_id,
            platform=platform,
            message=message,
            response=response,
            intent_detected=intent,
            outcome='responded'
        )
        
        return response
    
    def _personalize_response(self, response: str, client_id: str, platform: str) -> str:
        """تخصيص الرد"""
        # إضافة معلومات المنصة
        if platform == 'whatsapp':
            response = response.replace('01061245527', f'wa.me/{self.phone_number}')
        
        return response
    
    def send_whatsapp_message(self, phone: str, message: str) -> Dict:
        """إرسال رسالة واتساب (محاكاة)"""
        # في الإنتاج: استخدم WhatsApp Business API
        # هنا نحاكي الإرسال
        
        return {
            'status': 'sent',
            'phone': phone,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'message_id': f'WA-{datetime.now().strftime("%Y%m%d%H%M%S")}'
        }
    
    def send_telegram_message(self, chat_id: str, message: str) -> Dict:
        """إرسال رسالة تيليجرام (محاكاة)"""
        # في الإنتاج: استخدم Telegram Bot API
        # هنا نحاكي الإرسال
        
        return {
            'status': 'sent',
            'chat_id': chat_id,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'message_id': f'TG-{datetime.now().strftime("%Y%m%d%H%M%S")}'
        }
    
    def handle_incoming_whatsapp(self, phone: str, message: str) -> str:
        """معالجة رسالة واتساب واردة"""
        response = self.process_message(phone, 'whatsapp', message)
        self.send_whatsapp_message(phone, response)
        return response
    
    def handle_incoming_telegram(self, chat_id: str, message: str) -> str:
        """معالجة رسالة تيليجرام واردة"""
        response = self.process_message(chat_id, 'telegram', message)
        self.send_telegram_message(chat_id, response)
        return response
