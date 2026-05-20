import argparse
import sqlite3
from typing import Sequence

try:
    from .auth_utils import AUTH_DB_PATH, create_user, delete_user, init_auth_db, list_users, modify_user
except ImportError:
    from auth_utils import AUTH_DB_PATH, create_user, delete_user, init_auth_db, list_users, modify_user


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="管理 strong/weak stock 示範系統的使用者帳號"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init 讓老師第一次拿到範例時，可以先建立 auth.db。
    subparsers.add_parser("init", help="建立 local auth.db 與 users 資料表")

    create_parser = subparsers.add_parser("create", help="新增使用者")
    create_parser.add_argument("--userid", required=True, help="登入帳號")
    create_parser.add_argument("--password", required=True, help="登入密碼")
    create_parser.add_argument("--email", required=True, help="電子郵件")

    modify_parser = subparsers.add_parser("modify", help="修改使用者資料")
    modify_parser.add_argument("--userid", required=True, help="要修改的帳號")
    modify_parser.add_argument("--password", help="新的登入密碼")
    modify_parser.add_argument("--email", help="新的電子郵件")

    delete_parser = subparsers.add_parser("delete", help="刪除使用者")
    delete_parser.add_argument("--userid", required=True, help="要刪除的帳號")

    subparsers.add_parser("list", help="列出所有使用者")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            init_auth_db()
            print(f"已建立資料庫: {AUTH_DB_PATH}")
            return 0

        if args.command == "create":
            create_user(userid=args.userid, password=args.password, email=args.email)
            print(f"已新增使用者: {args.userid}")
            return 0

        if args.command == "modify":
            modify_user(userid=args.userid, password=args.password, email=args.email)
            print(f"已更新使用者: {args.userid}")
            return 0

        if args.command == "delete":
            delete_user(userid=args.userid)
            print(f"已刪除使用者: {args.userid}")
            return 0

        if args.command == "list":
            users = list_users()
            if not users:
                print("目前沒有任何使用者")
                return 0

            for user in users:
                print(f"{user['userid']}\t{user['email']}")
            return 0
    except sqlite3.IntegrityError as exc:
        parser.exit(status=1, message=f"資料庫約束失敗: {exc}\n")
    except ValueError as exc:
        parser.exit(status=1, message=f"{exc}\n")

    parser.exit(status=1, message="未知的指令\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
