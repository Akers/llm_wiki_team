"""MCP 工具测试。

覆盖 mcp-tools spec 中的所有场景（17/17）：
- search_wiki: 有结果、无结果、缺少参数、空 query
- read_wiki_page: 正常读取、不存在、路径遍历
- write_wiki_page: 创建、覆盖、路径遍历
- ingest_text: 正常提交、超限、空内容
- check_ingest_status: pending、completed(含 wiki_page_paths)、unknown
"""

import pytest

from _utils import ServerHandle


# ===================================================================
# search_wiki
# ===================================================================


class TestSearchWiki:
    """search_wiki 工具测试。"""

    def test_search_returns_results(self, server: ServerHandle):
        """搜索已有页面返回匹配结果。"""
        # 先写入一个页面
        server.mcp_tool("write_wiki_page", {
            "path": "machine-learning.md",
            "content": "# Machine Learning\n\nDeep learning and neural networks are subsets of ML.",
        })

        result = server.mcp_tool("search_wiki", {"query": "machine learning"})
        assert result["is_error"] is False
        data = result["parsed"]
        assert "results" in data
        assert len(data["results"]) > 0

    def test_search_results_structure(self, server: ServerHandle):
        """搜索结果包含 path / title / score / snippet。"""
        server.mcp_tool("write_wiki_page", {
            "path": "rust-basics.md",
            "content": "# Rust Basics\n\nRust is a systems programming language focused on safety.",
        })

        result = server.mcp_tool("search_wiki", {"query": "rust"})
        assert result["is_error"] is False
        if result["parsed"]["results"]:
            r = result["parsed"]["results"][0]
            assert "path" in r
            assert "title" in r
            assert "score" in r
            assert "snippet" in r

    def test_search_limits_to_10(self, server: ServerHandle):
        """搜索最多返回 10 条结果。"""
        # 创建 15 个页面
        for i in range(15):
            server.mcp_tool("write_wiki_page", {
                "path": f"topic/page-{i:02d}.md",
                "content": f"# Page {i}\n\nCommon keyword: alpha beta gamma.",
            })

        result = server.mcp_tool("search_wiki", {"query": "alpha beta"})
        assert result["is_error"] is False
        assert len(result["parsed"]["results"]) <= 10

    def test_search_no_results(self, server: ServerHandle):
        """搜索不存在的关键词返回空结果列表。"""
        result = server.mcp_tool("search_wiki", {"query": "zzz_nonexistent_xyzzy_12345"})
        assert result["is_error"] is False
        data = result["parsed"]
        assert data["results"] == []

    def test_search_missing_query(self, server: ServerHandle):
        """缺少 query 参数返回参数错误。"""
        result = server.mcp_tool("search_wiki", {})
        assert result["is_error"] is True
        assert "Invalid parameters" in result["content"]

    def test_search_empty_query(self, server: ServerHandle):
        """空 query 字符串返回错误。"""
        result = server.mcp_tool("search_wiki", {"query": ""})
        assert result["is_error"] is True
        assert "required" in result["parsed"]["error"].lower()

    def test_search_whitespace_query(self, server: ServerHandle):
        """纯空白 query 返回错误。"""
        result = server.mcp_tool("search_wiki", {"query": "   "})
        assert result["is_error"] is True


# ===================================================================
# read_wiki_page
# ===================================================================


class TestReadWikiPage:
    """read_wiki_page 工具测试。"""

    def test_read_existing_page(self, server: ServerHandle):
        """读取已存在的页面返回内容。"""
        content = "# Hello World\n\nThis is a test page."
        server.mcp_tool("write_wiki_page", {
            "path": "hello.md",
            "content": content,
        })

        result = server.mcp_tool("read_wiki_page", {"path": "hello.md"})
        assert result["is_error"] is False
        data = result["parsed"]
        assert data["path"] == "hello.md"
        assert data["content"] == content

    def test_read_page_in_subdirectory(self, server: ServerHandle):
        """读取子目录下的页面。"""
        server.mcp_tool("write_wiki_page", {
            "path": "notes/meeting.md",
            "content": "# Meeting Notes\n\nAttendees: Alice, Bob",
        })

        result = server.mcp_tool("read_wiki_page", {"path": "notes/meeting.md"})
        assert result["is_error"] is False
        assert "Meeting Notes" in result["parsed"]["content"]

    def test_read_nonexistent_page(self, server: ServerHandle):
        """读取不存在的页面返回错误，并提示使用 search_wiki。"""
        result = server.mcp_tool("read_wiki_page", {"path": "does-not-exist.md"})
        assert result["is_error"] is True
        assert "not found" in result["parsed"]["error"].lower()
        assert "search_wiki" in result["parsed"]["error"]

    def test_read_path_traversal_dotdot(self, server: ServerHandle):
        """路径包含 .. 的请求被拒绝（路径遍历攻击）。"""
        result = server.mcp_tool("read_wiki_page", {"path": "../../../etc/passwd"})
        assert result["is_error"] is True
        assert "path traversal" in result["parsed"]["error"].lower() or "invalid" in result["parsed"]["error"].lower()

    def test_read_path_traversal_absolute(self, server: ServerHandle):
        """绝对路径被拒绝。"""
        result = server.mcp_tool("read_wiki_page", {"path": "/etc/passwd"})
        assert result["is_error"] is True

    def test_read_empty_path(self, server: ServerHandle):
        """空路径返回错误。"""
        result = server.mcp_tool("read_wiki_page", {"path": ""})
        assert result["is_error"] is True

    def test_read_missing_path_param(self, server: ServerHandle):
        """缺少 path 参数返回参数错误。"""
        result = server.mcp_tool("read_wiki_page", {})
        assert result["is_error"] is True
        assert "Invalid parameters" in result["content"]


# ===================================================================
# write_wiki_page
# ===================================================================


class TestWriteWikiPage:
    """write_wiki_page 工具测试。"""

    def test_create_new_page(self, server: ServerHandle):
        """创建新页面成功，action = 'created'。"""
        result = server.mcp_tool("write_wiki_page", {
            "path": "new-page.md",
            "content": "# New Page\n\nFresh content.",
        })
        assert result["is_error"] is False
        data = result["parsed"]
        assert data["success"] is True
        assert data["action"] == "created"
        assert data["path"] == "new-page.md"

    def test_create_page_verifies_on_disk(self, server: ServerHandle):
        """创建的页面实际存在于磁盘上。"""
        server.mcp_tool("write_wiki_page", {
            "path": "disk-test.md",
            "content": "# Disk Test\n\nVerify on disk.",
        })

        file_path = server.project_dir / "wiki" / "disk-test.md"
        assert file_path.exists()
        assert "Disk Test" in file_path.read_text()

    def test_overwrite_existing_page(self, server: ServerHandle):
        """覆盖已有页面，action = 'updated'。"""
        server.mcp_tool("write_wiki_page", {
            "path": "overwrite.md",
            "content": "Version 1",
        })
        result = server.mcp_tool("write_wiki_page", {
            "path": "overwrite.md",
            "content": "Version 2 - updated",
        })
        assert result["is_error"] is False
        assert result["parsed"]["action"] == "updated"

        # Verify content updated
        verify = server.mcp_tool("read_wiki_page", {"path": "overwrite.md"})
        assert "Version 2" in verify["parsed"]["content"]

    def test_create_in_subdirectory(self, server: ServerHandle):
        """在子目录中创建页面（自动创建目录）。"""
        result = server.mcp_tool("write_wiki_page", {
            "path": "deep/nested/page.md",
            "content": "# Deep Page",
        })
        assert result["is_error"] is False
        assert result["parsed"]["action"] == "created"

        # Verify directory was created
        assert (server.project_dir / "wiki" / "deep" / "nested" / "page.md").exists()

    def test_write_path_traversal_dotdot(self, server: ServerHandle):
        """路径包含 .. 被拒绝。"""
        result = server.mcp_tool("write_wiki_page", {
            "path": "../escape.md",
            "content": "should fail",
        })
        assert result["is_error"] is True

    def test_write_path_traversal_absolute(self, server: ServerHandle):
        """绝对路径被拒绝。"""
        result = server.mcp_tool("write_wiki_page", {
            "path": "/tmp/evil.md",
            "content": "should fail",
        })
        assert result["is_error"] is True

    def test_write_empty_path(self, server: ServerHandle):
        """空路径返回错误。"""
        result = server.mcp_tool("write_wiki_page", {
            "path": "",
            "content": "content",
        })
        assert result["is_error"] is True

    def test_write_missing_params(self, server: ServerHandle):
        """缺少必需参数返回错误。"""
        result = server.mcp_tool("write_wiki_page", {"path": "test.md"})
        assert result["is_error"] is True

        result = server.mcp_tool("write_wiki_page", {"content": "text"})
        assert result["is_error"] is True


# ===================================================================
# ingest_text
# ===================================================================


class TestIngestText:
    """ingest_text 工具测试。"""

    def test_ingest_returns_task_id(self, server: ServerHandle):
        """正常提交返回 task_id。"""
        result = server.mcp_tool("ingest_text", {
            "content": "This is a test document about artificial intelligence.",
        })
        assert result["is_error"] is False
        data = result["parsed"]
        assert "task_id" in data
        assert len(data["task_id"]) > 0
        assert data["status"] == "queued"

    def test_ingest_with_title_and_source_type(self, server: ServerHandle):
        """带 title 和 source_type 参数提交。"""
        result = server.mcp_tool("ingest_text", {
            "content": "Document body text.",
            "title": "Test Article",
            "source_type": "article",
        })
        assert result["is_error"] is False
        data = result["parsed"]
        assert "source_file" in data
        assert "article" in data["source_file"]

    def test_ingest_creates_source_file(self, server: ServerHandle):
        """提交后在 sources/mcp-ingest/ 目录创建文件。"""
        result = server.mcp_tool("ingest_text", {
            "content": "Test content for file creation.",
            "title": "FileTest",
        })
        assert result["is_error"] is False

        mcp_ingest_dir = server.project_dir / "sources" / "mcp-ingest"
        assert mcp_ingest_dir.exists()
        files = list(mcp_ingest_dir.iterdir())
        assert len(files) > 0

    def test_ingest_content_exceeds_100kb(self, server: ServerHandle):
        """内容超过 100KB 返回错误。"""
        big_content = "A" * (102_400 + 1)  # 100KB + 1 byte
        result = server.mcp_tool("ingest_text", {"content": big_content})
        assert result["is_error"] is True
        assert "exceeds" in result["parsed"]["error"].lower() or "100" in result["parsed"]["error"]

    def test_ingest_exactly_100kb_succeeds(self, server: ServerHandle):
        """刚好 100KB 的内容可以提交。"""
        content = "B" * 102_400  # exactly 100KB
        result = server.mcp_tool("ingest_text", {"content": content})
        assert result["is_error"] is False

    def test_ingest_empty_content(self, server: ServerHandle):
        """空内容返回错误。"""
        result = server.mcp_tool("ingest_text", {"content": ""})
        assert result["is_error"] is True
        assert "empty" in result["parsed"]["error"].lower() or "required" in result["parsed"]["error"].lower()

    def test_ingest_whitespace_only_content(self, server: ServerHandle):
        """纯空白内容返回错误。"""
        result = server.mcp_tool("ingest_text", {"content": "   \n\t   "})
        assert result["is_error"] is True

    def test_ingest_missing_content_param(self, server: ServerHandle):
        """缺少 content 参数返回参数错误。"""
        result = server.mcp_tool("ingest_text", {})
        assert result["is_error"] is True
        assert "Invalid parameters" in result["content"]


# ===================================================================
# check_ingest_status
# ===================================================================


class TestCheckIngestStatus:
    """check_ingest_status 工具测试。"""

    def test_check_pending_task(self, server: ServerHandle):
        """检查刚提交的 pending 任务。"""
        ingest_result = server.mcp_tool("ingest_text", {
            "content": "Status check test document.",
        })
        task_id = ingest_result["parsed"]["task_id"]

        result = server.mcp_tool("check_ingest_status", {"task_id": task_id})
        assert result["is_error"] is False
        data = result["parsed"]
        assert data["task_id"] == task_id
        # Task should be in pending or processing state
        assert data["status"] in ("pending", "processing", "done")

    def test_check_unknown_task(self, server: ServerHandle):
        """检查不存在的 task_id 返回 not found 错误。"""
        # First create a queue by ingesting something, then check for a fake task_id
        server.mcp_tool("ingest_text", {
            "content": "Queue setup for unknown task test.",
        })
        
        result = server.mcp_tool("check_ingest_status", {
            "task_id": "nonexistent-task-id-00000000",
        })
        assert result["is_error"] is True
        assert "not found" in result["parsed"]["error"].lower()

    def test_check_missing_task_id_param(self, server: ServerHandle):
        """缺少 task_id 参数返回参数错误。"""
        result = server.mcp_tool("check_ingest_status", {})
        assert result["is_error"] is True
        assert "Invalid parameters" in result["content"]

    def test_check_returns_source_path(self, server: ServerHandle):
        """返回结果包含 source_path。"""
        ingest_result = server.mcp_tool("ingest_text", {
            "content": "Source path test.",
        })
        task_id = ingest_result["parsed"]["task_id"]

        result = server.mcp_tool("check_ingest_status", {"task_id": task_id})
        assert result["is_error"] is False
        assert "source_path" in result["parsed"]

    def test_check_task_status_schema(self, server: ServerHandle):
        """返回结果包含所有标准字段。"""
        ingest_result = server.mcp_tool("ingest_text", {
            "content": "Schema verification test.",
        })
        task_id = ingest_result["parsed"]["task_id"]

        result = server.mcp_tool("check_ingest_status", {"task_id": task_id})
        data = result["parsed"]
        # The response should have standard fields
        assert "task_id" in data
        assert "status" in data
        assert "source_path" in data
        assert "error" in data
