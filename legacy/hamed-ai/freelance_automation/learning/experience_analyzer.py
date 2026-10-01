"""
Experience Analyzer - محلل التجارب واستخراج الأنماط
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from core.logger import logger
from learning.experience_database import ExperienceDatabase

class ExperienceAnalyzer:
    """محلل التجارب - يستخرج الأنماط ويقدم توصيات"""
    
    def __init__(self):
        self.db = ExperienceDatabase()
        logger.info("ExperienceAnalyzer initialized")
    
    def analyze_before_decision(self, 
                               category: str, 
                               input_data: Dict) -> Dict:
        """تحليل قبل اتخاذ قرار - يستعلم من التجارب السابقة"""
        
        # الحصول على توصية
        recommendation = self.db.get_recommendation(category, input_data)
        
        # الحصول على معدل النجاح
        success_rate = self.db.get_success_rate(category, days=30)
        
        # الحصول على أفضل الاستراتيجيات
        best_strategies = self.db.get_best_strategies(category, limit=3)
        
        # الحصول على الأخطاء الشائعة
        recent_mistakes = self.db.get_recent_mistakes(limit=5)
        
        # بناء التحليل الشامل
        analysis = {
            'category': category,
            'timestamp': datetime.now().isoformat(),
            'recommendation': recommendation,
            'historical_stats': success_rate,
            'best_strategies': best_strategies,
            'common_mistakes': recent_mistakes,
            'confidence_level': self._calculate_confidence(recommendation, success_rate),
            'risk_assessment': self._assess_risk(recommendation, success_rate),
            'action_plan': self._generate_action_plan(recommendation, best_strategies)
        }
        
        logger.info(f"Analysis completed for {category}: {recommendation['recommendation']}")
        return analysis
    
    def _calculate_confidence(self, recommendation: Dict, stats: Dict) -> str:
        """حساب مستوى الثقة"""
        success_rate = stats.get('success_rate', 0)
        sample_size = stats.get('total', 0)
        
        if sample_size < 5:
            return 'low'
        elif success_rate > 80:
            return 'very_high'
        elif success_rate > 60:
            return 'high'
        elif success_rate > 40:
            return 'medium'
        else:
            return 'low'
    
    def _assess_risk(self, recommendation: Dict, stats: Dict) -> Dict:
        """تقييم المخاطر"""
        success_rate = stats.get('success_rate', 0)
        total_loss = stats.get('total_loss', 0)
        total_revenue = stats.get('total_revenue', 0)
        
        if success_rate > 70 and total_revenue > total_loss:
            risk_level = 'low'
            risk_factors = []
        elif success_rate > 50:
            risk_level = 'medium'
            risk_factors = ['معدل نجاح متوسط']
        else:
            risk_level = 'high'
            risk_factors = ['معدل نجاح منخفض', 'خسائر محتملة']
        
        if total_loss > total_revenue:
            risk_factors.append('خسائر تفوق الأرباح')
            risk_level = 'high'
        
        return {
            'level': risk_level,
            'factors': risk_factors,
            'mitigation': self._suggest_mitigation(risk_level)
        }
    
    def _suggest_mitigation(self, risk_level: str) -> List[str]:
        """اقتراحات لتقليل المخاطر"""
        if risk_level == 'low':
            return ['المتابعة العادية']
        elif risk_level == 'medium':
            return [
                'مراجعة دقيقة قبل التنفيذ',
                'بدء بمبلغ صغير',
                'تحديد نقاط التوقف'
            ]
        else:
            return [
                'تجنب هذا القرار حالياً',
                'البحث عن بدائل أكثر أماناً',
                'استشارة المدير الرئيسي',
                'تقسيم المخاطر على عدة خطوات'
            ]
    
    def _generate_action_plan(self, recommendation: Dict, strategies: List[Dict]) -> List[str]:
        """توليد خطة عمل"""
        plan = []
        
        if recommendation['recommendation'] == 'proceed':
            plan.append('✅ المتابعة مع القرار')
            if strategies:
                plan.append(f'استخدام استراتيجية: {strategies[0]["decision"]}')
            plan.append('تنفيذ مع مراقبة دقيقة')
            plan.append('تسجيل النتيجة للتعلم')
        elif recommendation['recommendation'] == 'caution':
            plan.append('⚠️ الحذر في التنفيذ')
            plan.append('مراجعة جميع التفاصيل')
            plan.append('بدء بخطوة صغيرة')
            plan.append('تجهيز خطة بديلة')
        else:
            plan.append('❌ عدم المتابعة')
            plan.append('البحث عن بدائل')
            plan.append('تحليل الأسباب')
        
        return plan
    
    def analyze_site_for_outreach(self, url: str, analysis_data: Dict) -> Dict:
        """تحليل موقع قبل إرسال رسالة"""
        
        # الحصول على تجارب سابقة مع مواقع مشابهة
        site_type = analysis_data.get('site_type', 'unknown')
        score = analysis_data.get('score', 0)
        
        # البحث عن تجارب مشابهة
        similar_experiences = self.db.get_similar_experiences(
            'site_outreach',
            {'site_type': site_type, 'score_range': self._get_score_range(score)},
            limit=10
        )
        
        # تحليل فعالية الرسائل
        message_effectiveness = self.db.get_message_effectiveness(limit=5)
        
        # حساب احتمالية النجاح
        if similar_experiences:
            successes = sum(1 for exp in similar_experiences if exp['success'])
            success_rate = (successes / len(similar_experiences)) * 100
        else:
            success_rate = 50  # افتراضي
        
        # تحديد أفضل قالب رسالة
        best_template = None
        if message_effectiveness:
            best_template = message_effectiveness[0]['message_template']
        
        return {
            'url': url,
            'site_type': site_type,
            'score': score,
            'recommendation': 'send' if success_rate > 40 else 'skip',
            'success_probability': success_rate,
            'best_template': best_template,
            'similar_cases': len(similar_experiences),
            'tips': self._generate_outreach_tips(site_type, score)
        }
    
    def _get_score_range(self, score: int) -> str:
        """تحويل النتيجة إلى نطاق"""
        if score < 40:
            return 'low'
        elif score < 70:
            return 'medium'
        else:
            return 'high'
    
    def _generate_outreach_tips(self, site_type: str, score: int) -> List[str]:
        """توليد نصائح للتواصل"""
        tips = []
        
        if score < 50:
            tips.append('الموقع فيه مشاكل كثيرة - ركز على الحلول السريعة')
        elif score < 70:
            tips.append('الموقع متوسط - قدم تحسينات محددة')
        else:
            tips.append('الموقع جيد - قدم خدمات متقدمة')
        
        if site_type == 'ecommerce':
            tips.append('ركز على زيادة المبيعات والتحويلات')
        elif site_type == 'blog':
            tips.append('ركز على SEO والمحتوى')
        elif site_type == 'business':
            tips.append('ركز على الاحترافية والصورة')
        
        return tips
    
    def analyze_purchase_opportunity(self, 
                                   product: str,
                                   supplier: str,
                                   price: float,
                                   quality: float) -> Dict:
        """تحليل فرصة شراء"""
        
        # البحث عن تجارب سابقة مع نفس المورد
        supplier_experiences = self.db.get_similar_experiences(
            'purchase',
            {'supplier': supplier},
            limit=10
        )
        
        # البحث عن تجارب مشابهة في السعر
        price_experiences = self.db.get_similar_experiences(
            'purchase',
            {'price_range': self._get_price_range(price)},
            limit=10
        )
        
        # حساب التوصية
        if supplier_experiences:
            successes = sum(1 for exp in supplier_experiences if exp['success'])
            supplier_success_rate = (successes / len(supplier_experiences)) * 100
        else:
            supplier_success_rate = 50
        
        # تقييم الجودة مقابل السعر
        value_score = quality / (price / 100) if price > 0 else 0
        
        # القرار
        if supplier_success_rate > 70 and value_score > 1:
            decision = 'approve'
            reason = 'مورد موثوق + قيمة جيدة'
        elif supplier_success_rate > 50:
            decision = 'review'
            reason = 'مراجعة إضافية مطلوبة'
        else:
            decision = 'reject'
            reason = 'مورد غير موثوق'
        
        return {
            'product': product,
            'supplier': supplier,
            'price': price,
            'quality': quality,
            'decision': decision,
            'reason': reason,
            'supplier_reliability': supplier_success_rate,
            'value_score': value_score,
            'similar_experiences': len(supplier_experiences)
        }
    
    def _get_price_range(self, price: float) -> str:
        """تحويل السعر إلى نطاق"""
        if price < 50:
            return 'low'
        elif price < 200:
            return 'medium'
        else:
            return 'high'
    
    def generate_learning_report(self, days: int = 30) -> Dict:
        """توليد تقرير التعلم"""
        
        # ملخص التعلم
        summary = self.db.get_learning_summary()
        
        # إحصائيات تحليل المواقع
        site_stats = self.db.get_site_analysis_stats()
        
        # رؤى الشراء
        purchase_insights = self.db.get_purchase_insights()
        
        # رؤى التفاوض
        negotiation_insights = self.db.get_negotiation_insights()
        
        # الأخطاء والدروس
        recent_mistakes = self.db.get_recent_mistakes(limit=10)
        
        return {
            'period_days': days,
            'generated_at': datetime.now().isoformat(),
            'learning_summary': summary,
            'site_analysis': site_stats,
            'purchase_insights': purchase_insights,
            'negotiation_insights': negotiation_insights,
            'recent_mistakes': recent_mistakes,
            'key_lessons': self._extract_key_lessons(recent_mistakes),
            'improvement_areas': self._identify_improvement_areas(summary)
        }
    
    def _extract_key_lessons(self, mistakes: List[Dict]) -> List[str]:
        """استخراج الدروس الرئيسية"""
        lessons = []
        
        for mistake in mistakes:
            if mistake.get('lesson'):
                lessons.append(mistake['lesson'])
        
        # إزالة التكرار
        unique_lessons = list(set(lessons))
        return unique_lessons[:10]
    
    def _identify_improvement_areas(self, summary: Dict) -> List[Dict]:
        """تحديد مجالات التحسين"""
        improvements = []
        
        for category, stats in summary['categories'].items():
            if stats['total'] > 0 and stats['success_rate'] < 60:
                improvements.append({
                    'area': category,
                    'current_rate': stats['success_rate'],
                    'target_rate': 70,
                    'gap': 70 - stats['success_rate'],
                    'priority': 'high' if stats['success_rate'] < 40 else 'medium'
                })
        
        # ترتيب حسب الأولوية
        improvements.sort(key=lambda x: x['gap'], reverse=True)
        return improvements
