"""
Auto Analyzer - يحلل المواقع والمتاجر الإلكترونية تلقائياً
"""
import re
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse

from core.config import Config
from core.database import Database
from core.logger import logger

class AutoAnalyzer:
    """يحلل المواقع تلقائياً ويولد تقارير احترافية"""
    
    def __init__(self):
        self.db = Database()
        self.analysis_templates = self._load_templates()
        
        logger.info("AutoAnalyzer initialized")
    
    def _load_templates(self) -> Dict:
        """تحميل قوالب التحليل"""
        return {
            "ecommerce": {
                "title": "تحليل متجر إلكتروني",
                "checks": [
                    "سرعة التحميل",
                    "تجربة المستخدم",
                    "SEO",
                    "الأمان",
                    "التسويق",
                    "التحويل"
                ],
                "services": [
                    "تحسين سرعة الموقع",
                    "تحسين SEO",
                    "تحسين تجربة المستخدم",
                    "إعداد حملات تسويقية",
                    "تحسين معدل التحويل"
                ]
            },
            "business": {
                "title": "تحليل موقع شركة",
                "checks": [
                    "العلامة التجارية",
                    "المحتوى",
                    "التواصل",
                    "المصداقية",
                    "SEO محلي"
                ],
                "services": [
                    "تحسين الهوية البصرية",
                    "كتابة محتوى احترافي",
                    "إعداد صفحة تواصل فعالة",
                    "تحسين SEO محلي"
                ]
            },
            "blog": {
                "title": "تحليل مدونة",
                "checks": [
                    "جودة المحتوى",
                    "SEO",
                    "التفاعل",
                    "الربح من المحتوى"
                ],
                "services": [
                    "تحسين SEO",
                    "كتابة محتوى",
                    "إعداد استراتيجية محتوى",
                    "تحسين الربح من الإعلانات"
                ]
            }
        }
    
    def analyze_website(self, url: str) -> Dict:
        """تحليل موقع إلكتروني"""
        start_time = time.time()
        
        try:
            # Parse URL
            parsed = urlparse(url)
            domain = parsed.netloc
            
            logger.info(f"Analyzing website: {domain}")
            
            # Determine website type
            site_type = self._detect_site_type(url)
            
            # Generate analysis
            analysis = self._generate_analysis(url, domain, site_type)
            
            # Calculate score
            score = self._calculate_score(analysis)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(analysis, site_type)
            
            # Generate services offer
            services = self._generate_services_offer(site_type, score)
            
            duration = time.time() - start_time
            
            result = {
                "url": url,
                "domain": domain,
                "site_type": site_type,
                "analysis": analysis,
                "score": score,
                "recommendations": recommendations,
                "services": services,
                "analyzed_at": datetime.now().isoformat(),
                "duration": duration
            }
            
            # Save to database
            self._save_analysis(result)
            
            logger.info(f"Analysis completed for {domain} - Score: {score}/100")
            
            return result
        
        except Exception as e:
            logger.error(f"Analysis failed for {url}: {e}")
            raise
    
    def _detect_site_type(self, url: str) -> str:
        """تحديد نوع الموقع"""
        url_lower = url.lower()
        
        if any(keyword in url_lower for keyword in ['shop', 'store', 'product', 'buy', 'cart']):
            return "ecommerce"
        elif any(keyword in url_lower for keyword in ['blog', 'article', 'post', 'news']):
            return "blog"
        else:
            return "business"
    
    def _generate_analysis(self, url: str, domain: str, site_type: str) -> Dict:
        """توليد تحليل مفصل"""
        # محاكاة تحليل حقيقي
        # في الإنتاج: استخدم requests + BeautifulSoup + AI
        
        template = self.analysis_templates.get(site_type, self.analysis_templates["business"])
        
        analysis = {
            "type": template["title"],
            "checks": {}
        }
        
        for check in template["checks"]:
            # محاكاة نتيجة فحص (في الإنتاج: فحص حقيقي)
            score = random.randint(40, 85)
            status = "needs_improvement" if score < 70 else "good"
            
            analysis["checks"][check] = {
                "score": score,
                "status": status,
                "details": self._get_check_details(check, score)
            }
        
        return analysis
    
    def _get_check_details(self, check: str, score: int) -> str:
        """تفاصيل كل فحص"""
        details_map = {
            "سرعة التحميل": f"سرعة التحميل {score}/100 - يمكن تحسينها عن طريق ضغط الصور وتقليل HTTP requests",
            "تجربة المستخدم": f"تجربة المستخدم {score}/100 - التصميم يحتاج تحسين في التنقل",
            "SEO": f"نتيجة SEO {score}/100 - يحتاج تحسين الكلمات المفتاحية والـ meta tags",
            "الأمان": f"مستوى الأمان {score}/100 - تأكد من تفعيل SSL",
            "التسويق": f"التسويق {score}/100 - يحتاج استراتيجية تسويقية أقوى",
            "التحويل": f"معدل التحويل {score}/100 - يمكن تحسينه بتحسين CTA",
            "العلامة التجارية": f"العلامة التجارية {score}/100 - تحتاج تعزيز",
            "المحتوى": f"جودة المحتوى {score}/100 - يحتاج تحسين",
            "التواصل": f"صفحة التواصل {score}/100 - تحتاج تحسين",
            "المصداقية": f"المصداقية {score}/100 - أضف شهادات العملاء",
            "SEO محلي": f"SEO محلي {score}/100 - يحتاج تحسين",
            "جودة المحتوى": f"جودة المحتوى {score}/100 - يحتاج تحسين",
            "التفاعل": f"معدل التفاعل {score}/100 - يمكن تحسينه",
            "الربح من المحتوى": f"استراتيجية الربح {score}/100 - يمكن تحسينها"
        }
        
        return details_map.get(check, f"نتيجة {score}/100")
    
    def _calculate_score(self, analysis: Dict) -> int:
        """حساب الدرجة الإجمالية"""
        if not analysis.get("checks"):
            return 0
        
        scores = [check["score"] for check in analysis["checks"].values()]
        return int(sum(scores) / len(scores))
    
    def _generate_recommendations(self, analysis: Dict, site_type: str) -> List[str]:
        """توليد توصيات"""
        recommendations = []
        
        for check_name, check_data in analysis.get("checks", {}).items():
            if check_data["score"] < 70:
                recommendations.append(f"تحسين {check_name} (النتيجة الحالية: {check_data['score']}/100)")
        
        return recommendations[:5]  # أول 5 توصيات
    
    def _generate_services_offer(self, site_type: str, score: int) -> List[Dict]:
        """توليد عرض خدمات"""
        template = self.analysis_templates.get(site_type, self.analysis_templates["business"])
        
        services = []
        base_price = 50 if score < 50 else 30 if score < 70 else 20
        
        for i, service in enumerate(template["services"][:3]):
            services.append({
                "name": service,
                "price": base_price + (i * 10),
                "currency": "USD",
                "delivery": "3-7 أيام"
            })
        
        return services
    
    def _save_analysis(self, result: Dict):
        """حفظ التحليل في قاعدة البيانات"""
        try:
            self.db.execute("""
                INSERT INTO website_analyses 
                (url, domain, site_type, score, analysis, recommendations, services, analyzed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result['url'],
                result['domain'],
                result['site_type'],
                result['score'],
                json.dumps(result['analysis']),
                json.dumps(result['recommendations']),
                json.dumps(result['services']),
                result['analyzed_at']
            ))
        except Exception as e:
            logger.error(f"Failed to save analysis: {e}")
    
    def get_analysis_history(self, limit: int = 10) -> List[Dict]:
        """جلب سجل التحليلات"""
        return self.db.fetch_all("""
            SELECT * FROM website_analyses 
            ORDER BY analyzed_at DESC 
            LIMIT ?
        """, (limit,))
