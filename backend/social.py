"""社交模块 — 用户认证、动态、评论、点赞、好友
使用 SQLite 数据库，零外部依赖
"""
import sqlite3
import hashlib
import secrets
import json
import os
from datetime import datetime, timezone
from contextlib import contextmanager

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "data", "social.db"))


def ensure_db_dir():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


@contextmanager
def get_db():
    """获取数据库连接，自动提交/关闭"""
    ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    # 确保表存在
    conn.execute("CREATE TABLE IF NOT EXISTS _init_check (k TEXT PRIMARY KEY)")
    if conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'").fetchone() is None:
        _init_tables(conn)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _init_tables(conn):
    """在给定连接上创建所有表"""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                name TEXT NOT NULL DEFAULT '',
                avatar TEXT NOT NULL DEFAULT '',
                school TEXT NOT NULL DEFAULT '',
                bio TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS tokens (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                user_name TEXT NOT NULL,
                user_avatar TEXT NOT NULL DEFAULT '',
                text TEXT NOT NULL,
                images TEXT NOT NULL DEFAULT '[]',
                topic TEXT NOT NULL DEFAULT '',
                likes_count INTEGER NOT NULL DEFAULT 0,
                comments_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS comments (
                id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                user_name TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS likes (
                id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(post_id, user_id)
            );

            CREATE TABLE IF NOT EXISTS friends (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                friend_id TEXT NOT NULL,
                friend_name TEXT NOT NULL DEFAULT '',
                friend_avatar TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (friend_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, friend_id)
            );

            CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post_id);
            CREATE INDEX IF NOT EXISTS idx_likes_post ON likes(post_id);
            CREATE INDEX IF NOT EXISTS idx_friends_user ON friends(user_id);
        """)


# ── 密码工具 ──────────────────────────────────────────

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """返回 (hash, salt)"""
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return h, salt


# ── Token 工具 ─────────────────────────────────────────

def generate_token() -> str:
    return secrets.token_hex(32)


def get_user_by_token(token: str) -> dict | None:
    """通过 token 获取用户，失败返回 None"""
    with get_db() as db:
        row = db.execute("""
            SELECT u.* FROM users u
            JOIN tokens t ON u.id = t.user_id
            WHERE t.token = ?
        """, (token,)).fetchone()
        return dict(row) if row else None


def require_user(token: str) -> dict:
    """通过 token 获取用户，未登录抛异常"""
    user = get_user_by_token(token)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="请先登录")
    return user


# ── 用户认证 ──────────────────────────────────────────

def register_user(email: str, password: str, name: str = "") -> dict:
    """注册新用户，返回用户信息 + token"""
    email = email.strip().lower()
    if not email or "@" not in email:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="请输入有效邮箱")

    if len(password) < 6:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="密码至少6位")

    pw_hash, salt = hash_password(password)
    user_id = "u_" + secrets.token_hex(12)
    display_name = name.strip() or email.split("@")[0]

    with get_db() as db:
        existing = db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if existing:
            from fastapi import HTTPException
            raise HTTPException(status_code=409, detail="该邮箱已注册，请直接登录")

        db.execute(
            "INSERT INTO users (id, email, password_hash, salt, name) VALUES (?,?,?,?,?)",
            (user_id, email, pw_hash, salt, display_name),
        )
        token = generate_token()
        db.execute("INSERT INTO tokens (token, user_id) VALUES (?,?)", (token, user_id))

    return {
        "token": token,
        "user": {"id": user_id, "email": email, "name": display_name, "avatar": "", "school": "", "bio": ""},
    }


def login_user(email: str, password: str) -> dict:
    """登录，返回用户信息 + token"""
    email = email.strip().lower()

    with get_db() as db:
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if not user:
            from fastapi import HTTPException
            raise HTTPException(status_code=401, detail="邮箱未注册")

        h, _ = hash_password(password, user["salt"])
        if h != user["password_hash"]:
            from fastapi import HTTPException
            raise HTTPException(status_code=401, detail="密码错误")

        token = generate_token()
        db.execute("INSERT INTO tokens (token, user_id) VALUES (?,?)", (token, user["id"]))

    return {
        "token": token,
        "user": {
            "id": user["id"], "email": user["email"], "name": user["name"],
            "avatar": user["avatar"], "school": user["school"], "bio": user["bio"],
        },
    }


def update_profile(token: str, name: str = None, avatar: str = None, school: str = None, bio: str = None) -> dict:
    """更新用户资料"""
    user = require_user(token)
    updates = {}
    if name is not None:
        updates["name"] = name.strip()
    if avatar is not None:
        updates["avatar"] = avatar.strip()
    if school is not None:
        updates["school"] = school.strip()
    if bio is not None:
        updates["bio"] = bio.strip()

    if not updates:
        return {"user": user}

    with get_db() as db:
        set_clause = ", ".join(f"{k}=?" for k in updates)
        values = list(updates.values()) + [user["id"]]
        db.execute(f"UPDATE users SET {set_clause} WHERE id=?", values)

    return {"user": {**user, **updates}}


# ── 动态 ──────────────────────────────────────────────

TOPICS = ["晒生活", "找室友", "二手", "求助", "美食", "旅行", "学习", "其他"]


def create_post(token: str, text: str, topic: str = "", images: list = None) -> dict:
    """发布动态"""
    user = require_user(token)
    text = text.strip()
    if not text:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="内容不能为空")
    if len(text) > 2000:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="内容不能超过2000字")

    post_id = "p_" + secrets.token_hex(8)
    images_json = json.dumps(images or [], ensure_ascii=False)

    with get_db() as db:
        db.execute(
            """INSERT INTO posts (id, user_id, user_name, user_avatar, text, images, topic)
               VALUES (?,?,?,?,?,?,?)""",
            (post_id, user["id"], user["name"], user.get("avatar", ""),
             text, images_json, topic),
        )

    return {
        "id": post_id,
        "user_id": user["id"],
        "user_name": user["name"],
        "user_avatar": user.get("avatar", ""),
        "text": text,
        "images": images or [],
        "topic": topic,
        "likes_count": 0,
        "comments_count": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "liked": False,
    }


def list_posts(token: str = None, topic: str = "", page: int = 1, limit: int = 20) -> dict:
    """获取动态列表（按时间倒序）"""
    offset = (page - 1) * limit
    with get_db() as db:
        if topic:
            rows = db.execute(
                "SELECT * FROM posts WHERE topic=? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (topic, limit, offset),
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM posts ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()

        posts = []
        for r in rows:
            d = dict(r)
            d["images"] = json.loads(d.get("images", "[]"))
            d["liked"] = False
            if token:
                user = get_user_by_token(token)
                if user:
                    liked = db.execute(
                        "SELECT 1 FROM likes WHERE post_id=? AND user_id=?",
                        (d["id"], user["id"]),
                    ).fetchone()
                    d["liked"] = bool(liked)
            posts.append(d)

    return {"posts": posts, "page": page, "has_more": len(posts) == limit}


def delete_post(token: str, post_id: str) -> dict:
    """删除自己的动态"""
    user = require_user(token)
    with get_db() as db:
        post = db.execute("SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()
        if not post:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="动态不存在")
        if post["user_id"] != user["id"]:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail="只能删除自己的动态")
        db.execute("DELETE FROM posts WHERE id=?", (post_id,))
    return {"ok": True}


# ── 评论 ──────────────────────────────────────────────

def add_comment(token: str, post_id: str, text: str) -> dict:
    """添加评论"""
    user = require_user(token)
    text = text.strip()
    if not text:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="评论不能为空")
    if len(text) > 500:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="评论不能超过500字")

    comment_id = "c_" + secrets.token_hex(8)
    with get_db() as db:
        # 验证动态存在
        post = db.execute("SELECT id FROM posts WHERE id=?", (post_id,)).fetchone()
        if not post:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="动态不存在")

        db.execute(
            "INSERT INTO comments (id, post_id, user_id, user_name, text) VALUES (?,?,?,?,?)",
            (comment_id, post_id, user["id"], user["name"], text),
        )
        db.execute(
            "UPDATE posts SET comments_count = (SELECT COUNT(*) FROM comments WHERE post_id=?) WHERE id=?",
            (post_id, post_id),
        )

    return {
        "id": comment_id,
        "post_id": post_id,
        "user_id": user["id"],
        "user_name": user["name"],
        "text": text,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def list_comments(post_id: str) -> list:
    """获取动态的评论列表"""
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM comments WHERE post_id=? ORDER BY created_at ASC",
            (post_id,),
        ).fetchall()
    return [dict(r) for r in rows]


# ── 点赞 ──────────────────────────────────────────────

def toggle_like(token: str, post_id: str) -> dict:
    """切换点赞状态（点赞/取消）"""
    user = require_user(token)
    with get_db() as db:
        existing = db.execute(
            "SELECT id FROM likes WHERE post_id=? AND user_id=?",
            (post_id, user["id"]),
        ).fetchone()

        if existing:
            db.execute("DELETE FROM likes WHERE id=?", (existing["id"],))
            liked = False
        else:
            like_id = "l_" + secrets.token_hex(8)
            db.execute(
                "INSERT INTO likes (id, post_id, user_id) VALUES (?,?,?)",
                (like_id, post_id, user["id"]),
            )
            liked = True

        # 更新点赞计数
        db.execute(
            "UPDATE posts SET likes_count = (SELECT COUNT(*) FROM likes WHERE post_id=?) WHERE id=?",
            (post_id, post_id),
        )

        post = db.execute("SELECT likes_count FROM posts WHERE id=?", (post_id,)).fetchone()

    return {"liked": liked, "likes_count": post["likes_count"] if post else 0}


# ── 好友 ──────────────────────────────────────────────

def send_friend_request(token: str, friend_email: str) -> dict:
    """发送好友请求"""
    user = require_user(token)
    friend_email = friend_email.strip().lower()

    with get_db() as db:
        friend = db.execute("SELECT * FROM users WHERE email=?", (friend_email,)).fetchone()
        if not friend:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="用户不存在")
        if friend["id"] == user["id"]:
            from fastapi import HTTPException
            raise HTTPException(status_code=422, detail="不能加自己为好友")

        # 检查是否已有好友关系
        existing = db.execute(
            "SELECT * FROM friends WHERE user_id=? AND friend_id=?",
            (user["id"], friend["id"]),
        ).fetchone()
        if existing:
            from fastapi import HTTPException
            raise HTTPException(status_code=409, detail="已发送过好友请求")

        req_id = "f_" + secrets.token_hex(8)
        db.execute(
            "INSERT INTO friends (id, user_id, friend_id, friend_name, friend_avatar, status) VALUES (?,?,?,?,?,?)",
            (req_id, user["id"], friend["id"], friend["name"], friend["avatar"] or "", "pending"),
        )
        # 同时给对方创建一条反向记录（待接受）
        rev_id = "f_" + secrets.token_hex(8)
        db.execute(
            "INSERT INTO friends (id, user_id, friend_id, friend_name, friend_avatar, status) VALUES (?,?,?,?,?,?)",
            (rev_id, friend["id"], user["id"], user["name"], user.get("avatar", ""), "pending_received"),
        )

    return {"ok": True, "message": f"已向 {friend['name']} 发送好友请求"}


def accept_friend_request(token: str, friend_id: str) -> dict:
    """接受好友请求"""
    user = require_user(token)
    with get_db() as db:
        # 更新双方状态为 accepted
        db.execute(
            "UPDATE friends SET status='accepted' WHERE user_id=? AND friend_id=? AND status='pending_received'",
            (user["id"], friend_id),
        )
        db.execute(
            "UPDATE friends SET status='accepted' WHERE user_id=? AND friend_id=? AND status='pending'",
            (friend_id, user["id"]),
        )
    return {"ok": True}


def reject_friend_request(token: str, friend_id: str) -> dict:
    """拒绝好友请求"""
    user = require_user(token)
    with get_db() as db:
        db.execute(
            "DELETE FROM friends WHERE user_id=? AND friend_id=?",
            (user["id"], friend_id),
        )
        db.execute(
            "DELETE FROM friends WHERE user_id=? AND friend_id=?",
            (friend_id, user["id"]),
        )
    return {"ok": True}


def list_friends(token: str) -> dict:
    """获取好友列表"""
    user = require_user(token)
    with get_db() as db:
        accepted = db.execute(
            "SELECT * FROM friends WHERE user_id=? AND status='accepted' ORDER BY friend_name",
            (user["id"],),
        ).fetchall()
        pending_sent = db.execute(
            "SELECT * FROM friends WHERE user_id=? AND status='pending' ORDER BY created_at DESC",
            (user["id"],),
        ).fetchall()
        pending_received = db.execute(
            "SELECT * FROM friends WHERE user_id=? AND status='pending_received' ORDER BY created_at DESC",
            (user["id"],),
        ).fetchall()

    return {
        "friends": [dict(r) for r in accepted],
        "pending_sent": [dict(r) for r in pending_sent],
        "pending_received": [dict(r) for r in pending_received],
    }


def search_users(token: str, query: str) -> dict:
    """搜索用户（按邮箱或昵称）"""
    require_user(token)
    q = f"%{query.strip()}%"
    with get_db() as db:
        rows = db.execute(
            "SELECT id, name, avatar, school, email FROM users WHERE email LIKE ? OR name LIKE ? LIMIT 20",
            (q, q),
        ).fetchall()
    return {"users": [dict(r) for r in rows]}


# 启动时自动初始化
def init_db():
    """初始化数据库表（公开接口）"""
    with get_db() as conn:
        pass  # _init_tables is called automatically by get_db if needed

init_db()
