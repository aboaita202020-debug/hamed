from .models import Offer, Opportunity


def build_store_offer(opportunity: Opportunity, prospect_name: str = "صاحب المتجر") -> Offer:
    return Offer(
        subject="مراجعة مخصصة لمتجرك",
        message=(
            f"أهلًا {prospect_name}، أثناء المراجعة ظهرت لنا هذه النقطة: {opportunity.problem} "
            "بدل ما نفترض السبب، نقترح اختبارًا صغيرًا قابلًا للقياس. "
            "إذا حابب، نرسل لك ملخص الملاحظات والخطوات المقترحة."
        ),
        service=opportunity.solution,
        next_step="إرسال التدقيق المختصر ثم الاتفاق على تجربة أولية",
        evidence=opportunity.evidence,
    )
