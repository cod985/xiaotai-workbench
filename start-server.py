# -*- coding: utf-8 -*-
"""
小台一日游 · 局域网一键启动
双击运行（或命令行执行 python start-server.py），
电脑和手机连同一个 WiFi 后，手机浏览器打开屏幕上显示的地址即可。
按 Ctrl+C 停止服务。
"""
import http.server
import socket
import socketserver

PORT = 8899


def get_lan_ip():
    """取本机局域网 IP（连不通外网时退回 127.0.0.1）"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("223.5.5.5", 80))
        ip = s.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # 不刷访问日志，保持窗口干净


if __name__ == "__main__":
    ip = get_lan_ip()
    with socketserver.TCPServer(("0.0.0.0", PORT), QuietHandler) as httpd:
        print("=" * 44)
        print("  小台一日游 · 本地服务已启动")
        print("=" * 44)
        print("  电脑访问:   http://127.0.0.1:%d" % PORT)
        print("  手机访问:   http://%s:%d" % (ip, PORT))
        print("")
        print("  提示：手机需与电脑连同一个 WiFi；")
        print("  若手机打不开，请在系统防火墙提示中点「允许」。")
        print("  按 Ctrl+C 停止服务。")
        print("=" * 44)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务已停止。")
