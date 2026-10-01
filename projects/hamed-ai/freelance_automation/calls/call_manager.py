"""
Call Manager - مدير المكالمات الذكي
يتكامل مع البائع الذكي ويدير كل المكالمات
"""
import time
import random
from datetime import datetime
from typing import Dict, List, Optional
from .call_database import CallDatabase

class CallManager:
    """مدير المكالمات الذكي"""
    
    def __init__(self):
        self.db = CallDatabase()
        self.phone_number = "01061245527"
        self._init_default_templates()
    
    def _init_default_templates(self):
        """تهيئة قوالب المكالمات الافتراضية"""
        templates = [
            {
                'name': 'Sales Call - Website Analysis',
                'service_type': 'website_analysis',
                'opening': 'مرحباً، معك [اسمك] من فريق التطوير. هل لدي دقيقة من وقتك؟',
                'script': '''🎯 مكالمة بيع - تحليل المواقع

1. الترحيب والتعريف
   - مرحباً، معك [اسمك]
   - أنا من فريق التطوير المتخصص في تحسين المواقع

2. تقديم القيمة
   - لاحظت موقعك [اسم الموقع]
   - قمت بتحليل سريع ووجدت بعض النقاط المهمة
   - النتيجة الحالية: [النتيجة]/100

3. عرض المشكلة
   - هناك [عدد] مشاكل يمكن تحسينها
   - هذا يؤثر على [الزيارات/المبيعات/SEO]

4. تقديم الحل
   - نقدم خدمة تحليل شامل
   - تشمل [القائمة]
   - السعر: [السعر] فقط

5. إغلاق الصفقة
   - هل تريد أن نبدأ الآن؟
   - لدينا عرض خاص خصم 20%
   - الدفع عبر فودافون كاش: 01061245527''',
                'closing': 'شكراً لوقتك. سنتواصل معك قريباً. يوم سعيد!',
                'key_points': 'التركيز على القيمة، تقديم تحليل مجاني، خصم 20%'
            },
            {
                'name': 'Follow-up Call',
                'service_type': 'follow_up',
                'opening': 'مرحباً، معك [اسمك]. كيف حالك؟',
                'script': '''📞 مكالمة متابعة

1. الترحيب
   - مرحباً [اسم العميل]
   - كيف حالك؟

2. المراجعة
   - تحدثنا مؤخراً عن [الخدمة]
   - هل كان لديك وقت للتفكير؟

3. الإجابة على الأسئلة
   - هل لديك أي أسئلة؟
   - هل تحتاج معلومات إضافية؟

4. الدفع
   - يمكننا البدء اليوم
   - الدفع عبر فودافون كاش: 01061245527

5. الإغلاق
   - متى تريد أن نبدأ؟''',
                'closing': 'ممتاز! سنتواصل معك قريباً. شكراً!',
                'key_points': 'متابعة ودية، الإجابة على الأسئلة، تسهيل الدفع'
            },
            {
                'name': 'Customer Support Call',
                'service_type': 'support',
                'opening': 'مرحباً، معك [اسمك] من خدمة العملاء. كيف يمكنني مساعدتك؟',
                'script': '''🛎️ مكالمة دعم فني

1. الترحيب
   - مرحباً، معك [اسمك]
   - كيف يمكنني مساعدتك اليوم؟

2. فهم المشكلة
   - ما المشكلة التي تواجهها؟
   - متى بدأت المشكلة؟
   - هل جربت أي حلول؟

3. تقديم الحل
   - سأقوم بحل المشكلة الآن
   - [شرح الحل]

4. التأكد من الرضا
   - هل تم حل المشكلة؟
   - هل تحتاج مساعدة أخرى؟

5. الإغلاق
   - شكراً لتواصلك معنا
   - نتطلع لخدمتك مرة أخرى''',
                'closing': 'شكراً لتواصلك. نتطلع لخدمتك مرة أخرى!',
                'key_points': 'الاستماع الجيد، حل سريع، التأكد من الرضا'
            }
        ]
        
        for template in templates:
            self.db.add_call_template(
                name=template['name'],
                script=template['script'],
                service_type=template['service_type'],
                opening=template['opening'],
                closing=template['closing'],
                key_points=template['key_points']
            )
    
    # ============ إدارة المكالمات ============
    
    def initiate_call(self, client_ Dict, call_type: str = 'sales',
                     purpose: str = None) -> Dict:
        """بدء مكالمة جديدة"""
        
        # إنشاء المكالمة
        call_id = self.db.create_call(
            client_id=client_data.get('client_id'),
            client_name=client_data.get('name'),
            client_phone=client_data.get('phone'),
            direction='outgoing',
            call_type=call_type,
            purpose=purpose
        )
        
        # الحصول على القالب المناسب
        template = self.db.get_call_template(call_type)
        
        # تخصيص القالب
        if template:
            script = self._customize_template(template, client_data)
        else:
            script = self._generate_generic_script(client_data, call_type)
        
        return {
            'call_id': call_id,
            'client': client_data,
            'script': script,
            'template': template,
            'status': 'ready',
            'phone_number': self.phone_number
        }
    
    def _customize_template(self, template: Dict, client_ Dict) -> Dict:
        """تخصيص القالب حسب العميل"""
        
        script = template['script']
        
        # استبدال المتغيرات
        replacements = {
            '[اسمك]': 'أحمد',
            '[اسم الموقع]': client_data.get('website', 'موقعك'),
            '[النتيجة]': str(client_data.get('score', 65)),
            '[عدد]': str(client_data.get('issues_count', 5)),
            '[القائمة]': 'تحليل شامل، تحسين SEO، تحسين السرعة',
            '[السعر]': '$50',
            '[اسم العميل]': client_data.get('name', 'العميل')
        }
        
        for key, value in replacements.items():
            script = script.replace(key, value)
        
        return {
            'opening': template['opening'],
            'script': script,
            'closing': template['closing'],
            'key_points': template['key_points']
        }
    
    def _generate_generic_script(self, client_ Dict, call_type: str) -> Dict:
        """توليد سكربت عام"""
        
        name = client_data.get('name', 'العميل')
        
        return {
            'opening': f'مرحباً {name}، معك أحمد من فريق التطوير.',
            'script': f'''📞 مكالمة {call_type}

1. الترحيب
   - مرحباً {name}
   - كيف حالك؟

2. الغرض من المكالمة
   - أردت التحدث معك عن خدماتنا
   - نقدم خدمات [نوع الخدمة]

3. العرض
   - لدينا عرض خاص لك
   - السعر: $50 فقط
   - الدفع عبر فودافون كاش: 01061245527

4. الإغلاق
   - هل تريد أن نبدأ؟''',
            'closing': 'شكراً لوقتك. يوم سعيد!',
            'key_points': 'التركيز على القيمة، تسهيل الدفع'
        }
    
    def start_call(self, call_id: str) -> Dict:
        """بدء المكالمة فعلياً"""
        
        self.db.update_call_status(call_id, 'in_progress')
        
        return {
            'call_id': call_id,
            'status': 'in_progress',
            'started_at': datetime.now().isoformat()
        }
    
    def end_call(self, call_id: str, duration: int, outcome: str = None,
                notes: str = None) -> Dict:
        """إنهاء المكالمة"""
        
        self.db.update_call_status(
            call_id,
            'completed',
            duration=duration,
            outcome=outcome,
            notes=notes
        )
        
        # تحديث الإحصائيات
        self.db.update_daily_stats()
        
        # تحديث جهة الاتصال
        call = self.db.get_call(call_id)
        if call and call.get('client_id'):
            self.db.update_contact_after_call(call['client_id'], duration)
        
        # تحديث القالب إذا كان هناك
        if call and call.get('call_type'):
            template = self.db.get_call_template(call['call_type'])
            if template:
                success = outcome == 'success'
                self.db.update_template_stats(template['id'], success)
        
        return {
            'call_id': call_id,
            'status': 'completed',
            'duration': duration,
            'outcome': outcome,
            'ended_at': datetime.now().isoformat()
        }
    
    def miss_call(self, call_id: str, reason: str = None) -> Dict:
        """تسجيل مكالمة فائتة"""
        
        self.db.update_call_status(
            call_id,
            'missed',
            notes=reason
        )
        
        return {
            'call_id': call_id,
            'status': 'missed',
            'reason': reason
        }
    
    # ============ إدارة جهات الاتصال ============
    
    def add_contact(self, name: str, phone: str, email: str = None,
                   company: str = None, service_type: str = None) -> str:
        """إضافة جهة اتصال"""
        return self.db.add_contact(name, phone, email, company, service_type)
    
    def get_contact(self, contact_id: str) -> Optional[Dict]:
        """الحصول على جهة اتصال"""
        return self.db.get_contact(contact_id)
    
    def get_all_contacts(self) -> List[Dict]:
        """الحصول على كل جهات الاتصال"""
        return self.db.get_all_contacts()
    
    # ============ المكالمات الواردة ============
    
    def handle_incoming_call(self, phone: str) -> Dict:
        """التعامل مع مكالمة واردة"""
        
        # البحث عن جهة الاتصال
        contacts = self.db.get_all_contacts()
        contact = next((c for c in contacts if c['phone'] == phone), None)
        
        # إنشاء مكالمة
        call_id = self.db.create_call(
            client_id=contact['contact_id'] if contact else None,
            client_name=contact['name'] if contact else 'Unknown',
            client_phone=phone,
            direction='incoming',
            call_type='support'
        )
        
        return {
            'call_id': call_id,
            'contact': contact,
            'status': 'ringing',
            'phone_number': self.phone_number
        }
    
    # ============ الإحصائيات والتقارير ============
    
    def get_call_history(self, client_id: str = None, limit: int = 50) -> List[Dict]:
        """الحصول على سجل المكالمات"""
        return self.db.get_call_history(client_id, limit)
    
    def get_active_calls(self) -> List[Dict]:
        """الحصول على المكالمات النشطة"""
        return self.db.get_active_calls()
    
    def get_stats(self, days: int = 7) -> Dict:
        """الحصول على الإحصائيات"""
        
        overall = self.db.get_overall_stats()
        daily = self.db.get_call_stats(days)
        
        return {
            'overall': overall,
            'daily': daily,
            'period_days': days
        }
    
    def generate_call_report(self, days: int = 30) -> Dict:
        """توليد تقرير شامل عن المكالمات"""
        
        stats = self.get_stats(days)
        history = self.get_call_history(limit=100)
        
        # حساب المؤشرات
        total_calls = stats['overall']['total_calls']
        completed = stats['overall']['completed_calls']
        missed = stats['overall']['missed_calls']
        
        success_rate = stats['overall']['success_rate']
        avg_duration = stats['overall']['avg_duration']
        
        # تحليل النتائج
        outcomes = {}
        for call in history:
            outcome = call.get('outcome', 'unknown')
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
        
        return {
            'period_days': days,
            'total_calls': total_calls,
            'completed_calls': completed,
            'missed_calls': missed,
            'success_rate': success_rate,
            'avg_duration': avg_duration,
            'outcomes': outcomes,
            'recommendations': self._generate_recommendations(stats, outcomes)
        }
    
    def _generate_recommendations(self, stats: Dict, outcomes: Dict) -> List[str]:
        """توليد توصيات بناءً على الإحصائيات"""
        
        recommendations = []
        
        overall = stats['overall']
        
        # تحليل معدل النجاح
        if overall['success_rate'] < 50:
            recommendations.append("⚠️ معدل النجاح منخفض - راجع قوالب المكالمات")
        elif overall['success_rate'] > 80:
            recommendations.append("✅ أداء ممتاز - حافظ على هذا المستوى")
        
        # تحليل المكالمات الفائتة
        if overall['missed_calls'] > overall['total_calls'] * 0.2:
            recommendations.append("📞 عدد كبير من المكالمات الفائتة - حاول الرد بسرعة")
        
        # تحليل مدة المكالمات
        if overall['avg_duration'] < 60:
            recommendations.append("⏱️ المكالمات قصيرة جداً - حاول تحسين العرض")
        elif overall['avg_duration'] > 600:
            recommendations.append("⏱️ المكالمات طويلة جداً - حاول الاختصار")
        
        # تحليل النتائج
        if 'success' in outcomes:
            success_count = outcomes['success']
            total = sum(outcomes.values())
            if success_count / total > 0.7:
                recommendations.append("🎯 نسبة نجاح عالية - استمر في نفس النهج")
        
        return recommendations
