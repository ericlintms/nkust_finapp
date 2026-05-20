import base64
import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import time
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
AUTH_DB_PATH = BASE_DIR / "auth.db"
JWT_COOKIE_NAME = "good_stock_token"
JWT_EXPIRE_SECONDS = 2 * 60 * 60
PBKDF2_ITERATIONS = 200_000

# 這是示範程式，所以提供一個預設 secret 讓學生下載後即可執行。
# 真正部署時仍建議透過環境變數覆寫，避免把正式 secret 寫死在程式裡。
JWT_SECRET = os.environ.get("GOOD_STOCK_JWT_SECRET", "good-stock-demo-secret-change-me")


class AuthError(ValueError):
    """JWT 驗證失敗時統一丟出的錯誤型別。"""


def init_auth_db() -> None:
    """建立 local auth.db 與 users 資料表。"""
    with sqlite3.connect(AUTH_DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                userid TEXT PRIMARY KEY,
                passwd TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )


def _connect_auth_db() -> sqlite3.Connection:
    """每次都回傳新的連線，避免 Web 請求之間共用 sqlite 連線。"""
    conn = sqlite3.connect(AUTH_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    """把明碼密碼轉成 PBKDF2 雜湊格式，方便安全儲存在 auth.db。"""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return "pbkdf2_sha256${iterations}${salt}${digest}".format(
        iterations=PBKDF2_ITERATIONS,
        salt=base64.urlsafe_b64encode(salt).decode("ascii"),
        digest=base64.urlsafe_b64encode(digest).decode("ascii"),
    )


def verify_password(password: str, stored_password: str) -> bool:
    """把使用者輸入再雜湊一次，與資料庫中的結果做常數時間比較。"""
    try:
        algorithm, iterations, salt_b64, digest_b64 = stored_password.split("$", maxsplit=3)
    except ValueError as exc:
        raise ValueError("資料庫中的密碼格式不正確") from exc

    if algorithm != "pbkdf2_sha256":
        raise ValueError(f"不支援的密碼演算法: {algorithm}")

    salt = base64.urlsafe_b64decode(salt_b64.encode("ascii"))
    expected_digest = base64.urlsafe_b64decode(digest_b64.encode("ascii"))
    current_digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        int(iterations),
    )
    return hmac.compare_digest(current_digest, expected_digest)


def list_users() -> list[dict[str, str]]:
    init_auth_db()
    with _connect_auth_db() as conn:
        rows = conn.execute(
            "SELECT userid, email FROM users ORDER BY userid"
        ).fetchall()
    return [dict(row) for row in rows]


def get_user(userid: str) -> dict[str, str] | None:
    init_auth_db()
    with _connect_auth_db() as conn:
        row = conn.execute(
            "SELECT userid, passwd, email FROM users WHERE userid = ?",
            (userid,),
        ).fetchone()
    return dict(row) if row else None


def create_user(userid: str, password: str, email: str) -> None:
    init_auth_db()
    with _connect_auth_db() as conn:
        conn.execute(
            "INSERT INTO users (userid, passwd, email) VALUES (?, ?, ?)",
            (userid, hash_password(password), email),
        )
        conn.commit()


def modify_user(userid: str, password: str | None = None, email: str | None = None) -> None:
    if password is None and email is None:
        raise ValueError("modify 至少要提供 --password 或 --email")

    fields: list[str] = []
    values: list[str] = []

    if password is not None:
        fields.append("passwd = ?")
        values.append(hash_password(password))

    if email is not None:
        fields.append("email = ?")
        values.append(email)

    values.append(userid)

    init_auth_db()
    with _connect_auth_db() as conn:
        cursor = conn.execute(
            f"UPDATE users SET {', '.join(fields)} WHERE userid = ?",
            values,
        )
        conn.commit()

    if cursor.rowcount == 0:
        raise ValueError(f"找不到使用者: {userid}")


def delete_user(userid: str) -> None:
    init_auth_db()
    with _connect_auth_db() as conn:
        cursor = conn.execute("DELETE FROM users WHERE userid = ?", (userid,))
        conn.commit()

    if cursor.rowcount == 0:
        raise ValueError(f"找不到使用者: {userid}")


def authenticate_user(userid: str, password: str) -> dict[str, str] | None:
    """登入時先查帳號，再驗證 PBKDF2 密碼。"""
    user = get_user(userid)
    if user is None:
        return None

    if not verify_password(password, user["passwd"]):
        return None

    return user


def _base64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _base64url_decode(raw: str) -> bytes:
    padding = "=" * (-len(raw) % 4)
    return base64.urlsafe_b64decode((raw + padding).encode("ascii"))


def _sign(message: bytes) -> bytes:
    return hmac.new(JWT_SECRET.encode("utf-8"), message, hashlib.sha256).digest()


def create_jwt(userid: str, expire_seconds: int = JWT_EXPIRE_SECONDS) -> str:
    """
    手刻一個最精簡的 HS256 JWT。

    這樣學生可以直接看到 JWT 的三段式結構：
    1. header：說明演算法與 token 類型
    2. payload：放使用者與到期時間
    3. signature：用 secret 對前兩段簽章，防止內容被竄改
    """
    issued_at = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": userid,
        "iat": issued_at,
        "exp": issued_at + expire_seconds,
    }

    header_segment = _base64url_encode(
        json.dumps(header, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    )
    payload_segment = _base64url_encode(
        json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    )
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    signature_segment = _base64url_encode(_sign(signing_input))
    return f"{header_segment}.{payload_segment}.{signature_segment}"


def decode_jwt(token: str) -> dict[str, object]:
    """驗證 JWT 簽章與 exp，到期或被改過都視為無效。"""
    try:
        header_segment, payload_segment, signature_segment = token.split(".", maxsplit=2)
    except ValueError as exc:
        raise AuthError("JWT 格式不正確") from exc

    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    expected_signature = _base64url_encode(_sign(signing_input))
    if not hmac.compare_digest(expected_signature, signature_segment):
        raise AuthError("JWT 簽章驗證失敗")

    try:
        header = json.loads(_base64url_decode(header_segment))
        payload = json.loads(_base64url_decode(payload_segment))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise AuthError("JWT 內容解析失敗") from exc

    if header.get("alg") != "HS256":
        raise AuthError("JWT 演算法不支援")

    expire_time = payload.get("exp")
    if not isinstance(expire_time, int):
        raise AuthError("JWT 缺少有效的 exp 欄位")

    if expire_time <= int(time.time()):
        raise AuthError("JWT 已過期")

    if not isinstance(payload.get("sub"), str) or not payload["sub"]:
        raise AuthError("JWT 缺少有效的 sub 欄位")

    return payload
