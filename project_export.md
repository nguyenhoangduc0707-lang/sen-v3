# DYT_01 - Export for NotebookLM

**Exported:** 2026-06-01T21:25:46.738269

## 📊 Statistics

- Total files: 4976
- Database tables: 12
- Export size: 21162.77 KB

## 🗄️ Database Content

### Table: campaigns
Rows: 18

```json
[
  {
    "id": 1001,
    "name": "Chương trình Tai nghe không dây",
    "commission_rate": null,
    "commission_fixed": null,
    "cpc_price": 300.0,
    "description": "Mô tả chi tiết về chương trình affiliate Tai nghe không dây...",
    "url": "https://shopee.vn/tai-nghe-không-dây"
  },
  {
    "id": 1002,
    "name": "Chương trình Điện thoại thông minh",
    "commission_rate": null,
    "commission_fixed": null,
    "cpc_price": 300.0,
    "description": "Mô tả chi tiết về chương trình affiliate Điện thoại thông minh...",
    "url": "https://shopee.vn/điện-thoại-thông-minh"
  },
  {
    "id": 1003,
    "name": "Chương trình Bàn phím cơ",
    "commission_rate": null,
    "commission_fixed": 100000.0,
    "cpc_price": null,
    "description": "Mô tả chi tiết về chương trình affiliate Bàn phím cơ...",
    "url": "https://shopee.vn/bàn-phím-cơ"
  },
  {
    "id": 1004,
    "name": "Chương trình Bàn phím cơ",
    "commission_rate": null,
    "commission_fixed": null,
    "cpc_price": 300.0,
    "description": "Mô tả chi tiết về chương trình affiliate Bàn phím cơ...",
    "url": "https://shopee.vn/bàn-phím-cơ"
  },
  {
    "id": 1005,
    "name": "Chương trình Áo thun thể thao",
    "commission_rate": null,
    "commission_fixed": null,
    "cpc_price": 300.0,
    "description": "Mô tả chi tiết về chương trình affiliate Áo thun thể thao...",
    "url": "https://shopee.vn/áo-thun-thể-thao"
  }
]
```

### Table: users
Rows: 1

```json
[
  {
    "id": 1,
    "username": "admin",
    "display_name": "Administrator",
    "email": "admin@example.com",
    "phone": null,
    "password_hash": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
    "is_admin": 0,
    "created_at": "2026-05-30 04:57:40.290605"
  }
]
```

### Table: workers
Rows: 2

```json
[
  {
    "id": 1,
    "name": "content_creator",
    "category": null,
    "version": "unknown",
    "last_heartbeat": "2026-05-30 06:16:15.952992",
    "status": "ACTIVE"
  },
  {
    "id": 2,
    "name": "facebook_autoposter",
    "category": null,
    "version": "unknown",
    "last_heartbeat": "2026-05-29 16:28:36.215726",
    "status": "ACTIVE"
  }
]
```

### Table: stealth_data
Rows: 0

### Table: dead_letter
Rows: 6

```json
[
  {
    "id": 1,
    "original_task_id": 1,
    "category": "content",
    "worker_name": "content_creator",
    "payload": "{\"campaign_id\": 1001, \"priority\": \"normal\"}",
    "failure_reason": "DB error: connection to server at \"localhost\" (::1), port 5432 failed: FATAL:  password authentication failed for user \"sen_user\"\n",
    "failed_at": "2026-05-29 14:34:43.885516"
  },
  {
    "id": 2,
    "original_task_id": 2,
    "category": "content",
    "worker_name": "content_creator",
    "payload": "{\"campaign_id\": 1001, \"priority\": \"normal\"}",
    "failure_reason": "DB error: connection to server at \"localhost\" (::1), port 5432 failed: FATAL:  password authentication failed for user \"sen_user\"\n",
    "failed_at": "2026-05-29 14:35:47.069443"
  },
  {
    "id": 3,
    "original_task_id": 3,
    "category": "content",
    "worker_name": "content_creator",
    "payload": "{\"campaign_id\": 1001, \"priority\": \"normal\"}",
    "failure_reason": "DB error: connection to server at \"localhost\" (::1), port 5432 failed: FATAL:  password authentication failed for user \"sen_user\"\n",
    "failed_at": "2026-05-29 14:40:35.281090"
  },
  {
    "id": 4,
    "original_task_id": 17,
    "category": null,
    "worker_name": "content_creator",
    "payload": "{\"priority\": \"high\", \"campaign_id\": 1016}",
    "failure_reason": "Campaign 1016 not found",
    "failed_at": "2026-05-30 05:34:56.313634"
  },
  {
    "id": 5,
    "original_task_id": 18,
    "category": null,
    "worker_name": "content_creator",
    "payload": "{\"priority\": \"normal\", \"campaign_id\": 2001}",
    "failure_reason": "Campaign 2001 not found",
    "failed_at": "2026-05-30 05:40:55.983738"
  }
]
```

### Table: archived_tasks
Rows: 0

### Table: tasks
Rows: 26

```json
[
  {
    "id": 1,
    "task_id": null,
    "category": "content",
    "worker_name": "content_creator",
    "payload": "{\"campaign_id\": 1001, \"priority\": \"normal\"}",
    "status": "COMPLETED",
    "retries": 0,
    "created_at": "2026-05-29 16:08:02.066017",
    "started_at": "2026-05-29T16:08:02.347249",
    "finished_at": "2026-05-29 16:08:03.716143",
    "last_error": null,
    "assigned_to": null
  },
  {
    "id": 2,
    "task_id": null,
    "category": "content",
    "worker_name": "content_creator",
    "payload": "{\"campaign_id\": 1002, \"priority\": \"normal\"}",
    "status": "COMPLETED",
    "retries": 0,
    "created_at": "2026-05-29 16:08:04.458452",
    "started_at": "2026-05-29T16:08:04.505324",
    "finished_at": "2026-05-29 16:08:05.599406",
    "last_error": null,
    "assigned_to": null
  },
  {
    "id": 3,
    "task_id": null,
    "category": "content",
    "worker_name": "content_creator",
    "payload": "{\"campaign_id\": 1003, \"priority\": \"normal\"}",
    "status": "COMPLETED",
    "retries": 0,
    "created_at": "2026-05-29 16:08:06.775728",
    "started_at": "2026-05-29T16:08:06.806976",
    "finished_at": "2026-05-29 16:08:07.867426",
    "last_error": null,
    "assigned_to": null
  },
  {
    "id": 4,
    "task_id": null,
    "category": "content",
    "worker_name": "content_creator",
    "payload": "{\"campaign_id\": 1004, \"priority\": \"normal\"}",
    "status": "COMPLETED",
    "retries": 0,
    "created_at": "2026-05-29 16:08:09.106216",
    "started_at": "2026-05-29T16:08:09.497234",
    "finished_at": "2026-05-29 16:08:09.686581",
    "last_error": null,
    "assigned_to": null
  },
  {
    "id": 5,
    "task_id": null,
    "category": "content",
    "worker_name": "content_creator",
    "payload": "{\"campaign_id\": 1005, \"priority\": \"normal\"}",
    "status": "COMPLETED",
    "retries": 0,
    "created_at": "2026-05-29 16:08:11.433406",
    "started_at": "2026-05-29T16:08:11.683384",
    "finished_at": "2026-05-29 16:08:12.699358",
    "last_error": null,
    "assigned_to": null
  }
]
```

### Table: commissions
Rows: 0

### Table: assignments
Rows: 0

### Table: execution_logs
Rows: 62

```json
[
  {
    "id": 1,
    "task_id": 1,
    "worker_name": "content_creator",
    "log_level": "INFO",
    "message": "Result: {'status': 'error', 'summary': 'DB error: connection to server at \"localhost\" (::1), port 5432 failed: FATAL:  password authentication failed for user \"sen_user\"\\n'}",
    "timestamp": "2026-05-29 14:34:43.432418"
  },
  {
    "id": 2,
    "task_id": 1,
    "worker_name": "content_creator",
    "log_level": "INFO",
    "message": "Result: {'status': 'error', 'summary': 'DB error: connection to server at \"localhost\" (::1), port 5432 failed: FATAL:  password authentication failed for user \"sen_user\"\\n'}",
    "timestamp": "2026-05-29 14:34:43.619892"
  },
  {
    "id": 3,
    "task_id": 1,
    "worker_name": "content_creator",
    "log_level": "INFO",
    "message": "Result: {'status': 'error', 'summary': 'DB error: connection to server at \"localhost\" (::1), port 5432 failed: FATAL:  password authentication failed for user \"sen_user\"\\n'}",
    "timestamp": "2026-05-29 14:34:43.744901"
  },
  {
    "id": 4,
    "task_id": 1,
    "worker_name": "content_creator",
    "log_level": "INFO",
    "message": "Result: {'status': 'error', 'summary': 'DB error: connection to server at \"localhost\" (::1), port 5432 failed: FATAL:  password authentication failed for user \"sen_user\"\\n'}",
    "timestamp": "2026-05-29 14:34:43.869875"
  },
  {
    "id": 5,
    "task_id": 2,
    "worker_name": "content_creator",
    "log_level": "INFO",
    "message": "Result: {'status': 'error', 'summary': 'DB error: connection to server at \"localhost\" (::1), port 5432 failed: FATAL:  password authentication failed for user \"sen_user\"\\n'}",
    "timestamp": "2026-05-29 14:35:46.569461"
  }
]
```

### Table: facebook_posts
Rows: 0

### Table: sqlite_sequence
Rows: 0

## 📁 Code Files

### .js files (4007)
- `frontend\vite.config.js` (372 chars)
- `frontend\build\static\js\453.20359781.chunk.js` (4466 chars)
- `frontend\build\static\js\main.f35acb2f.js` (502009 chars)
- `frontend\dist\assets\index-DFHlmh-G.js` (203876 chars)
- `frontend\node_modules\.vite\deps\chunk-7HS6NGTM.js` (45530 chars)
- `frontend\node_modules\.vite\deps\chunk-BUSYA2B4.js` (236 chars)
- `frontend\node_modules\.vite\deps\chunk-HDXPTNVX.js` (16146 chars)
- `frontend\node_modules\.vite\deps\react-dom.js` (155 chars)
- `frontend\node_modules\.vite\deps\react-dom_client.js` (1005108 chars)
- `frontend\node_modules\.vite\deps\react.js` (117 chars)
- `frontend\node_modules\.vite\deps\react_jsx-dev-runtime.js` (12307 chars)
- `frontend\node_modules\.vite\deps\react_jsx-runtime.js` (12669 chars)
- `frontend\node_modules\.vite\deps\web-vitals.js` (8503 chars)
- `frontend\node_modules\@acemir\cssom\build\CSSOM.js` (203935 chars)
- `frontend\node_modules\@acemir\cssom\lib\clone.js` (2988 chars)
- `frontend\node_modules\@acemir\cssom\lib\CSSConditionRule.js` (868 chars)
- `frontend\node_modules\@acemir\cssom\lib\CSSContainerRule.js` (1940 chars)
- `frontend\node_modules\@acemir\cssom\lib\CSSCounterStyleRule.js` (1569 chars)
- `frontend\node_modules\@acemir\cssom\lib\CSSDocumentRule.js` (1501 chars)
- `frontend\node_modules\@acemir\cssom\lib\CSSFontFaceRule.js` (1627 chars)
- ... and 3987 more

### .json files (499)
- `config.json` (42 chars)
- `facebook_auth.json` (1050 chars)
- `facebook_cookies.json` (885 chars)
- `fb_cookies_selenium.json` (1651 chars)
- `notebooks_data.json` (700 chars)
- `package.json` (474 chars)
- `frontend\package-lock.json` (121461 chars)
- `frontend\package.json` (723 chars)
- `frontend\build\asset-manifest.json` (517 chars)
- `frontend\build\manifest.json` (492 chars)
- `frontend\dist\manifest.json` (492 chars)
- `frontend\node_modules\.package-lock.json` (96957 chars)
- `frontend\node_modules\.cache\babel-loader\00937306e55b99bdc951a4186acc16903747c9ebce4b5ec0ee0b8f126406636f.json` (1295 chars)
- `frontend\node_modules\.cache\babel-loader\01d49eb5e48b8b03aeee9512521703e04d063d287c90989ade3939774af4c242.json` (45659 chars)
- `frontend\node_modules\.cache\babel-loader\026f19f76e1e3b627611dd86c56f64a301fbfbbbe6f0c0f9af5eb95bf0c73051.json` (1784 chars)
- `frontend\node_modules\.cache\babel-loader\04bf231ce1919793c8c349eadf1ec6062e0e32dadf650bfb88d0927648b54128.json` (3725 chars)
- `frontend\node_modules\.cache\babel-loader\07c106b28fb60d094b9b927356316b799d2314c70d107ca02375ea07dc3a9248.json` (372 chars)
- `frontend\node_modules\.cache\babel-loader\0a4583f506f488b12a6dbe6830e237394b74e29d9dd09229bd4320fb8d4b58f3.json` (69782 chars)
- `frontend\node_modules\.cache\babel-loader\0e9caee439feefa59faafa29be8ce21a6ea5b6beacea265cd7442f518f94d0f0.json` (927 chars)
- `frontend\node_modules\.cache\babel-loader\1019ea01d2451a40bea37fd73d4613bf377514c07fec68332f25fa51229a9db8.json` (41805 chars)
- ... and 479 more

### .jsx files (15)
- `AdminDashboard.jsx` (1124 chars)
- `frontend\NotebookLM.jsx` (154 chars)
- `frontend\src\App.jsx` (5665 chars)
- `frontend\src\App.test.jsx` (227 chars)
- `frontend\src\index.jsx` (539 chars)
- `frontend\src\components\Header.jsx` (1074 chars)
- `frontend\src\components\Sidebar.jsx` (3786 chars)
- `frontend\src\components\TaskItem.jsx` (1740 chars)
- `frontend\src\components\TaskList.jsx` (1514 chars)
- `frontend\src_backup_20260528_175311\App.jsx` (66028 chars)
- `frontend\src_backup_20260528_175311\index.jsx` (539 chars)
- `frontend\src_backup_20260528_175311\components\Header.jsx` (1074 chars)
- `frontend\src_backup_20260528_175311\components\Sidebar.jsx` (3786 chars)
- `frontend\src_backup_20260528_175311\components\TaskItem.jsx` (1705 chars)
- `frontend\src_backup_20260528_175311\components\TaskList.jsx` (1435 chars)

### .md files (307)
- `notebooklm_source.md` (191 chars)
- `README_CONFIG.md` (1051 chars)
- `SEN_V3_NotebookLM.md` (6043 chars)
- `frontend\README.md` (3359 chars)
- `frontend\node_modules\@adobe\css-tools\README.md` (4943 chars)
- `frontend\node_modules\@adobe\css-tools\docs\API.md` (6715 chars)
- `frontend\node_modules\@adobe\css-tools\docs\AST.md` (6426 chars)
- `frontend\node_modules\@adobe\css-tools\docs\CHANGELOG.md` (5798 chars)
- `frontend\node_modules\@adobe\css-tools\docs\EXAMPLES.md` (8921 chars)
- `frontend\node_modules\@asamuzakjp\css-color\README.md` (9649 chars)
- `frontend\node_modules\@asamuzakjp\dom-selector\README.md` (10209 chars)
- `frontend\node_modules\@asamuzakjp\dom-selector\node_modules\css-tree\README.md` (8343 chars)
- `frontend\node_modules\@asamuzakjp\dom-selector\node_modules\lru-cache\LICENSE.md` (1552 chars)
- `frontend\node_modules\@asamuzakjp\dom-selector\node_modules\lru-cache\README.md` (15974 chars)
- `frontend\node_modules\@asamuzakjp\dom-selector\node_modules\mdn-data\README.md` (2247 chars)
- `frontend\node_modules\@asamuzakjp\generational-cache\README.md` (7866 chars)
- `frontend\node_modules\@asamuzakjp\nwsapi\README.md` (5440 chars)
- `frontend\node_modules\@babel\code-frame\README.md` (334 chars)
- `frontend\node_modules\@babel\compat-data\README.md` (307 chars)
- `frontend\node_modules\@babel\core\README.md` (401 chars)
- ... and 287 more

### .py files (119)
- `accesstrade_mock.py` (4092 chars)
- `blind_comparator.py` (2288 chars)
- `bootstrap.py` (7410 chars)
- `build_accesstrade.py` (7872 chars)
- `build_picker.py` (7676 chars)
- `check_db.py` (610 chars)
- `computer_use_agent.py` (5002 chars)
- `content_creation_agent.py` (6490 chars)
- `content_worker.py` (2894 chars)
- `create_nb.py` (272 chars)
- `dom_agent.py` (1722 chars)
- `facebook_complete.py` (8606 chars)
- `facebook_poster_fixed.py` (7246 chars)
- `facebook_posts.py` (0 chars)
- `facebook_stepbystep.py` (8715 chars)
- `fb_auto_click.py` (2611 chars)
- `fb_auto_undetected.py` (3989 chars)
- `fb_auto_v2.py` (5181 chars)
- `fb_post_quick.py` (2366 chars)
- `fb_scheduler.py` (702 chars)
- ... and 99 more

### .txt files (25)
- `facebook_posts.txt` (0 chars)
- `post_content.txt` (363 chars)
- `requirements.txt` (746 chars)
- `requirements_db.txt` (37 chars)
- `requirements_worker.txt` (30 chars)
- `Security_Report_20260530_134652.txt` (737 chars)
- `setup_ai_context.txt` (1128 chars)
- `worker_loop_claims_and_completes.txt` (258 chars)
- `frontend\build\robots.txt` (67 chars)
- `frontend\build\static\js\main.f35acb2f.js.LICENSE.txt` (1468 chars)
- `frontend\dist\robots.txt` (67 chars)
- `frontend\node_modules\@acemir\cssom\LICENSE.txt` (1054 chars)
- `frontend\node_modules\baseline-browser-mapping\LICENSE.txt` (11357 chars)
- `frontend\node_modules\bidi-js\LICENSE.txt` (1071 chars)
- `frontend\node_modules\css.escape\LICENSE-MIT.txt` (1077 chars)
- `frontend\node_modules\data-urls\LICENSE.txt` (1068 chars)
- `frontend\node_modules\html-encoding-sniffer\LICENSE.txt` (1068 chars)
- `frontend\node_modules\is-potential-custom-element-name\LICENSE-MIT.txt` (1077 chars)
- `frontend\node_modules\jsdom\LICENSE.txt` (1056 chars)
- `frontend\node_modules\jsesc\LICENSE-MIT.txt` (1077 chars)
- ... and 5 more

### .yaml files (1)
- `.pre-commit-config.yaml` (949 chars)

### .yml files (3)
- `docker-compose.yml` (891 chars)
- `frontend\node_modules\siginfo\.travis.yml` (1523 chars)
- `frontend\node_modules\stackback\.travis.yml` (47 chars)

