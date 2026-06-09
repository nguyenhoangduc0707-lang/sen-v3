print('=== Running optimized Accesstrade high conversion analysis ===')

def _get_demo_campaigns():
    return [
        {'id': 'CAMP_001', 'name': 'ACFC Double 5 Sale - Thời trang Mỹ Phẩm', 'commission_rate': 0.12, 'gross_commission': 500000, 'cookie_duration': 30, 'approval_status': 'approved', 'merchant_name': 'ACFC', 'category': 'fashion'},
        {'id': 'CAMP_002', 'name': 'Calvin Klein Double Day', 'commission_rate': 0.10, 'gross_commission': 300000, 'cookie_duration': 45, 'approval_status': 'approved', 'merchant_name': 'CalvinKlein', 'category': 'fashion'},
        {'id': 'CAMP_003', 'name': 'Tommy Hilfiger Sale', 'commission_rate': 0.08, 'gross_commission': 250000, 'cookie_duration': 30, 'approval_status': 'approved', 'merchant_name': 'Tommy', 'category': 'fashion'},
        {'id': 'CAMP_004', 'name': 'Mango Special Price', 'commission_rate': 0.15, 'gross_commission': 400000, 'cookie_duration': 60, 'approval_status': 'approved', 'merchant_name': 'Mango', 'category': 'fashion'},
        {'id': 'CAMP_005', 'name': 'AI Tool - Notion AI Affiliate', 'commission_rate': 0.25, 'gross_commission': 100000, 'cookie_duration': 90, 'approval_status': 'approved', 'merchant_name': 'Notion', 'category': 'tech ai'},
    ]

def _score(c):
    commission = float(c.get('commission_rate') or c.get('commission') or 0)
    gross = float(c.get('gross_commission') or 0)
    cookie = int(c.get('cookie_duration') or 0)
    approved = 10 if str(c.get('approval_status','')).lower() in ('approved','active','1') else 0
    category = str(c.get('category') or c.get('merchant_name') or '').lower()
    cat_bonus = 5 if any(k in category for k in ['fashion', 'beauty', 'tech', 'ai', 'app']) else 0
    conv_bonus = 10  # mock from internal data
    base = commission * 60 + gross * 0.001 + cookie * 0.8 + approved + cat_bonus + conv_bonus
    return round(base, 4)

def analyze_conversion_strategies(top_campaigns):
    strategies = []
    for c in top_campaigns:
        score = c.get('_score', 0)
        comm = float(c.get('commission_rate') or 0)
        strategy = {
            'campaign': c.get('name') or c.get('campaign_name'),
            'score': score,
            'recommended_theme': 'affiliate' if 'sale' in str(c.get('name','')).lower() or comm > 0.2 else 'motivational',
            'best_posting_hours': [8,9,12,18,19,20,21],
            'conversion_potential': 'HIGH' if score > 30 else 'MEDIUM' if score > 15 else 'LOW',
            'action': 'Create content promoting ' + c.get('name') + ' with strong CTA + affiliate link. Post at peak hours.'
        }
        strategies.append(strategy)
    return {
        'top_strategies': strategies,
        'summary': 'Ưu tiên campaigns có score cao từ commission + historical conversions. Kết hợp với PostingOptimizer để chọn giờ tối ưu.'
    }

demo = _get_demo_campaigns()
for c in demo:
    c['_score'] = _score(c)
top = sorted(demo, key=lambda x: x['_score'], reverse=True)[:5]
print('Top campaigns:')
for c in top:
    print('  ' + c['name'] + ' score=' + str(c['_score']) + ' comm=' + str(c.get('commission_rate')))
analysis = analyze_conversion_strategies(top)
print('\n=== HIGH CONVERSION STRATEGIES ===')
for s in analysis['top_strategies']:
    print('- ' + s['campaign'] + ': ' + s['conversion_potential'] + ' | Theme: ' + s['recommended_theme'] + ' | ' + s['action'])
print('\n' + analysis['summary'])
print('\n💡 Next: Use these with schedule_optimized_posts.py and content generation for high ROI on Accesstrade.')