from auto_picker import analyze_conversion_strategies, _get_demo_campaigns
print("=== Testing optimized Accesstrade analysis for high conversion ===")
demo = _get_demo_campaigns()
print("Demo campaigns loaded:", len(demo))
top = sorted(demo, key=lambda x: float(x.get("commission_rate",0)), reverse=True)[:5]
for c in top:
    c["_score"] = 50 + (float(c.get("commission_rate",0))*100)  # mock enhanced score
print("Top campaigns for analysis:")
for c in top:
    print(f"  {c['name']} comm={c.get('commission_rate')} score={c['_score']}")
analysis = analyze_conversion_strategies(top)
print("\n=== HIGH CONVERSION STRATEGIES FROM ACCESSTRADE ===")
for s in analysis["top_strategies"]:
    print(f"- {s['campaign']}: {s['conversion_potential']} | Recommended theme: {s['recommended_theme']} | {s['action']}")
print("\nSummary:", analysis["summary"])
print("\n💡 Use these strategies with content_worker + schedule_optimized_posts for max ROI.")