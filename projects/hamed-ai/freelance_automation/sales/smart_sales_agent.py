"""
Smart Sales Agent - بائع خدمات محترف يتكيف تلقائياً
يتعلم من كل عملية بيع ويتحسن مع الوقت
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from .smart_sales_db import SmartSalesDatabase

class SmartSalesAgent:
    """بائع ذكي يتكيف مع نوع الخدمة وسلوك العميل"""
    
    def __init__(self):
        self.db = SmartSalesDatabase()
        self._init_default_strategies()
    
    def _init_default_strategies(self):
        """تهيئة الاستراتيجيات الافتراضية"""
        # استراتيجيات عامة
        strategies = [
            {
                'service_type': 'website_analysis',
                'strategy_name': 'Free Analysis First',
                'approach': 'قدم تحليل مجاني أولاً ثم اعرض الخدمات المدفوعة',
                'message_template': '''🎯 تحليل مجاني لموقعك: {domain}

مرحباً،

قمت بتحليل موقعك ووجدت بعض النقاط المهمة:

📊 النتيجة الإجمالية: {score}/100

🔍 أهم الملاحظات:
{recommendations}

💡 الخدمات المقترحة:
{services}

🎁 عرض خاص:
- تحليل مجاني شامل
- خصم 20% على أول خدمة
- ضمان جودة 100%

📞 للتواصل:
واتساب: 01061245527
فودافون كاش: 01061245527''',
                'pricing_strategy': 'ابدأ بسعر منخفض ثم ارفع تدريجياً',
                'best_for_client_type': 'business_owners'
            },
            {
                'service_type': 'seo_optimization',
                'strategy_name': 'ROI Focused',
                'approach': 'ركز على العائد على الاستثمار والنتائج الملموسة',
                'message_template': '''📈 تحسين SEO لموقعك - زيادة الزيارات والمبيعات

مرحباً،

لاحظت أن موقعك {domain} لديه إمكانات كبيرة للنمو في محركات البحث.

🎯 النتائج المتوقعة:
- زيادة الزيارات بنسبة 150-300%
- تحسين ترتيب الكلمات المفتاحية
- زيادة المبيعات بنسبة 50-100%

💰 العائد على الاستثمار:
- الاستثمار: ${price}
- العائد المتوقع: ${expected_roi}
- فترة الاسترداد: 2-3 شهور

📞 للتواصل:
واتساب: 01061245527''',
                'pricing_strategy': 'سعّر حسب القيمة والنتائج المتوقعة',
                'best_for_client_type': 'business_owners'
            },
            {
                'service_type': 'content_writing',
                'strategy_name': 'Quality Samples',
                'approach': 'قدم عينات من أعمالك السابقة كدليل على الجودة',
                'message_template': '''✍️ خدمة كتابة محتوى احترافي

مرحباً،

أقدم خدمة كتابة محتوى احترافي تشمل:
- مقالات SEO
- محتوى مواقع
- منشورات سوشيال ميديا
- وصف منتجات

📝 عينات من أعمالي السابقة:
{samples}

💰 الأسعار:
- مقال 500 كلمة: $10
- مقال 1000 كلمة: $20
- محتوى موقع كامل: حسب المشروع

📞 للتواصل:
واتساب: 01061245527''',
                'pricing_strategy': 'سعّر حسب عدد الكلمات والجودة',
                'best_for_client_type': 'content_marketers'
            }
        ]
        
        for strategy in strategies:
            self.db.add_strategy(
                service_type=strategy['service_type'],
                strategy_name=strategy['strategy_name'],
                approach=strategy['approach'],
                message_template=strategy['message_template'],
                pricing_strategy=strategy['pricing_strategy'],
                best_for_client_type=strategy['best_for_client_type']
            )
    
    def analyze_service_request(self, service_type: str, client_info: Dict = None) -> Dict:
        """تحليل طلب الخدمة واقتراح أفضل استراتيجية"""
        
        # الحصول على أفضل الاستراتيجيات لهذا النوع من الخدمة
        best_strategies = self.db.get_best_strategies(service_type, limit=3)
        
        # الحصول على معلومات نوع الخدمة
        service_info = self.db.get_service_type(service_type)
        
        # تحليل سلوك العميل إذا كانت المعلومات متاحة
        client_profile = None
        if client_info and 'client_id' in client_info:
            client_profile = self.db.get_client_profile(
                client_info['client_id'], 
                service_type
            )
        
        # اختيار أفضل استراتيجية
        recommended_strategy = None
        if best_strategies:
            # إذا كان هناك ملف للعميل، اختر الاستراتيجية المناسبة لنوعه
            if client_profile and client_profile.get('behavior_pattern'):
                for strategy in best_strategies:
                    if strategy.get('best_for_client_type') == client_profile['behavior_pattern']:
                        recommended_strategy = strategy
                        break
            
            # إذا لم نجد استراتيجية مناسبة، استخدم الأفضل بشكل عام
            if not recommended_strategy:
                recommended_strategy = best_strategies[0]
        
        # الحصول على التكيف إذا كان متاحاً
        adaptation = None
        if client_profile:
            client_type = client_profile.get('behavior_pattern', 'general')
            adaptation = self.db.get_adaptation(service_type, client_type)
        
        return {
            'service_type': service_type,
            'service_info': service_info,
            'client_profile': client_profile,
            'recommended_strategy': recommended_strategy,
            'alternative_strategies': best_strategies[1:] if len(best_strategies) > 1 else [],
            'adaptation': adaptation,
            'confidence_level': self._calculate_confidence(recommended_strategy, client_profile)
        }
    
    def _calculate_confidence(self, strategy: Dict = None, client_profile: Dict = None) -> str:
        """حساب مستوى الثقة في التوصية"""
        if not strategy:
            return 'low'
        
        success_rate = strategy.get('success_rate', 0)
        usage_count = strategy.get('usage_count', 0)
        
        if success_rate >= 80 and usage_count >= 10:
            return 'very_high'
        elif success_rate >= 60 and usage_count >= 5:
            return 'high'
        elif success_rate >= 40:
            return 'medium'
        else:
            return 'low'
    
    def generate_sales_message(self, service_type: str, client_data: Dict, 
                              customization: Dict = None) -> str:
        """توليد رسالة بيع مخصصة"""
        
        analysis = self.analyze_service_request(service_type, client_data)
        strategy = analysis.get('recommended_strategy')
        
        if not strategy or not strategy.get('message_template'):
            return self._generate_generic_message(service_type, client_data)
        
        message = strategy['message_template']
        
        # تخصيص الرسالة
        if customization:
            for key, value in customization.items():
                message = message.replace(f'{{{key}}}', str(value))
        
        # تخصيص إضافي بناءً على سلوك العميل
        client_profile = analysis.get('client_profile')
        if client_profile:
            message = self._personalize_message(message, client_profile)
        
        return message
    
    def _personalize_message(self, message: str, client_profile: Dict) -> str:
        """تخصيص الرسالة بناءً على ملف العميل"""
        
        # تخصيص بناءً على حساسية السعر
        price_sensitivity = client_profile.get('price_sensitivity')
        if price_sensitivity == 'high':
            message += "\n\n💡 لدينا عروض خاصة وخصومات مناسبة لميزانيتك"
        elif price_sensitivity == 'low':
            message += "\n\n✨ نضمن لك أعلى جودة وأفضل النتائج"
        
        # تخصيص بناءً على سرعة اتخاذ القرار
        decision_speed = client_profile.get('decision_speed')
        if decision_speed == 'fast':
            message += "\n\n⚡ ابدأ الآن واحصل على نتائج سريعة"
        elif decision_speed == 'slow':
            message += "\n\n📅 خذ وقتك في التفكير، نحن هنا للإجابة على أي أسئلة"
        
        return message
    
    def _generate_generic_message(self, service_type: str, client_data: Dict) -> str:
        """توليد رسالة عامة إذا لم تكن هناك استراتيجية محددة"""
        
        domain = client_data.get('domain', 'موقعك')
        
        return f'''🎯 خدمة {service_type} احترافية

مرحباً،

أقدم خدمة {service_type} احترافية لـ {domain}

💡 الخدمات تشمل:
- تحليل شامل
- توصيات عملية
- تنفيذ احترافي
- متابعة مستمرة

📞 للتواصل:
واتساب: 01061245527
فودافون كاش: 01061245527

🚀 ابدأ الآن واحصل على نتائج مضمونة!'''
    
    def record_sale_outcome(self, sale_data: Dict) -> int:
        """تسجيل نتيجة عملية البيع والتعلم منها"""
        
        # تسجيل عملية البيع
        sale_id = self.db.record_sale(
            client_id=sale_data.get('client_id'),
            service_type=sale_data['service_type'],
            strategy_used=sale_data.get('strategy_used'),
            approach=sale_data.get('approach'),
            initial_price=sale_data.get('initial_price'),
            final_price=sale_data.get('final_price'),
            objections_handled=sale_data.get('objections_handled'),
            outcome=sale_data['outcome'],
            revenue=sale_data.get('revenue'),
            duration_days=sale_data.get('duration_days'),
            lessons_learned=sale_data.get('lessons_learned'),
            client_feedback=sale_data.get('client_feedback')
        )
        
        # تحديث إحصائيات الاستراتيجية
        if sale_data.get('strategy_id'):
            success = sale_data['outcome'] == 'success'
            self.db.update_strategy_stats(
                sale_data['strategy_id'],
                success,
                sale_data.get('revenue', 0)
            )
        
        # تسجيل سلوك العميل
        if sale_data.get('client_id'):
            self.db.record_client_behavior(
                client_id=sale_data['client_id'],
                service_type=sale_data['service_type'],
                behavior_pattern=sale_data.get('client_behavior'),
                objections=sale_data.get('objections_handled'),
                preferred_communication=sale_data.get('communication_channel'),
                price_sensitivity=sale_data.get('price_sensitivity'),
                decision_speed=sale_data.get('decision_speed'),
                success=sale_data['outcome'] == 'success'
            )
        
        # التعلم من الدروس المستفادة
        if sale_data.get('lessons_learned'):
            self._learn_from_experience(sale_data)
        
        return sale_id
    
    def _learn_from_experience(self, sale_data: Dict):
        """التعلم من التجربة وتحسين الاستراتيجيات"""
        
        service_type = sale_data['service_type']
        outcome = sale_data['outcome']
        lessons = sale_data.get('lessons_learned', '')
        
        # إذا كانت التجربة ناجحة، سجل التكيف الناجح
        if outcome == 'success':
            client_behavior = sale_data.get('client_behavior', 'general')
            strategy_used = sale_data.get('strategy_used', '')
            
            adaptation = f"استخدم {strategy_used} مع {client_behavior} - نجح بسبب: {lessons}"
            
            self.db.adapt_strategy(
                service_type=service_type,
                client_type=client_behavior,
                adaptation=adaptation,
                success=True,
                notes=lessons
            )
        
        # إذا فشلت التجربة، سجل ما يجب تجنبه
        elif outcome == 'failed':
            client_behavior = sale_data.get('client_behavior', 'general')
            
            adaptation = f"تجنب هذا النهج مع {client_behavior} - السبب: {lessons}"
            
            self.db.adapt_strategy(
                service_type=service_type,
                client_type=client_behavior,
                adaptation=adaptation,
                success=False,
                notes=lessons
            )
    
    def get_sales_performance(self, service_type: str = None, days: int = 30) -> Dict:
        """الحصول على أداء المبيعات"""
        
        analytics = self.db.get_sales_analytics(service_type, days)
        top_strategies = self.db.get_top_performing_strategies(service_type, limit=5)
        
        return {
            'analytics': analytics,
            'top_strategies': top_strategies,
            'period_days': days,
            'service_type': service_type or 'all'
        }
    
    def suggest_improvements(self, service_type: str = None) -> List[str]:
        """اقتراح تحسينات بناءً على البيانات"""
        
        suggestions = []
        
        # الحصول على التحليلات
        analytics = self.db.get_sales_analytics(service_type, days=30)
        
        # اقتراحات بناءً على معدل النجاح
        if analytics['success_rate'] < 50:
            suggestions.append("⚠️ معدل النجاح منخفض - راجع الاستراتيجيات المستخدمة")
        elif analytics['success_rate'] > 80:
            suggestions.append("✅ أداء ممتاز - حافظ على هذا المستوى")
        
        # اقتراحات بناءً على متوسط الإيرادات
        if analytics['avg_revenue'] < 50:
            suggestions.append("💡 حاول رفع الأسعار تدريجياً مع تحسين القيمة المقدمة")
        
        # اقتراحات بناءً على مدة الصفقات
        if analytics['avg_duration'] > 14:
            suggestions.append("⏱️ الصفقات تأخذ وقت طويل - حاول تسريع عملية البيع")
        
        # الحصول على أفضل الاستراتيجيات
        top_strategies = self.db.get_top_performing_strategies(service_type, limit=3)
        
        if top_strategies:
            best = top_strategies[0]
            suggestions.append(f"🎯 الاستراتيجية الأفضل: {best['strategy_name']} (نجاح {best['success_rate']:.1f}%)")
        
        return suggestions
