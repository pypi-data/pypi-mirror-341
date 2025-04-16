"""
HackMD MCP Server - 提供 HackMD 文章管理功能的 MCP Server
"""
import os
import json
import httpx
from typing import Sequence, Dict, Optional, List, Any, Union
import argparse
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError
from pydantic import BaseModel, Field

# API 設置
HACKMD_API_BASE = "https://api.hackmd.io/v1"
# 從環境變量獲取 API 令牌
HACKMD_API_TOKEN = os.environ.get("HACKMD_API_TOKEN", "")

# 定義模型
class Note(BaseModel):
    id: str
    title: str
    tags: Optional[List[str]] = None
    content: Optional[str] = None
    publishType: Optional[str] = None
    permalink: Optional[str] = None
    shortId: Optional[str] = None
    createdAt: Optional[Union[int, str]] = None
    publishedAt: Optional[Union[int, str]] = None
    lastChangedAt: Optional[Union[int, str]] = None
    lastChangeUser: Optional[Dict[str, Any]] = None
    userPath: Optional[str] = None
    teamPath: Optional[str] = None
    readPermission: Optional[str] = None
    writePermission: Optional[str] = None
    commentPermission: Optional[str] = None
    publishLink: Optional[str] = None

class NoteContent(BaseModel):
    content: str

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = None
    readPermission: Optional[str] = None
    writePermission: Optional[str] = None
    commentPermission: Optional[str] = None
    permalink: Optional[str] = None

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    readPermission: Optional[str] = None
    writePermission: Optional[str] = None
    commentPermission: Optional[str] = None
    permalink: Optional[str] = None

class Team(BaseModel):
    id: str
    ownerId: str
    path: str
    name: str
    logo: Optional[str] = None
    description: Optional[str] = None
    visibility: str
    createdAt: Optional[Union[int, str]] = None

class HackMDServer:
    def __init__(self):
        # 檢查 API 令牌是否設置
        if not HACKMD_API_TOKEN:
            print("警告: 未設置 HACKMD_API_TOKEN 環境變量")
            
        print("HackMD MCP 服務啟動，API 基礎網址:", HACKMD_API_BASE)
        
        # 測試 API 連線
        import subprocess
        cmd = f'curl "https://api.hackmd.io/v1/me" -H "Authorization: Bearer {HACKMD_API_TOKEN}"'
        try:
            print("正在測試 API 連線...")
            result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
            if result.returncode == 0:
                print("API 連線測試成功!")
                user_data = json.loads(result.stdout)
                print(f"已連接到 HackMD 帳號: {user_data.get('name', '未知')}")
            else:
                print(f"API 連線測試失敗: {result.stderr}")
        except Exception as e:
            print(f"測試 API 時發生錯誤: {str(e)}")

    async def get_api_client(self):
        """獲取配置好的 API 客戶端"""
        if not HACKMD_API_TOKEN:
            raise ValueError("未設置 HACKMD_API_TOKEN 環境變量")
            
        return httpx.AsyncClient(
            base_url=HACKMD_API_BASE,
            headers={
                "Authorization": f"Bearer {HACKMD_API_TOKEN}",
                "Content-Type": "application/json"
            }
        )

    async def list_notes(self) -> List[Note]:
        """列出所有可訪問的 HackMD 筆記"""
        print("正在獲取筆記列表...")
        
        async with await self.get_api_client() as client:
            response = await client.get("/notes")
            response.raise_for_status()
            notes = response.json()
        print(f"API 回傳型別: {type(notes)}, 筆數: {len(notes)}")
        if notes and isinstance(notes[0], dict):
            # 為防止後續將整數時間戳轉換為字串的驗證錯誤，使用 model_validate 方法
            notes = [Note.model_validate(n) for n in notes]
        print(f"轉換後型別: {type(notes[0]) if notes else 'empty'}，前兩筆: {notes[:2] if notes else '[]'}")
        return notes

    async def get_note(self, note_id: str) -> Note:
        """獲取指定筆記的詳細信息和內容"""
        print(f"正在獲取筆記 {note_id} 的信息...")
        
        async with await self.get_api_client() as client:
            response = await client.get(f"/notes/{note_id}")
            response.raise_for_status()
            note = response.json()
        print(f"API 回傳型別: {type(note)}，內容: {str(note)[:100]}")
        if isinstance(note, dict):
            # 使用 model_validate 替代直接構造，處理可能的整數時間戳
            note = Note.model_validate(note)
        print(f"轉換後型別: {type(note)}，title: {getattr(note, 'title', None)}")
        return note

    async def create_note(self, note: NoteCreate) -> Note:
        """創建一個新的 HackMD 筆記"""
        print(f"正在創建新筆記: {note.title}")
        
        async with await self.get_api_client() as client:
            response = await client.post(
                "/notes",
                json={
                    "title": note.title,
                    "content": note.content,
                    "readPermission": note.readPermission or "guest",
                    "writePermission": note.writePermission or "signed_in",
                    "commentPermission": note.commentPermission or "disabled",
                    "permalink": note.permalink,
                    "tags": note.tags or []
                }
            )
            response.raise_for_status()
            created_note = response.json()
        print(f"API 回傳型別: {type(created_note)}，內容: {str(created_note)[:100]}")
        if isinstance(created_note, dict):
            created_note = Note(**created_note)
        print(f"轉換後型別: {type(created_note)}，title: {getattr(created_note, 'title', None)}")
        return created_note

    async def update_note(self, note_id: str, update: NoteUpdate) -> Note:
        """更新現有 HackMD 筆記的內容或設置"""
        print(f"正在更新筆記 {note_id}")
        
        # 準備更新的數據
        update_data = {k: v for k, v in update.model_dump().items() if v is not None}
        if not update_data:
            raise ValueError("沒有提供任何更新內容")
        
        async with await self.get_api_client() as client:
            # 更新筆記內容
            if "content" in update_data:
                content = update_data.pop("content")
                print(f"更新筆記內容，筆記ID: {note_id}")
                content_update = {"content": content}
                content_response = await client.patch(
                    f"/notes/{note_id}/content",
                    json=content_update
                )
                content_response.raise_for_status()
                print(f"筆記內容更新響應狀態: {content_response.status_code}")
                
            # 更新筆記元數據
            if update_data:
                print(f"更新筆記元數據: {update_data}")
                metadata_response = await client.patch(
                    f"/notes/{note_id}",
                    json=update_data
                )
                metadata_response.raise_for_status()
                print(f"筆記元數據更新響應狀態: {metadata_response.status_code}")
                
            # 獲取更新後的筆記
            response = await client.get(f"/notes/{note_id}")
            response.raise_for_status()
            updated_note = response.json()
            
        print(f"API 回傳型別: {type(updated_note)}，內容: {str(updated_note)[:100]}")
        if isinstance(updated_note, dict):
            updated_note = Note.model_validate(updated_note)
        print(f"轉換後型別: {type(updated_note)}，title: {getattr(updated_note, 'title', None)}")
        return updated_note

    async def delete_note(self, note_id: str) -> Dict[str, str]:
        """刪除指定的 HackMD 筆記"""
        print(f"正在刪除筆記 {note_id}...")
        
        async with await self.get_api_client() as client:
            response = await client.delete(f"/notes/{note_id}")
            response.raise_for_status()
            
        print(f"成功刪除筆記 {note_id}")
        return {"status": "success", "message": f"筆記 {note_id} 已被刪除"}

    async def search_notes(self, query: str) -> List[Note]:
        """搜尋筆記"""
        print(f"正在搜尋筆記: {query}")
        
        # 獲取所有筆記然後進行本地搜尋（HackMD API 沒有搜尋端點）
        notes = await self.list_notes()
        
        # 根據標題和標籤篩選
        results = []
        for note in notes:
            if query.lower() in note.title.lower():
                results.append(note)
                continue
                
            if note.tags:
                for tag in note.tags:
                    if query.lower() in tag.lower():
                        results.append(note)
                        break
        
        print(f"搜尋結果: 找到 {len(results)} 篇匹配筆記")
        return results

    async def list_note_resources(self, note_id: str = None) -> List[Dict[str, Any]]:
        """列出筆記可訪問的資源"""
        resources = []
        
        # 如果沒有指定筆記 ID，就獲取當前用戶的所有筆記
        if not note_id:
            notes = await self.list_notes()
            resources.append({
                "uri": "hackmd://notes",
                "description": "所有筆記列表",
                "type": "list"
            })
            
            for note in notes:
                resources.append({
                    "uri": f"hackmd://notes/{note.id}",
                    "description": f"筆記: {note.title}",
                    "type": "note"
                })
                resources.append({
                    "uri": f"hackmd://notes/{note.id}/content",
                    "description": f"筆記內容: {note.title}",
                    "type": "content"
                })
        else:
            # 指定了筆記 ID，列出該筆記的相關資源
            note = await self.get_note(note_id)
            resources.append({
                "uri": f"hackmd://notes/{note.id}",
                "description": f"筆記: {note.title}",
                "type": "note"
            })
            resources.append({
                "uri": f"hackmd://notes/{note.id}/content",
                "description": f"筆記內容: {note.title}",
                "type": "content"
            })
            
        return resources

    # 添加團隊相關功能
    async def list_teams(self) -> List[Team]:
        """列出所有可訪問的團隊"""
        print("正在獲取團隊列表...")
        
        async with await self.get_api_client() as client:
            response = await client.get("/teams")
            response.raise_for_status()
            teams = response.json()
        print(f"API 回傳型別: {type(teams)}, 筆數: {len(teams)}")
        if teams and isinstance(teams[0], dict):
            # 使用 model_validate 方法處理可能的整數時間戳
            teams = [Team.model_validate(t) for t in teams]
        print(f"轉換後型別: {type(teams[0]) if teams else 'empty'}，前兩筆: {teams[:2] if teams else '[]'}")
        return teams
    
    async def get_team_notes(self, team_path: str) -> List[Note]:
        """獲取團隊工作區中的筆記列表"""
        print(f"正在獲取團隊 {team_path} 的筆記列表...")
        
        async with await self.get_api_client() as client:
            response = await client.get(f"/teams/{team_path}/notes")
            response.raise_for_status()
            notes = response.json()
        print(f"API 回傳型別: {type(notes)}, 筆數: {len(notes)}")
        if notes and isinstance(notes[0], dict):
            notes = [Note(**n) for n in notes]
        print(f"轉換後型別: {type(notes[0]) if notes else 'empty'}，前兩筆: {notes[:2] if notes else '[]'}")
        return notes
    
    async def create_team_note(self, team_path: str, note: NoteCreate) -> Note:
        """在團隊工作區中創建筆記"""
        print(f"正在團隊 {team_path} 中創建新筆記: {note.title}")
        
        async with await self.get_api_client() as client:
            response = await client.post(
                f"/teams/{team_path}/notes",
                json={
                    "title": note.title,
                    "content": note.content,
                    "readPermission": note.readPermission or "guest",
                    "writePermission": note.writePermission or "signed_in",
                    "commentPermission": note.commentPermission or "disabled",
                    "permalink": note.permalink,
                    "tags": note.tags or []
                }
            )
            response.raise_for_status()
            created_note = response.json()
            
        print(f"成功在團隊中創建筆記，ID: {created_note['id']}")
        return created_note

async def serve() -> None:
    server = Server("hackmd-mcp")
    # 初始化 HackMD 服務
    hackmd_server = HackMDServer()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """列出可用的工具。"""
        return [
            Tool(
                name="list_notes",
                description="列出所有可訪問的 HackMD 筆記",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            
            Tool(
                name="get_note",
                description="獲取指定筆記的詳細信息和內容",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "note_id": {
                            "type": "string",
                            "description": "筆記的 ID",
                        }
                    },
                    "required": ["note_id"]
                },
            ),
            
            Tool(
                name="create_note",
                description="創建一個新的 HackMD 筆記",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "筆記標題",
                        },
                        "content": {
                            "type": "string",
                            "description": "筆記內容（Markdown 格式）",
                        },
                        "tags": {
                            "type": "array",
                            "description": "標籤列表",
                            "items": {"type": "string"}
                        },
                        "readPermission": {
                            "type": "string",
                            "description": "讀取權限（guest, signed_in, owner）",
                            "default": "guest"
                        },
                        "writePermission": {
                            "type": "string",
                            "description": "寫入權限（guest, signed_in, owner）",
                            "default": "signed_in"
                        },
                        "commentPermission": {
                            "type": "string",
                            "description": "評論權限（disabled, forbidden, guest, signed_in, owner）",
                            "default": "disabled"
                        },
                        "permalink": {
                            "type": "string",
                            "description": "自定義永久鏈接",
                        }
                    },
                    "required": ["title", "content"]
                },
            ),
            
            Tool(
                name="update_note",
                description="更新現有 HackMD 筆記的內容或設置",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "note_id": {
                            "type": "string",
                            "description": "筆記的 ID",
                        },
                        "title": {
                            "type": "string",
                            "description": "更新的標題",
                        },
                        "content": {
                            "type": "string",
                            "description": "更新的內容（Markdown 格式）",
                        },
                        "tags": {
                            "type": "array",
                            "description": "更新的標籤列表",
                            "items": {"type": "string"}
                        },
                        "readPermission": {
                            "type": "string",
                            "description": "更新的讀取權限（guest, signed_in, owner）",
                        },
                        "writePermission": {
                            "type": "string",
                            "description": "更新的寫入權限（guest, signed_in, owner）",
                        },
                        "commentPermission": {
                            "type": "string",
                            "description": "更新的評論權限（disabled, forbidden, guest, signed_in, owner）",
                        },
                        "permalink": {
                            "type": "string",
                            "description": "更新的自定義永久鏈接",
                        }
                    },
                    "required": ["note_id"]
                },
            ),
            
            Tool(
                name="delete_note",
                description="刪除指定的 HackMD 筆記",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "note_id": {
                            "type": "string",
                            "description": "筆記的 ID",
                        }
                    },
                    "required": ["note_id"]
                },
            ),
            
            Tool(
                name="search_notes",
                description="搜尋筆記（根據標題和標籤）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜尋關鍵詞",
                        }
                    },
                    "required": ["query"]
                },
            ),
            
            # 添加團隊相關工具
            Tool(
                name="list_teams",
                description="列出所有可訪問的團隊",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            
            Tool(
                name="get_team_notes",
                description="獲取團隊工作區中的筆記列表",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "team_path": {
                            "type": "string",
                            "description": "團隊路徑",
                        }
                    },
                    "required": ["team_path"]
                },
            ),
            
            Tool(
                name="create_team_note",
                description="在團隊工作區中創建筆記",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "team_path": {
                            "type": "string",
                            "description": "團隊路徑",
                        },
                        "title": {
                            "type": "string",
                            "description": "筆記標題",
                        },
                        "content": {
                            "type": "string",
                            "description": "筆記內容（Markdown 格式）",
                        },
                        "tags": {
                            "type": "array",
                            "description": "標籤列表",
                            "items": {"type": "string"}
                        },
                        "readPermission": {
                            "type": "string",
                            "description": "讀取權限（guest, signed_in, owner）",
                            "default": "guest"
                        },
                        "writePermission": {
                            "type": "string",
                            "description": "寫入權限（guest, signed_in, owner）",
                            "default": "signed_in"
                        },
                        "commentPermission": {
                            "type": "string",
                            "description": "評論權限（disabled, forbidden, guest, signed_in, owner）",
                            "default": "disabled"
                        },
                        "permalink": {
                            "type": "string",
                            "description": "自定義永久鏈接",
                        }
                    },
                    "required": ["team_path", "title", "content"]
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """處理工具調用。"""
        try:
            if name == "list_notes":
                notes = await hackmd_server.list_notes()
                return [
                    TextContent(type="text", text=json.dumps([note.model_dump() for note in notes], indent=2, ensure_ascii=False))
                ]
                
            elif name == "get_note":
                note_id = arguments.get("note_id")
                
                if not note_id:
                    raise ValueError("缺少必要參數: note_id")
                
                note = await hackmd_server.get_note(note_id)
                return [
                    TextContent(type="text", text=json.dumps(note.model_dump(), indent=2, ensure_ascii=False))
                ]
                
            elif name == "create_note":
                title = arguments.get("title")
                content = arguments.get("content")
                tags = arguments.get("tags", [])
                read_permission = arguments.get("readPermission", "guest")
                write_permission = arguments.get("writePermission", "signed_in")
                comment_permission = arguments.get("commentPermission", "disabled")
                permalink = arguments.get("permalink")
                
                if not title or not content:
                    raise ValueError("缺少必要參數: title 和 content")
                
                note = NoteCreate(
                    title=title,
                    content=content,
                    tags=tags,
                    readPermission=read_permission,
                    writePermission=write_permission,
                    commentPermission=comment_permission,
                    permalink=permalink
                )
                
                created_note = await hackmd_server.create_note(note)
                return [
                    TextContent(type="text", text=json.dumps(created_note.model_dump(), indent=2, ensure_ascii=False))
                ]
                
            elif name == "update_note":
                note_id = arguments.get("note_id")
                
                if not note_id:
                    raise ValueError("缺少必要參數: note_id")
                
                # 檢查是否有其他參數需要更新
                update_data = {}
                for field in ["title", "content", "tags", "readPermission", "writePermission", "commentPermission", "permalink"]:
                    if field in arguments:
                        update_data[field] = arguments[field]
                
                if not update_data:
                    raise ValueError("沒有提供任何更新內容")
                
                note_update = NoteUpdate(**update_data)
                updated_note = await hackmd_server.update_note(note_id, note_update)
                
                return [
                    TextContent(type="text", text=json.dumps(updated_note.model_dump(), indent=2, ensure_ascii=False))
                ]
                
            elif name == "delete_note":
                note_id = arguments.get("note_id")
                
                if not note_id:
                    raise ValueError("缺少必要參數: note_id")
                
                result = await hackmd_server.delete_note(note_id)
                return [
                    TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))
                ]
                
            elif name == "search_notes":
                query = arguments.get("query")
                
                if not query:
                    raise ValueError("缺少必要參數: query")
                
                notes = await hackmd_server.search_notes(query)
                return [
                    TextContent(type="text", text=json.dumps([note.model_dump() for note in notes], indent=2, ensure_ascii=False))
                ]
                
            # 處理團隊相關工具
            elif name == "list_teams":
                teams = await hackmd_server.list_teams()
                return [
                    TextContent(type="text", text=json.dumps([team.model_dump() for team in teams], indent=2, ensure_ascii=False))
                ]
                
            elif name == "get_team_notes":
                team_path = arguments.get("team_path")
                
                if not team_path:
                    raise ValueError("缺少必要參數: team_path")
                
                notes = await hackmd_server.get_team_notes(team_path)
                return [
                    TextContent(type="text", text=json.dumps([note.model_dump() for note in notes], indent=2, ensure_ascii=False))
                ]
                
            elif name == "create_team_note":
                team_path = arguments.get("team_path")
                title = arguments.get("title")
                content = arguments.get("content")
                tags = arguments.get("tags", [])
                read_permission = arguments.get("readPermission", "guest")
                write_permission = arguments.get("writePermission", "signed_in")
                comment_permission = arguments.get("commentPermission", "disabled")
                permalink = arguments.get("permalink")
                
                if not team_path or not title or not content:
                    raise ValueError("缺少必要參數: team_path, title 和 content")
                
                note = NoteCreate(
                    title=title,
                    content=content,
                    tags=tags,
                    readPermission=read_permission,
                    writePermission=write_permission,
                    commentPermission=comment_permission,
                    permalink=permalink
                )
                
                created_note = await hackmd_server.create_team_note(team_path, note)
                return [
                    TextContent(type="text", text=json.dumps(created_note.model_dump(), indent=2, ensure_ascii=False))
                ]
            
            else:
                raise ValueError(f"未知工具: {name}")
        except Exception as e:
            raise ValueError(f"處理請求時出錯: {str(e)}")

    # 修正資源相關功能 - 修正裝飾器使用方式
    @server.list_resources()
    async def list_resources() -> List[Dict[str, str]]:
        """列出可用的資源"""
        try:
            # 返回固定的資源列表格式
            notes = await hackmd_server.list_notes()
            # 獲取團隊列表
            teams = await hackmd_server.list_teams()
            
            resources = [
                {"uri": "hackmd://notes", "description": "所有個人筆記列表"},
                {"uri": "hackmd://teams", "description": "所有團隊列表"}
            ]
            
            # 添加每個個人筆記作為資源
            for note in notes:
                if not note.teamPath: # 確保是個人筆記
                    resources.append({
                        "uri": f"hackmd://notes/{note.id}", 
                        "description": f"個人筆記: {note.title}"
                    })
                    resources.append({
                        "uri": f"hackmd://notes/{note.id}/content",
                        "description": f"個人筆記內容: {note.title}"
                    })

            # 添加每個團隊及其筆記作為資源
            for team in teams:
                 resources.append({
                    "uri": f"hackmd://teams/{team.path}/notes",
                    "description": f"團隊筆記列表: {team.name}"
                 })
                 # 獲取團隊筆記並添加
                 team_notes = await hackmd_server.get_team_notes(team.path)
                 for note in team_notes:
                     resources.append({
                         "uri": f"hackmd://notes/{note.id}", # 團隊筆記也使用 /notes/{id} 訪問
                         "description": f"團隊筆記 ({team.name}): {note.title}"
                     })
                     resources.append({
                         "uri": f"hackmd://notes/{note.id}/content",
                         "description": f"團隊筆記內容 ({team.name}): {note.title}"
                     })

            return resources
        except Exception as e:
            print(f"獲取資源列表時發生錯誤: {e}")
            return []

    @server.read_resource() # 移除 URI 字串參數
    async def read_resource_notes() -> Dict[str, Any]:
        """獲取所有筆記列表資源 (對應 hackmd://notes)"""
        try:
            notes = await hackmd_server.list_notes()
            # 過濾掉團隊筆記，只返回個人筆記
            personal_notes = [note for note in notes if not note.teamPath]
            return {"notes": [note.model_dump() for note in personal_notes]}
        except Exception as e:
            print(f"獲取個人筆記列表資源時發生錯誤: {e}")
            raise ValueError(f"獲取個人筆記列表資源時發生錯誤: {str(e)}")

    @server.read_resource() # 移除 URI 字串參數
    async def read_resource_teams() -> Dict[str, Any]:
        """獲取所有團隊列表資源 (對應 hackmd://teams)"""
        try:
            teams = await hackmd_server.list_teams()
            return {"teams": [team.model_dump() for team in teams]}
        except Exception as e:
            print(f"獲取團隊列表資源時發生錯誤: {e}")
            raise ValueError(f"獲取團隊列表資源時發生錯誤: {str(e)}")

    @server.read_resource() # 移除 URI 字串參數
    async def read_resource_team_notes(team_path: str) -> Dict[str, Any]:
        """獲取特定團隊的筆記列表資源 (對應 hackmd://teams/{team_path}/notes)"""
        try:
            notes = await hackmd_server.get_team_notes(team_path)
            return {"notes": [note.model_dump() for note in notes]}
        except Exception as e:
            print(f"獲取團隊 {team_path} 筆記列表資源時發生錯誤: {e}")
            raise ValueError(f"獲取團隊 {team_path} 筆記列表資源時發生錯誤: {str(e)}")


    @server.read_resource()  # 移除 URI 字串參數
    async def read_resource_note(note_id: str) -> Dict[str, Any]:
        """獲取特定筆記資源 (對應 hackmd://notes/{note_id})"""
        try:
            note = await hackmd_server.get_note(note_id)
            return note.model_dump()
        except Exception as e:
            print(f"獲取筆記資源 {note_id} 時發生錯誤: {e}")
            raise ValueError(f"獲取筆記資源 {note_id} 時發生錯誤: {str(e)}")

    @server.read_resource()  # 移除 URI 字串參數
    async def read_resource_note_content(note_id: str) -> Dict[str, Any]:
        """獲取特定筆記內容資源 (對應 hackmd://notes/{note_id}/content)"""
        try:
            # 使用 get_note 而不是 get_note_content
            note = await hackmd_server.get_note(note_id)
            return {"content": note.content} if note.content else {"content": ""}
        except Exception as e:
            print(f"獲取筆記內容資源 {note_id} 時發生錯誤: {e}")
            raise ValueError(f"獲取筆記內容資源 {note_id} 時發生錯誤: {str(e)}")
    
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)

def main():
    import asyncio
    
    # 解析命令行參數
    parser = argparse.ArgumentParser(description="HackMD MCP Server")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 啟動伺服器的子命令
    server_parser = subparsers.add_parser('server', help='啟動 HackMD MCP 伺服器')
    
    # 列出筆記的子命令
    list_parser = subparsers.add_parser('list', help='列出所有筆記')
    
    # 獲取筆記的子命令
    get_parser = subparsers.add_parser('get', help='獲取筆記')
    get_parser.add_argument('note_id', help='筆記 ID')
    
    # 創建筆記的子命令
    create_parser = subparsers.add_parser('create', help='創建新筆記')
    create_parser.add_argument('--title', required=True, help='筆記標題')
    create_parser.add_argument('--content', required=True, help='筆記內容')
    create_parser.add_argument('--tag', action='append', dest='tags', help='添加標籤 (可多次使用)')
    create_parser.add_argument('--read', choices=['guest', 'signed_in', 'owner'], default='guest', help='讀取權限')
    create_parser.add_argument('--write', choices=['guest', 'signed_in', 'owner'], default='signed_in', help='寫入權限')
    create_parser.add_argument('--comment', choices=['disabled', 'forbidden', 'guest', 'signed_in', 'owner'], default='disabled', help='評論權限')
    
    # 更新筆記的子命令
    update_parser = subparsers.add_parser('update', help='更新筆記')
    update_parser.add_argument('note_id', help='筆記 ID')
    update_parser.add_argument('--title', help='更新標題')
    update_parser.add_argument('--content', help='更新內容')
    update_parser.add_argument('--tag', action='append', dest='tags', help='更新標籤 (可多次使用)')
    update_parser.add_argument('--read', choices=['guest', 'signed_in', 'owner'], help='更新讀取權限')
    update_parser.add_argument('--write', choices=['guest', 'signed_in', 'owner'], help='更新寫入權限')
    update_parser.add_argument('--comment', choices=['disabled', 'forbidden', 'guest', 'signed_in', 'owner'], help='更新評論權限')
    
    # 刪除筆記的子命令
    delete_parser = subparsers.add_parser('delete', help='刪除筆記')
    delete_parser.add_argument('note_id', help='筆記 ID')
    
    # 搜尋筆記的子命令
    search_parser = subparsers.add_parser('search', help='搜尋筆記')
    search_parser.add_argument('query', help='搜尋關鍵詞')
    
    args = parser.parse_args()
    
    # 檢查是否設置了 HACKMD_API_TOKEN 環境變數
    if not os.environ.get("HACKMD_API_TOKEN"):
        print("錯誤: 請設置 HACKMD_API_TOKEN 環境變數")
        print("您可以使用以下命令設置：")
        print("export HACKMD_API_TOKEN=您的API令牌")
        sys.exit(1)
    
    if args.command == 'server' or args.command is None:
        print("啟動 HackMD MCP 伺服器...")
        asyncio.run(serve())
    else:
        # 創建一個臨時的 HackMD 伺服器實例
        hackmd_server = HackMDServer()
        
        async def process_command():
            try:
                if args.command == 'list':
                    notes = await hackmd_server.list_notes()
                    print(f"找到 {len(notes)} 篇筆記:")
                    for note in notes:
                        published = " (已發布)" if note.publishType else ""
                        print(f"ID: {note.id} - {note.title}{published}")
                    
                elif args.command == 'get':
                    note = await hackmd_server.get_note(args.note_id)
                    print(f"筆記標題: {note.title}")
                    print(f"筆記內容:\n{note.content}")
                    print(f"筆記標籤: {', '.join(note.tags) if note.tags else '無'}")
                    
                elif args.command == 'create':
                    note_data = NoteCreate(
                        title=args.title,
                        content=args.content,
                        tags=args.tags or [],
                        readPermission=args.read,
                        writePermission=args.write,
                        commentPermission=args.comment
                    )
                    created_note = await hackmd_server.create_note(note_data)
                    print(f"筆記已創建: {created_note.title}")
                    print(f"筆記 ID: {created_note.id}")
                    
                elif args.command == 'update':
                    update_data = {}
                    if args.title:
                        update_data['title'] = args.title
                    if args.content:
                        update_data['content'] = args.content
                    if args.tags:
                        update_data['tags'] = args.tags
                    if args.read:
                        update_data['readPermission'] = args.read
                    if args.write:
                        update_data['writePermission'] = args.write
                    if args.comment:
                        update_data['commentPermission'] = args.comment
                        
                    if not update_data:
                        print("錯誤: 請提供至少一個更新參數")
                        return
                        
                    note_update = NoteUpdate(**update_data)
                    updated_note = await hackmd_server.update_note(args.note_id, note_update)
                    print(f"筆記已更新: {updated_note.title}")
                    print(f"筆記 ID: {updated_note.id}")
                    
                elif args.command == 'delete':
                    result = await hackmd_server.delete_note(args.note_id)
                    print(f"筆記已刪除: {result['message']}")
                    
                elif args.command == 'search':
                    notes = await hackmd_server.search_notes(args.query)
                    print(f"找到 {len(notes)} 篇匹配筆記:")
                    for note in notes:
                        print(f"ID: {note.id} - {note.title}")
            
            except Exception as e:
                print(f"錯誤: {str(e)}")
                sys.exit(1)
        
        # 執行命令
        asyncio.run(process_command())

if __name__ == "__main__":
    main()