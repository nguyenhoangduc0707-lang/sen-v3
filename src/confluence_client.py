"""
Confluence Cloud Client for DYT-01 integration.
Allows reading/writing content from Confluence to use as content source for FB posting,
or publishing generated content back to Confluence.

Usage:
- Configure in .env:
  CONFLUENCE_BASE_URL=https://your-site.atlassian.net/wiki
  CONFLUENCE_EMAIL=your@email.com
  CONFLUENCE_API_TOKEN=your_api_token
  CONFLUENCE_SPACE_KEY=SPACEKEY

- Get API token from: https://id.atlassian.com/manage-profile/security/api-tokens
"""
import os
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class ConfluenceClient:
    def __init__(self, base_url: str = None, email: str = None, api_token: str = None, space_key: str = None):
        self.base_url = base_url or os.getenv("CONFLUENCE_BASE_URL", "").rstrip("/")
        self.email = email or os.getenv("CONFLUENCE_EMAIL")
        self.api_token = api_token or os.getenv("CONFLUENCE_API_TOKEN")
        self.space_key = space_key or os.getenv("CONFLUENCE_SPACE_KEY")

        if not all([self.base_url, self.email, self.api_token]):
            raise ValueError("Missing Confluence credentials. Set CONFLUENCE_BASE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN in .env")

        self.auth = (self.email, self.api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.api_base = f"{self.base_url}/rest/api"

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.api_base}{endpoint}"
        response = requests.request(method, url, auth=self.auth, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def get_page(self, page_id: str) -> Dict:
        """Get full page content by ID."""
        return self._request("GET", f"/content/{page_id}?expand=body.storage,version,space")

    def get_page_content(self, page_id: str) -> str:
        """Get only the HTML body content."""
        page = self.get_page(page_id)
        return page.get("body", {}).get("storage", {}).get("value", "")

    def search_pages(self, cql: str, limit: int = 25) -> List[Dict]:
        """
        Search pages using CQL (Confluence Query Language).
        Example CQL for approved FB content:
          space = "YOURSPACE" AND label = "approved" AND label = "fb-post" 
          AND "scheduled-date" > now()
        """
        params = {"cql": cql, "limit": limit, "expand": "body.storage,metadata.labels"}
        result = self._request("GET", "/content/search", params=params)
        return result.get("results", [])

    def create_page(self, title: str, body_html: str, parent_id: str = None, labels: List[str] = None) -> Dict:
        """Create a new page in the space."""
        data = {
            "type": "page",
            "title": title,
            "space": {"key": self.space_key},
            "body": {
                "storage": {
                    "value": body_html,
                    "representation": "storage"
                }
            }
        }
        if parent_id:
            data["ancestors"] = [{"id": parent_id}]

        page = self._request("POST", "/content", json=data)

        if labels:
            self.add_labels(page["id"], labels)

        return page

    def update_page(self, page_id: str, title: str, body_html: str, version_number: int) -> Dict:
        """Update existing page (requires current version number)."""
        data = {
            "version": {"number": version_number + 1},
            "title": title,
            "type": "page",
            "body": {
                "storage": {
                    "value": body_html,
                    "representation": "storage"
                }
            }
        }
        return self._request("PUT", f"/content/{page_id}", json=data)

    def add_labels(self, page_id: str, labels: List[str]):
        """Add labels to a page."""
        data = [{"prefix": "global", "name": label} for label in labels]
        self._request("POST", f"/content/{page_id}/label", json=data)

    def get_page_properties(self, page_id: str) -> Dict:
        """
        Get page properties (useful when using Page Properties macro).
        Note: Page Properties are stored as content properties.
        """
        try:
            props = self._request("GET", f"/content/{page_id}/property")
            return {p["key"]: p["value"] for p in props.get("results", [])}
        except:
            return {}

    def find_approved_fb_content(self, days_ahead: int = 7) -> List[Dict]:
        """
        Helper: Find pages ready for FB posting using CQL.
        Best used together with:
          - label = "fb-approved" on the page
          - label != "posted"
          - Page Properties macro with fields "scheduled-date" (YYYY-MM-DD) and "fanpage-key"
        """
        today = datetime.now().strftime("%Y-%m-%d")
        future = (datetime.now() + __import__("datetime").timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        cql = (
            f'space = "{self.space_key}" '
            'AND label = "fb-approved" '
            'AND label != "posted" '
            f'AND "scheduled-date" >= "{today}" '
            f'AND "scheduled-date" < "{future}"'
        )
        return self.search_pages(cql)

    def mark_as_posted(self, page_id: str):
        """Add 'posted' label and optionally update a property."""
        self.add_labels(page_id, ["posted"])
        # You can also update a custom property "post-status" = "published" here if using Page Properties

# Example usage (for testing):
if __name__ == "__main__":
    client = ConfluenceClient()
    pages = client.find_approved_fb_content()
    print(f"Found {len(pages)} approved pages ready for FB")
    for p in pages:
        print(f"  - {p['title']} (id: {p['id']})")