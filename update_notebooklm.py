"""
Build local NotebookLM context files for the DYT_01 project.

This script does not connect to Google directly. It keeps the project-side
NotebookLM source files current so they can be imported or copied into the
NotebookLM notebook linked below.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOK_ID = "5e64f86d-3f1b-44bd-a5c0-067fd839e3a5"
NOTEBOOK_URL = f"https://notebooklm.google.com/notebook/{NOTEBOOK_ID}"


PROJECT_PROFILE = {
    "name": "DYT_01 / SEN V3",
    "notebook_id": NOTEBOOK_ID,
    "notebook_url": NOTEBOOK_URL,
    "summary": (
        "Hệ thống tự động hóa affiliate/content với các worker tạo nội dung, "
        "quản lý campaign, link Accesstrade, lịch đăng bài và monitoring."
    ),
    "active_focus": [
        "Chuẩn hóa dữ liệu NotebookLM làm nguồn ngữ cảnh dự án.",
        "Theo dõi campaign Shopee tháng 6/2026.",
        "Theo dõi các link Accesstrade tài chính đang hoạt động.",
        "Duy trì pipeline worker: content, affiliate, posting và monitor.",
    ],
}


SHOPEE_CAMPAIGN_JUNE_2026 = {
    "campaigns": [
        {
            "name": "1.6 Opening Sale",
            "date": "2026-06-01",
            "url": "https://shopee.vn/m/6-6",
            "description": "Mở màn siêu sale - siêu nhanh, siêu rẻ.",
        },
        {
            "name": "6.6 Mid Year Mega Sale",
            "date": "2026-06-06",
            "url": "https://shopee.vn/m/6-6",
            "description": "Siêu sale giữa năm - giảm đến 50%.",
        },
        {
            "name": "15.6 Mid-month Sale",
            "date": "2026-06-15",
            "url": "https://shopee.vn/m/15-sale-giua-thang",
            "description": "Sale giữa tháng - Voucher Xtra 6 triệu.",
        },
        {
            "name": "25.6 Payday Sale",
            "date": "2026-06-25",
            "url": "https://shopee.vn/m/sale-cuoi-thang-don-luong-ve",
            "description": "Lương về sale to - giảm 20% mỗi ngày.",
        },
    ],
    "daily_themes": [
        {
            "day": "Tuesday",
            "theme": "Dress up & Make up",
            "vietnamese": "Làm đẹp - Mặc chất",
        },
        {
            "day": "Wednesday",
            "theme": "Low Price Day",
            "vietnamese": "Thứ 4 siêu rẻ",
        },
        {
            "day": "Thursday",
            "theme": "VCX",
            "vietnamese": "Ngày hội voucher",
        },
        {
            "day": "Friday",
            "theme": "In-Stock, Ships Fast",
            "vietnamese": "Hàng sẵn kho - Giao nhanh",
        },
        {
            "day": "Weekend",
            "theme": "Entertainment Weekend",
            "vietnamese": "Cuối tuần giải trí",
        },
    ],
}


ACCESSTRADE_FINANCE_LINKS = [
    {
        "name": "TPBANK CREATOR",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6767399642708413705?sub4=sen_v3",
    },
    {
        "name": "VPBank - Vay Tín chấp",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6822308958202075636?sub4=sen_v3",
    },
    {
        "name": "Chứng khoán Maybank",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6827321992129624253?sub4=sen_v3",
    },
    {
        "name": "AppMax Vay Nhanh",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6873138885445764645?sub4=sen_v3",
    },
    {
        "name": "HDBank - Thẻ tín dụng",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6877351644194955800?sub4=sen_v3",
    },
    {
        "name": "Chứng khoán Kafi X",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6896341778738303892?sub4=sen_v3",
    },
    {
        "name": "KIS",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6923208811031507234?sub4=sen_v3",
    },
    {
        "name": "BIDV CN1",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6933871567339046924?sub4=sen_v3",
    },
    {
        "name": "iShinhan Vay IOS",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6949939948611548600?sub4=sen_v3",
    },
    {
        "name": "iShinhan Vay Android",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6949942463850829113?sub4=sen_v3",
    },
    {
        "name": "VPBank SenID",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6985504292608237862?sub4=sen_v3",
    },
    {
        "name": "TPBank",
        "url": "https://go.isclix.com/deep_link/v5/6983938396644077046/6985504292608237863?sub4=sen_v3",
    },
]


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_markdown(updated_at: str) -> str:
    lines = [
        "# DYT_01 / SEN V3 - NotebookLM Project Context",
        "",
        f"Updated: {updated_at}",
        f"NotebookLM: {NOTEBOOK_URL}",
        "",
        "## Project Summary",
        "",
        PROJECT_PROFILE["summary"],
        "",
        "## Active Focus",
        "",
    ]

    lines.extend(f"- {item}" for item in PROJECT_PROFILE["active_focus"])

    lines.extend(
        [
            "",
            "## Shopee Campaigns - June 2026",
            "",
        ]
    )
    for campaign in SHOPEE_CAMPAIGN_JUNE_2026["campaigns"]:
        lines.extend(
            [
                f"### {campaign['name']}",
                f"- Date: {campaign['date']}",
                f"- Link: {campaign['url']}",
                f"- Notes: {campaign['description']}",
                "",
            ]
        )

    lines.extend(["## Daily Themes", ""])
    for theme in SHOPEE_CAMPAIGN_JUNE_2026["daily_themes"]:
        lines.append(
            f"- {theme['day']}: {theme['theme']} ({theme['vietnamese']})"
        )

    lines.extend(["", "## Active Accesstrade Finance Links", ""])
    for index, link in enumerate(ACCESSTRADE_FINANCE_LINKS, start=1):
        lines.extend([f"{index}. {link['name']}", f"   {link['url']}"])

    lines.extend(
        [
            "",
            "## Recommended Operating Commands",
            "",
            "- `python start_promotion.py`",
            "- `python marketing_content.py`",
            "- `python get_accesstrade_campaigns.py`",
            "- `python update_notebooklm.py`",
            "",
        ]
    )
    return "\n".join(lines)


def build_notebooks_data(updated_at: str, markdown_content: str) -> dict:
    return {
        "notebooks": {
            NOTEBOOK_ID: {
                "id": NOTEBOOK_ID,
                "name": "DYT_01 - Affiliate Campaign",
                "description": PROJECT_PROFILE["summary"],
                "url": NOTEBOOK_URL,
                "created_at": "2026-06-04T00:00:00",
                "updated_at": updated_at,
                "sources": [
                    {
                        "id": "src_project_context",
                        "name": "DYT_01 Project Context",
                        "content": markdown_content,
                        "added_at": updated_at,
                    }
                ],
                "notes": PROJECT_PROFILE["active_focus"],
            }
        },
        "conversations": {},
        "updated_at": updated_at,
    }


def main() -> None:
    updated_at = datetime.now().isoformat(timespec="seconds")

    campaign_payload = {
        "last_update": updated_at,
        "notebook_url": NOTEBOOK_URL,
        **SHOPEE_CAMPAIGN_JUNE_2026,
    }
    write_json(ROOT / "shopee_campaign_2026_06.json", campaign_payload)

    markdown_content = build_markdown(updated_at)
    (ROOT / "notebooklm_export.md").write_text(markdown_content, encoding="utf-8")
    (ROOT / "notebooklm_source.md").write_text(markdown_content, encoding="utf-8")

    notebooks_data = build_notebooks_data(updated_at, markdown_content)
    write_json(ROOT / "notebooks_data.json", notebooks_data)

    print("=" * 60)
    print("NotebookLM project context updated")
    print("=" * 60)
    print(f"Notebook: {NOTEBOOK_URL}")
    print("Wrote: shopee_campaign_2026_06.json")
    print("Wrote: notebooklm_export.md")
    print("Wrote: notebooklm_source.md")
    print("Wrote: notebooks_data.json")


if __name__ == "__main__":
    main()
