code = '''
def analyze_conversion_strategies(top_campaigns: list) -> dict:
    """Phân tích chiến lược có chuyển đổi cao từ Accesstrade + data nội bộ."""
    strategies = []
    for c in top_campaigns:
        score = c.get("_score", 0)
        comm = float(c.get("commission_rate") or c.get("commission") or 0)
        strategy = {
            "campaign": c.get("name") or c.get("campaign_name"),
            "score": score,
            "recommended_theme": "affiliate" if "sale" in str(c.get("name","")).lower() or comm > 0.2 else "motivational",
            "best_posting_hours": [8,9,12,18,19,20,21],
            "conversion_potential": "HIGH" if score > 30 else "MEDIUM" if score > 15 else "LOW",
            "action": "Create content promoting " + str(c.get("name")) + " with strong CTA + affiliate link. Post at peak hours."
        }
        strategies.append(strategy)
    
    return {
        "top_strategies": strategies,
        "summary": "Ưu tiên campaigns có score cao từ commission + historical conversions. Kết hợp với PostingOptimizer để chọn giờ tối ưu."
    }

if __name__ == "__main__":
    top = run_picker()
    if top:
        analysis = analyze_conversion_strategies(top)
        print("\\n📈 CHIẾN LƯỢC CHUYỂN ĐỔI CAO TỪ ACCESSTRADE:")
        for s in analysis["top_strategies"]:
            print("  - " + s["campaign"] + ": " + s["conversion_potential"] + " | Theme: " + s["recommended_theme"] + " | " + s["action"])
        print("\\n" + analysis["summary"])
'''
with open('auto_picker.py', 'a', encoding='utf-8') as f:
    f.write(code)
print('Appended the analysis function.')
