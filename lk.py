import time
import random
import threading
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import tkinter as tk
from tkinter import ttk, messagebox

import keyboard
import win32gui
import win32api
import win32con


I18N = {
    "zh": {
        "window_title": "LK Auto Bow 控制台",
        "hero_title": "LK Auto Bow",
        "hero_subtitle": "",
        "lang_label": "界面语言",
        "lang_zh": "中文",
        "lang_en": "English",
        "status_idle": "空闲：请先绑定游戏窗口。",
        "status_bound": "已停止。游戏窗口已绑定，可点“开始巡逻”。",
        "status_running": "运行中…",
        "status_stopping": "正在停止…",
        "status_bind_prompt": "请将鼠标移到游戏窗口上，3 秒后自动绑定。",
        "status_bind_ok": "绑定成功，可点“开始巡逻”。",
        "status_bind_fail": "绑定失败，请重试。",
        "status_reset": "已将虚拟坐标重置为 (0, 0)。",
        "hint_virtual": "说明：这里显示的是脚本内部的虚拟坐标，用来估算走位倾向，不是游戏真实坐标。",
        "quick_hint": "快捷键：仅当游戏窗口在前台时，按 Q 可停止巡逻，避免在别处打字误触。",
        "btn_bind": "绑定游戏窗口",
        "btn_start": "开始巡逻",
        "btn_stop": "停止",
        "btn_reset": "重置虚拟坐标",
        "btn_rethrow": "一键重扔精灵",
        "card_window": "窗口与运行",
        "card_position": "虚拟位置",
        "card_position_desc": "x 表示左右，y 表示前后",
        "stat_window": "窗口",
        "stat_mode": "状态",
        "stat_hotkey": "停止热键",
        "stat_window_bound": "已绑定",
        "stat_window_unbound": "未绑定",
        "stat_mode_running": "巡逻中",
        "stat_mode_idle": "待机",
        "stat_hotkey_value": "Q / 前台生效",
        "tab_move": "移动",
        "tab_skill": "技能连招",
        "move_intro": "活动范围越大，角色越容易在更大范围内来回；速度越大，每次按键对应的虚拟位移越大。",
        "range_group": "活动范围（虚拟坐标边界）",
        "speed_group": "移动速度系数",
        "interval_group": "巡逻间隔（秒）",
        "rethrow_group": "重扔精灵",
        "rethrow_intro": "手动点击按钮可立刻执行一次。自动重扔开启后，会按 1 到 6 依次按键，随机等待后发送一次左键，再随机等待更长一点切下一只。",
        "scale_rethrow_interval_hours": "自动重扔间隔(小时)",
        "scale_rethrow_key_hold": "左键按住时长",
        "scale_rethrow_click_gap": "按键后点击等待",
        "scale_rethrow_slot_gap": "每只精灵间隔",
        "scale_rethrow_rand_factor": "随机偏移系数",
        "skill_intro": "按顺序执行技能步骤。按键可填 tab / esc / 字母 / 数字；填 wait 表示纯等待。可拖拽左侧 Drag 手柄调整顺序。",
        "skill_timing_group": "技能触发节奏",
        "skill_hold_group": "按键按住时长",
        "skill_seq_group": "技能动作序列",
        "skill_seq_cols": ("拖拽", "按键", "次数", "间隔(秒)"),
        "skill_add": "+ 添加一行",
        "skill_remove": "− 删除末行",
        "delete_short": "删",
        "warn_bind_title": "需要先绑定窗口",
        "warn_bind_body": "请先绑定游戏窗口。",
        "info_running_title": "已经在运行",
        "info_running_body": "巡逻已经在运行中。",
        "info_worker_body": "后台线程仍在运行中。",
        "warn_skill_title": "技能序列无效",
        "warn_skill_body": "请至少保留一个有效步骤：非空按键，或间隔大于 0 的 wait。",
        "warn_rethrow_title": "无法重扔",
        "warn_rethrow_body": "请先绑定游戏窗口。",
        "status_rethrowing": "正在重扔精灵…",
        "status_rethrow_done": "已完成一轮重扔精灵。",
        "status_rethrow_busy": "已有重扔任务在执行，跳过本次请求。",
        "status_rethrow_failed": "重扔精灵未完成，请检查绑定窗口和点击落点。",
        "scale_max_x": "左右最大偏移",
        "scale_max_y": "前后最大偏移",
        "scale_side_speed": "左右 A/D 速度",
        "scale_forward_speed": "前后 W/S 速度",
        "scale_loop_wait_min": "主循环等待最短",
        "scale_loop_wait_max": "主循环等待最长",
        "scale_check_step": "检测步长",
        "scale_patrol_pause_min": "移动后停顿最短",
        "scale_patrol_pause_max": "移动后停顿最长",
        "scale_patrol_center_idle_min": "中心停顿最短",
        "scale_patrol_center_idle_max": "中心停顿最长",
        "scale_patrol_no_move_idle_min": "无动作停顿最短",
        "scale_patrol_no_move_idle_max": "无动作停顿最长",
        "scale_skill_interval": "技能间隔",
        "scale_skill_key_hold": "单次按键时长",
    },
    "en": {
        "window_title": "LK Auto Bow Console",
        "hero_title": "LK Auto Bow",
        "hero_subtitle": "",
        "lang_label": "Language",
        "lang_zh": "中文",
        "lang_en": "English",
        "status_idle": "Idle: bind the game window first.",
        "status_bound": "Stopped. Game window is bound and ready to start.",
        "status_running": "Running...",
        "status_stopping": "Stopping...",
        "status_bind_prompt": "Move your mouse over the game window. It will bind in 3 seconds.",
        "status_bind_ok": "Window bound successfully. You can start now.",
        "status_bind_fail": "Binding failed. Please try again.",
        "status_reset": "Virtual position reset to (0, 0).",
        "hint_virtual": "This is the script's internal virtual position estimate, not the actual in-game coordinates.",
        "quick_hint": "Hotkey: press Q to stop only while the game window is focused.",
        "btn_bind": "Bind Window",
        "btn_start": "Start Patrol",
        "btn_stop": "Stop",
        "btn_reset": "Reset Position",
        "btn_rethrow": "Rethrow Pets",
        "card_window": "Window & Control",
        "card_position": "Virtual Position",
        "card_position_desc": "x = left/right, y = forward/backward",
        "stat_window": "Window",
        "stat_mode": "State",
        "stat_hotkey": "Stop Key",
        "stat_window_bound": "Bound",
        "stat_window_unbound": "Unbound",
        "stat_mode_running": "Patrolling",
        "stat_mode_idle": "Idle",
        "stat_hotkey_value": "Q / focused only",
        "tab_move": "Movement",
        "tab_skill": "Skills",
        "move_intro": "A larger range allows wider roaming. Higher speed makes each key press count as more virtual movement.",
        "range_group": "Range (virtual bounds)",
        "speed_group": "Movement speed",
        "interval_group": "Patrol timing (seconds)",
        "rethrow_group": "Pet Rethrow",
        "rethrow_intro": "Use the button to trigger it immediately. Auto rethrow will press 1 through 6, wait a bit, send one left-click, then wait longer before moving to the next pet.",
        "scale_rethrow_interval_hours": "Auto rethrow interval (hours)",
        "scale_rethrow_key_hold": "Left click hold",
        "scale_rethrow_click_gap": "Wait before click",
        "scale_rethrow_slot_gap": "Gap between pets",
        "scale_rethrow_rand_factor": "Random offset factor",
        "skill_intro": "Steps run from top to bottom. Use tab / esc / letters / numbers, or set key to wait for a delay-only step. Drag the left Drag handle to reorder rows.",
        "skill_timing_group": "Skill timing",
        "skill_hold_group": "Key hold duration",
        "skill_seq_group": "Skill sequence",
        "skill_seq_cols": ("Drag", "Key", "Count", "Gap(s)"),
        "skill_add": "+ Add Row",
        "skill_remove": "- Remove Last",
        "delete_short": "Del",
        "warn_bind_title": "Bind Required",
        "warn_bind_body": "Please bind the game window first.",
        "info_running_title": "Already Running",
        "info_running_body": "Patrol is already running.",
        "info_worker_body": "The worker thread is still active.",
        "warn_skill_title": "Invalid Skill Sequence",
        "warn_skill_body": "Keep at least one valid step: a non-empty key, or a wait step with gap > 0.",
        "warn_rethrow_title": "Cannot Rethrow",
        "warn_rethrow_body": "Please bind the game window first.",
        "status_rethrowing": "Rethrowing pets...",
        "status_rethrow_done": "Finished one full pet rethrow cycle.",
        "status_rethrow_busy": "A rethrow task is already running. Skipping this request.",
        "status_rethrow_failed": "Pet rethrow did not finish. Check the bound window and click target.",
        "scale_max_x": "Max horizontal offset",
        "scale_max_y": "Max vertical offset",
        "scale_side_speed": "A/D speed",
        "scale_forward_speed": "W/S speed",
        "scale_loop_wait_min": "Min main wait",
        "scale_loop_wait_max": "Max main wait",
        "scale_check_step": "Check step",
        "scale_patrol_pause_min": "Min post-move pause",
        "scale_patrol_pause_max": "Max post-move pause",
        "scale_patrol_center_idle_min": "Min center idle",
        "scale_patrol_center_idle_max": "Max center idle",
        "scale_patrol_no_move_idle_min": "Min no-move idle",
        "scale_patrol_no_move_idle_max": "Max no-move idle",
        "scale_skill_interval": "Skill interval",
        "scale_skill_key_hold": "Key hold time",
    },
}


@dataclass
class RethrowTimingPlan:
    key_hold: float
    click_delay: float
    click_hold: float
    slot_delay: float


class GameAutomation:
    def __init__(self):
        self.game_hwnd = None
        self.running = False

        # =========================
        # 配置区
        # =========================

        # 技能循环触发间隔（两次整套序列之间至少相隔多少秒）
        self.skill_interval = 25.0
        # Tab/2/Esc 等按键按住时长（秒）
        self.skill_key_hold_time = 0.12
        # 重扔精灵：按 1~6 并在每次按键后补一个左键点击
        self.rethrow_sequence = ["1", "2", "3", "4", "5", "6"]
        self.rethrow_interval_hours = 0.0
        self.rethrow_click_gap = 0.5
        self.rethrow_slot_gap = 1.0
        self.rethrow_click_hold_time = 0.3
        self.rethrow_rand_factor = 0.3
        # 技能序列：每项 dict 含 key / times / gap（见 perform_skill_combo）
        self.skill_steps: List[Dict[str, Any]] = [
            {"key": "tab", "times": 1, "gap": 0.0},
            {"key": "wait", "times": 1, "gap": 1.0},
            {"key": "2", "times": 2, "gap": 0.25},
            {"key": "wait", "times": 1, "gap": 3.5},
            {"key": "esc", "times": 1, "gap": 0.0},
        ]

        # 主循环：每轮「巡逻移动」结束后的大段等待（秒，可在 UI 调）
        self.loop_wait_min = 20.0
        self.loop_wait_max = 40.0
        # 长等待中每隔多久检查一次 Q / 技能（秒）
        self.check_step = 0.3
        # 每步移动后的小停顿（秒）
        self.patrol_pause_min = 0.08
        self.patrol_pause_max = 0.18
        # 靠近中心时随机停顿时长（秒）
        self.patrol_center_idle_min = 0.25
        self.patrol_center_idle_max = 0.60
        # 本轮无移动键时的停顿时长（秒）
        self.patrol_no_move_idle_min = 0.20
        self.patrol_no_move_idle_max = 0.45

        # 二维虚拟位置
        self.virtual_x = 0.0   # 左右
        self.virtual_y = 0.0   # 前后

        # 活动范围
        self.max_x_offset = 1.5
        self.max_y_offset = 1.5

        # 中心缓冲区
        self.center_tolerance_x = 0.8
        self.center_tolerance_y = 0.8

        # 速度系数：按住 1 秒大概算多少虚拟位移
        self.side_speed_factor = 10.0
        self.forward_speed_factor = 10.0

        # 误差衰减
        self.position_decay = 0.94

        # 中心区域停顿概率
        self.center_idle_chance = 0.45

        # 运行态
        self.last_skill_time = 0.0
        self.last_rethrow_time = 0.0
        self.rethrow_lock = threading.Lock()

    @staticmethod
    def _rand_uniform_range(lo: float, hi: float) -> float:
        a, b = float(lo), float(hi)
        if a > b:
            a, b = b, a
        return random.uniform(a, b)

    def _rand_with_factor(self, base: float, factor: float, floor: float = 0.0) -> float:
        base = float(base)
        factor = max(0.0, float(factor))
        delta = abs(base) * factor
        lo = max(floor, base - delta)
        hi = max(floor, base + delta)
        return self._rand_uniform_range(lo, hi)

    def build_rethrow_timing_plan(self) -> RethrowTimingPlan:
        return RethrowTimingPlan(
            key_hold=self._rand_with_factor(0.12, self.rethrow_rand_factor, 0.03),
            click_delay=self._rand_with_factor(
                self.rethrow_click_gap, self.rethrow_rand_factor, 0.0
            ),
            click_hold=self._rand_with_factor(
                self.rethrow_click_hold_time, self.rethrow_rand_factor, 0.01
            ),
            slot_delay=self._rand_with_factor(
                self.rethrow_slot_gap, self.rethrow_rand_factor, 0.0
            ),
        )

    # =========================
    # 基础工具
    # =========================

    def key_to_vk(self, key: str):
        key = key.lower()

        if len(key) == 1 and key.isalpha():
            return 0x41 + ord(key) - ord('a')

        if key.isdigit():
            return 0x30 + ord(key) - ord('0')

        mapping = {
            'tab': win32con.VK_TAB,
            'space': win32con.VK_SPACE,
            'enter': win32con.VK_RETURN,
            'esc': win32con.VK_ESCAPE,
        }
        return mapping.get(key)

    def send_key_to_window(self, key, hold_time=0.15):
        if not self.game_hwnd:
            print("还没有选中游戏窗口")
            return False

        vk_code = self.key_to_vk(key)
        if vk_code is None:
            print(f"不支持的按键: {key}")
            return False

        try:
            win32api.PostMessage(self.game_hwnd, win32con.WM_KEYDOWN, vk_code, 0)
            time.sleep(hold_time)
            win32api.PostMessage(self.game_hwnd, win32con.WM_KEYUP, vk_code, 0)
            return True
        except Exception as e:
            print(f"发送按键失败 {key}: {e}")
            return False

    def send_left_click_to_window(self, client_point=None, hold_time=None):
        if not self.game_hwnd:
            print("还没有选中游戏窗口")
            return False

        try:
            self.set_foreground()
            time.sleep(0.08)

            if client_point is None:
                left, top, right, bottom = win32gui.GetClientRect(self.game_hwnd)
                cx = max(1, int((right - left) / 2))
                cy = max(1, int((bottom - top) / 2))
            else:
                cx, cy = client_point

            sx, sy = win32gui.ClientToScreen(self.game_hwnd, (cx, cy))
            original_pos = win32api.GetCursorPos()

            win32api.SetCursorPos((sx, sy))
            time.sleep(0.04)
            actual_hold = self.rethrow_click_hold_time if hold_time is None else hold_time
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(actual_hold)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.08)
            win32api.SetCursorPos(original_pos)
            return True
        except Exception as e:
            print(f"发送鼠标左键失败: {e}")
            return False

    def is_game_foreground(self):
        """仅当绑定的游戏窗口或其子窗口在前台时为 True，避免其它软件里按 Q 误停。"""
        if not self.game_hwnd:
            return False
        try:
            fg = win32gui.GetForegroundWindow()
            if not fg:
                return False
            if fg == self.game_hwnd:
                return True
            # 部分引擎焦点落在子 HWND 上
            return bool(win32gui.IsChild(self.game_hwnd, fg))
        except Exception:
            return False

    def should_stop(self):
        if not self.is_game_foreground():
            return False
        if keyboard.is_pressed("q"):
            self.running = False
            return True
        return False

    def interruptible_sleep(self, total_time, step=None):
        if step is None:
            step = self.check_step

        elapsed = 0.0
        while elapsed < total_time and self.running:
            if self.should_stop():
                return False

            sleep_chunk = min(step, total_time - elapsed)
            time.sleep(sleep_chunk)
            elapsed += sleep_chunk

        return self.running

    def controlled_sleep(self, total_time, allow_stop_check=True):
        elapsed = 0.0
        step = self.check_step if allow_stop_check else min(0.05, total_time if total_time > 0 else 0.05)
        while elapsed < total_time:
            if allow_stop_check and self.running and self.should_stop():
                return False
            sleep_chunk = min(step, total_time - elapsed)
            time.sleep(sleep_chunk)
            elapsed += sleep_chunk
            if allow_stop_check and self.running and not self.running:
                return False
        return True

    # =========================
    # 窗口处理
    # =========================

    def set_foreground(self):
        if not self.game_hwnd:
            print("没有窗口可切到前台")
            return False

        try:
            placement = win32gui.GetWindowPlacement(self.game_hwnd)
            if placement[1] == win32con.SW_SHOWMINIMIZED:
                win32gui.ShowWindow(self.game_hwnd, win32con.SW_RESTORE)

            win32gui.SetForegroundWindow(self.game_hwnd)
            return True
        except Exception as e:
            print(f"切前台失败: {e}")
            return False

    def get_top_unreal_window_from_point(self):
        x, y = win32gui.GetCursorPos()
        hwnd = win32gui.WindowFromPoint((x, y))

        if not hwnd:
            return None

        chain = []
        cur = hwnd

        while cur:
            title = win32gui.GetWindowText(cur).strip()
            cls = win32gui.GetClassName(cur).strip()
            chain.append((cur, cls, title))

            if cls == "UnrealWindow":
                return cur, chain

            parent = win32gui.GetParent(cur)
            if not parent:
                break
            cur = parent

        return hwnd, chain

    def select_window_by_mouse(self):
        print("请把鼠标移动到【小号游戏窗口】上。")
        print("3 秒后自动读取鼠标所在窗口...")
        time.sleep(3)

        result = self.get_top_unreal_window_from_point()
        if not result:
            print("没有读取到窗口")
            return False

        hwnd, chain = result

        print("检测到的窗口链：")
        for item_hwnd, item_cls, item_title in chain:
            print(f"  hwnd={item_hwnd} | class={item_cls} | title={item_title}")

        final_cls = win32gui.GetClassName(hwnd).strip()
        final_title = win32gui.GetWindowText(hwnd).strip()
        print(f"\n最终选中的窗口：hwnd={hwnd} | class={final_cls} | title={final_title}")

        self.game_hwnd = hwnd
        return True

    # =========================
    # 虚拟坐标
    # =========================

    def clamp_virtual_position(self):
        self.virtual_x = max(-self.max_x_offset - 1, min(self.virtual_x, self.max_x_offset + 1))
        self.virtual_y = max(-self.max_y_offset - 1, min(self.virtual_y, self.max_y_offset + 1))

    def apply_virtual_move(self, key, hold_time):
        if key == 'd':
            self.virtual_x += hold_time * self.side_speed_factor
        elif key == 'a':
            self.virtual_x -= hold_time * self.side_speed_factor
        elif key == 'w':
            self.virtual_y += hold_time * self.forward_speed_factor
        elif key == 's':
            self.virtual_y -= hold_time * self.forward_speed_factor

        self.clamp_virtual_position()

    def decay_virtual_position(self):
        self.virtual_x *= self.position_decay
        self.virtual_y *= self.position_decay
        self.clamp_virtual_position()

    def is_near_center(self):
        return (
            abs(self.virtual_x) <= self.center_tolerance_x
            and abs(self.virtual_y) <= self.center_tolerance_y
        )

    # =========================
    # 按键执行
    # =========================

    def execute_move_plan(self, move_plan):
        for key, hold_time in move_plan:
            if self.should_stop():
                return False

            success = self.send_key_to_window(key, hold_time)
            if success:
                self.apply_virtual_move(key, hold_time)

        return True

    # =========================
    # 技能逻辑
    # =========================

    def is_skill_ready(self):
        return (time.time() - self.last_skill_time) >= self.skill_interval

    def perform_skill_combo(self):
        """
        按 skill_steps 顺序执行一套技能。
        每步：key 为 wait/sleep 时只睡眠 gap 秒；否则按 times 次发键，同键之间隔 gap 秒。
        """
        steps = list(self.skill_steps) if self.skill_steps else []
        if not steps:
            print("技能序列为空，跳过")
            return True

        print("技能序列:", steps)
        hold = float(self.skill_key_hold_time)

        for step in steps:
            if self.should_stop():
                return False

            raw_key = str(step.get("key", "")).strip().lower()
            try:
                times = max(1, int(step.get("times", 1)))
            except (TypeError, ValueError):
                times = 1
            try:
                gap = max(0.0, float(step.get("gap", 0.0)))
            except (TypeError, ValueError):
                gap = 0.0

            # 纯等待：显式 wait / sleep，或留空键但「间隔」>0
            if raw_key in ("wait", "sleep", "delay") or (
                raw_key == "" and gap > 0.0
            ):
                if gap <= 0.0:
                    continue
                print(f"等待 {gap:.2f}s")
                if not self.interruptible_sleep(gap):
                    return False
                continue
            if raw_key == "":
                continue

            key = raw_key
            print(f"按键 {key} x{times}, 间隔 {gap:.2f}s")
            for i in range(times):
                if self.should_stop():
                    return False
                if not self.send_key_to_window(key, hold):
                    return False
                if i < times - 1 and gap > 0.0:
                    if not self.interruptible_sleep(gap):
                        return False

        return True

    def cast_skill_if_ready(self):
        if not self.is_skill_ready():
            return False

        success = self.perform_skill_combo()
        if not success:
            return False

        self.last_skill_time = time.time()
        return True

    def is_rethrow_due(self):
        if self.rethrow_interval_hours <= 0:
            return False
        return (time.time() - self.last_rethrow_time) >= (
            self.rethrow_interval_hours * 3600.0
        )

    def perform_rethrow_all_pets(self):
        if not self.game_hwnd:
            print("没有绑定游戏窗口，无法重扔精灵")
            return False

        if not self.rethrow_lock.acquire(blocking=False):
            print("已有重扔任务在执行，跳过")
            return None

        try:
            allow_stop_check = self.running
            for key in self.rethrow_sequence:
                plan = self.build_rethrow_timing_plan()
                if not self.perform_single_rethrow_step(key, plan, allow_stop_check):
                    return False

            self.last_rethrow_time = time.time()
            return True
        finally:
            self.rethrow_lock.release()

    def run_rethrow_if_due(self):
        if not self.is_rethrow_due():
            return False
        return self.perform_rethrow_all_pets()

    def perform_single_rethrow_step(
        self, key: str, plan: RethrowTimingPlan, allow_stop_check: bool
    ) -> bool:
        if allow_stop_check and self.should_stop():
            return False
        if not self.send_key_to_window(key, plan.key_hold):
            return False
        if not self.controlled_sleep(plan.click_delay, allow_stop_check):
            return False
        if not self.send_left_click_to_window(hold_time=plan.click_hold):
            return False
        if not self.controlled_sleep(plan.slot_delay, allow_stop_check):
            return False
        return True

    def wait_with_checks(self, total_wait):
        elapsed = 0.0

        while elapsed < total_wait and self.running:
            if self.should_stop():
                return

            self.cast_skill_if_ready()
            self.run_rethrow_if_due()

            chunk = min(self.check_step, total_wait - elapsed)
            time.sleep(chunk)
            elapsed += chunk

    # =========================
    # 巡逻决策
    # =========================

    def choose_side_action(self):
        x = self.virtual_x

        if x >= self.max_x_offset:
            return 'a', random.uniform(0.18, 0.28)

        if x <= -self.max_x_offset:
            return 'd', random.uniform(0.18, 0.28)

        if x > self.center_tolerance_x:
            key = random.choices(['a', 'd', None], weights=[0.65, 0.15, 0.20])[0]
        elif x < -self.center_tolerance_x:
            key = random.choices(['d', 'a', None], weights=[0.65, 0.15, 0.20])[0]
        else:
            key = random.choices([None, 'a', 'd'], weights=[0.60, 0.20, 0.20])[0]

        if key is None:
            return None, 0.0

        if abs(x) > self.center_tolerance_x:
            hold = random.uniform(0.12, 0.22)
        else:
            hold = random.uniform(0.06, 0.14)

        return key, hold

    def choose_forward_action(self):
        y = self.virtual_y

        if y >= self.max_y_offset:
            return 's', random.uniform(0.10, 0.18)

        if y <= -self.max_y_offset:
            return 'w', random.uniform(0.10, 0.18)

        if y > self.center_tolerance_y:
            key = random.choices([None, 's', 'w'], weights=[0.55, 0.30, 0.15])[0]
        elif y < -self.center_tolerance_y:
            key = random.choices(['w', None, 's'], weights=[0.55, 0.30, 0.15])[0]
        else:
            key = random.choices([None, 'w', 's'], weights=[0.70, 0.20, 0.10])[0]

        if key is None:
            return None, 0.0

        if abs(y) > self.center_tolerance_y:
            hold = random.uniform(0.08, 0.16)
        else:
            hold = random.uniform(0.05, 0.10)

        return key, hold

    def build_patrol_move_plan(self):
        move_plan = []

        side_key, side_hold = self.choose_side_action()
        if side_key is not None:
            move_plan.append((side_key, side_hold))

        forward_key, forward_hold = self.choose_forward_action()
        if forward_key is not None:
            move_plan.append((forward_key, forward_hold))

        if move_plan:
            return move_plan

        fallback = random.choice(['a', 'd', 'w', None])
        if fallback is None:
            return []

        return [(fallback, random.uniform(0.05, 0.09))]

    # =========================
    # 巡逻执行
    # =========================

    def patrol_move_once(self):
        print(f"[before] x={self.virtual_x:.2f}, y={self.virtual_y:.2f}")

        if self.is_near_center() and random.random() < self.center_idle_chance:
            idle_time = self._rand_uniform_range(
                self.patrol_center_idle_min, self.patrol_center_idle_max
            )
            print(f"中心区域停顿 {idle_time:.2f}s")
            self.interruptible_sleep(idle_time)
            self.decay_virtual_position()
            print(f"[after idle] x={self.virtual_x:.2f}, y={self.virtual_y:.2f}")
            return

        move_plan = self.build_patrol_move_plan()

        if move_plan:
            print("本轮动作:", move_plan)
            self.execute_move_plan(move_plan)
        else:
            idle_time = self._rand_uniform_range(
                self.patrol_no_move_idle_min, self.patrol_no_move_idle_max
            )
            print(f"无动作，停顿 {idle_time:.2f}s")
            self.interruptible_sleep(idle_time)

        self.decay_virtual_position()

        pause_time = self._rand_uniform_range(
            self.patrol_pause_min, self.patrol_pause_max
        )
        self.interruptible_sleep(pause_time)

        print(
            f"[after] x={self.virtual_x:.2f}, y={self.virtual_y:.2f}, "
            f"pause={pause_time:.2f}s"
        )

    # =========================
    # 主循环
    # =========================

    def run_patrol_loop(self):
        """在独立线程中运行；游戏前台时按 Q，或设置 running=False 可停止。"""
        self.set_foreground()
        time.sleep(1)

        print("Started. Press Q only while the game window is focused to stop.")
        self.running = True
        self.last_skill_time = 0.0

        while self.running:
            self.cast_skill_if_ready()
            self.run_rethrow_if_due()
            self.patrol_move_once()

            total_wait = self._rand_uniform_range(
                self.loop_wait_min, self.loop_wait_max
            )
            print(f"进入等待 {total_wait:.2f}s")
            self.wait_with_checks(total_wait)

        print("脚本已停止")

    def run(self):
        """命令行模式：先选窗口再进入巡逻。"""
        if not self.select_window_by_mouse():
            print("窗口选择失败，脚本结束")
            return
        self.run_patrol_loop()


def _apply_scale_vars_to_automation(auto, vars_bundle):
    """从界面变量同步到自动化实例（主线程调用）。"""
    plain_mappings = {
        "max_x": "max_x_offset",
        "max_y": "max_y_offset",
        "side_speed": "side_speed_factor",
        "forward_speed": "forward_speed_factor",
        "loop_wait_min": "loop_wait_min",
        "loop_wait_max": "loop_wait_max",
        "patrol_pause_min": "patrol_pause_min",
        "patrol_pause_max": "patrol_pause_max",
        "patrol_center_idle_min": "patrol_center_idle_min",
        "patrol_center_idle_max": "patrol_center_idle_max",
        "patrol_no_move_idle_min": "patrol_no_move_idle_min",
        "patrol_no_move_idle_max": "patrol_no_move_idle_max",
        "skill_interval": "skill_interval",
        "skill_key_hold": "skill_key_hold_time",
    }
    for var_key, attr_name in plain_mappings.items():
        setattr(auto, attr_name, float(vars_bundle[var_key].get()))

    auto.check_step = max(0.05, float(vars_bundle["check_step"].get()))
    auto.rethrow_interval_hours = max(
        0.0, float(vars_bundle["rethrow_interval_hours"].get())
    )
    auto.rethrow_click_hold_time = max(
        0.01, float(vars_bundle["rethrow_key_hold"].get())
    )
    auto.rethrow_click_gap = max(0.0, float(vars_bundle["rethrow_click_gap"].get()))
    auto.rethrow_slot_gap = max(0.0, float(vars_bundle["rethrow_slot_gap"].get()))
    auto.rethrow_rand_factor = max(
        0.0, float(vars_bundle["rethrow_rand_factor"].get())
    )


class AutomationUI:
    """简易控制面板：位置、范围、速度、技能间隔、开始/停止。"""

    def __init__(self):
        self.auto = GameAutomation()
        self.worker: Optional[threading.Thread] = None

        self.root = tk.Tk()
        self.current_lang = tk.StringVar(value="zh")
        self.root.title(I18N["zh"]["window_title"])
        self.root.minsize(760, 760)
        self.root.configure(bg="#eef3f8")

        self.status_var = tk.StringVar(value=I18N["zh"]["status_idle"])

        # 与 GameAutomation 默认一致的变量
        self.vars = {
            "max_x": tk.DoubleVar(value=self.auto.max_x_offset),
            "max_y": tk.DoubleVar(value=self.auto.max_y_offset),
            "side_speed": tk.DoubleVar(value=self.auto.side_speed_factor),
            "forward_speed": tk.DoubleVar(value=self.auto.forward_speed_factor),
            "loop_wait_min": tk.DoubleVar(value=self.auto.loop_wait_min),
            "loop_wait_max": tk.DoubleVar(value=self.auto.loop_wait_max),
            "check_step": tk.DoubleVar(value=self.auto.check_step),
            "patrol_pause_min": tk.DoubleVar(value=self.auto.patrol_pause_min),
            "patrol_pause_max": tk.DoubleVar(value=self.auto.patrol_pause_max),
            "patrol_center_idle_min": tk.DoubleVar(
                value=self.auto.patrol_center_idle_min
            ),
            "patrol_center_idle_max": tk.DoubleVar(
                value=self.auto.patrol_center_idle_max
            ),
            "patrol_no_move_idle_min": tk.DoubleVar(
                value=self.auto.patrol_no_move_idle_min
            ),
            "patrol_no_move_idle_max": tk.DoubleVar(
                value=self.auto.patrol_no_move_idle_max
            ),
            "skill_interval": tk.DoubleVar(value=self.auto.skill_interval),
            "skill_key_hold": tk.DoubleVar(value=self.auto.skill_key_hold_time),
            "rethrow_interval_hours": tk.DoubleVar(value=self.auto.rethrow_interval_hours),
            "rethrow_key_hold": tk.DoubleVar(value=self.auto.rethrow_click_hold_time),
            "rethrow_click_gap": tk.DoubleVar(value=self.auto.rethrow_click_gap),
            "rethrow_slot_gap": tk.DoubleVar(value=self.auto.rethrow_slot_gap),
            "rethrow_rand_factor": tk.DoubleVar(value=self.auto.rethrow_rand_factor),
        }

        self._skill_rows: List[Dict[str, Any]] = []
        self._skill_rows_container: Optional[ttk.Frame] = None
        self._scale_meta: List[Dict[str, Any]] = []
        self._dragging_skill_row: Optional[Dict[str, Any]] = None
        self.metric_vars = {
            "window": tk.StringVar(),
            "mode": tk.StringVar(),
            "hotkey": tk.StringVar(),
        }

        self.pos_var = tk.StringVar(value="0.00, 0.00")
        self._configure_styles()
        self._build_layout()
        self._skill_load_from_automation_defaults()
        self._refresh_text()
        self.root.after(120, self._tick)

    def _t(self, key: str):
        return I18N[self.current_lang.get()][key]

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", font=("Microsoft YaHei UI", 10), background="#f4efe8")
        style.configure("Card.TFrame", background="#fffaf2")
        style.configure(
            "Hero.TFrame",
            background="#102033",
        )
        style.configure(
            "HeroTitle.TLabel",
            background="#102033",
            foreground="#ffffff",
            font=("Georgia", 24, "bold"),
        )
        style.configure(
            "HeroSub.TLabel",
            background="#102033",
            foreground="#d7e4ef",
            font=("Microsoft YaHei UI", 10),
        )
        style.configure(
            "SectionTitle.TLabel",
            background="#fffaf2",
            foreground="#243447",
            font=("Segoe UI Semibold", 11),
        )
        style.configure(
            "Hint.TLabel",
            background="#fffaf2",
            foreground="#6b7280",
        )
        style.configure(
            "Status.TLabel",
            background="#fff1d6",
            foreground="#7a4b00",
            font=("Microsoft YaHei UI", 10),
            padding=12,
        )
        style.configure(
            "Primary.TButton",
            font=("Segoe UI Semibold", 10),
            padding=(14, 10),
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#ef7d32"), ("!disabled", "#d8611f")],
            foreground=[("!disabled", "#ffffff")],
        )
        style.configure(
            "Secondary.TButton",
            font=("Microsoft YaHei UI", 10),
            padding=(12, 10),
            background="#fffaf2",
            foreground="#243447",
            bordercolor="#d8c9b2",
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#f5e6d1"), ("!disabled", "#fffaf2")],
        )
        style.configure("TLabelframe", background="#fffaf2", borderwidth=1, relief="solid")
        style.configure(
            "TLabelframe.Label",
            background="#fffaf2",
            foreground="#243447",
            font=("Segoe UI Semibold", 10),
        )
        style.configure("TNotebook", background="#f4efe8", borderwidth=0, tabmargins=(0, 0, 0, 0))
        style.configure(
            "TNotebook.Tab",
            padding=(18, 10),
            font=("Segoe UI Semibold", 10),
            background="#eadfce",
            foreground="#4b5563",
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#102033"), ("!selected", "#eadfce")],
            foreground=[("selected", "#ffffff"), ("!selected", "#4b5563")],
        )

    def _build_layout(self):
        pad = {"padx": 10, "pady": 6}
        outer = ttk.Frame(self.root, padding=16, style="Card.TFrame")
        outer.pack(fill=tk.BOTH, expand=True)

        hero = tk.Frame(outer, bg="#102033", padx=22, pady=22, highlightthickness=0)
        hero.pack(fill=tk.X, pady=(0, 14))
        accent_bar = tk.Frame(hero, bg="#f08a24", height=4)
        accent_bar.pack(fill=tk.X, pady=(0, 14))
        self.hero_title_label = ttk.Label(hero, style="HeroTitle.TLabel")
        self.hero_title_label.pack(anchor=tk.W)
        top_line = tk.Frame(hero, bg="#102033")
        top_line.pack(fill=tk.X, pady=(8, 0))
        self.hero_subtitle_label = ttk.Label(top_line, style="HeroSub.TLabel")
        self.hero_subtitle_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        lang_box = tk.Frame(top_line, bg="#102033")
        lang_box.pack(side=tk.RIGHT)
        self.lang_label = ttk.Label(lang_box, style="HeroSub.TLabel")
        self.lang_label.pack(side=tk.LEFT, padx=(0, 8))
        self.lang_zh_button = tk.Button(
            lang_box,
            bd=0,
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: self._set_lang("zh"),
        )
        self.lang_zh_button.pack(side=tk.LEFT, padx=(0, 6))
        self.lang_en_button = tk.Button(
            lang_box,
            bd=0,
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: self._set_lang("en"),
        )
        self.lang_en_button.pack(side=tk.LEFT)

        metrics_row = tk.Frame(hero, bg="#102033")
        metrics_row.pack(fill=tk.X, pady=(16, 0))
        self.metric_cards = {}
        self.metric_cards["window"] = self._make_metric_card(metrics_row)
        self.metric_cards["window"]["frame"].pack(side=tk.LEFT, padx=(0, 10))
        self.metric_cards["mode"] = self._make_metric_card(metrics_row)
        self.metric_cards["mode"]["frame"].pack(side=tk.LEFT, padx=(0, 10))
        self.metric_cards["hotkey"] = self._make_metric_card(metrics_row)
        self.metric_cards["hotkey"]["frame"].pack(side=tk.LEFT)

        self.status_label = ttk.Label(
            outer,
            textvariable=self.status_var,
            wraplength=680,
            style="Status.TLabel",
        )
        self.status_label.pack(fill=tk.X, **pad)

        self.virtual_hint_label = ttk.Label(
            outer,
            wraplength=680,
            style="Hint.TLabel",
        )
        self.virtual_hint_label.pack(fill=tk.X, padx=10, pady=(0, 8))

        top_cards = ttk.Frame(outer, style="Card.TFrame")
        top_cards.pack(fill=tk.X)

        control_card = ttk.LabelFrame(top_cards)
        control_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8), pady=(0, 8))
        self.control_title = ttk.Label(control_card, style="SectionTitle.TLabel")
        self.control_title.pack(anchor=tk.W, padx=10, pady=(10, 4))

        row_btns = ttk.Frame(control_card)
        row_btns.pack(fill=tk.X, padx=10, pady=(4, 12))
        self.bind_button = ttk.Button(
            row_btns, command=self._on_bind, style="Secondary.TButton"
        )
        self.bind_button.pack(side=tk.LEFT, padx=(0, 8))
        self.start_button = ttk.Button(
            row_btns, command=self._on_start, style="Primary.TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 8))
        self.stop_button = ttk.Button(
            row_btns, command=self._on_stop, style="Secondary.TButton"
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 8))
        self.reset_button = ttk.Button(
            row_btns,
            command=self._on_reset_virtual_pos,
            style="Secondary.TButton",
        )
        self.reset_button.pack(side=tk.LEFT)
        self.rethrow_button = ttk.Button(
            control_card,
            command=self._on_rethrow,
            style="Secondary.TButton",
        )
        self.rethrow_button.pack(anchor=tk.W, padx=10, pady=(0, 12))

        pos_f = ttk.LabelFrame(top_cards)
        pos_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 8))
        self.position_frame = pos_f
        self.position_title = ttk.Label(pos_f, style="SectionTitle.TLabel")
        self.position_title.pack(anchor=tk.W, padx=10, pady=(10, 2))
        self.position_desc = ttk.Label(pos_f, style="Hint.TLabel")
        self.position_desc.pack(anchor=tk.W, padx=10, pady=(0, 4))
        ttk.Label(pos_f, textvariable=self.pos_var, font=("Consolas", 18)).pack(
            anchor=tk.W, padx=8, pady=6
        )

        def add_scale(parent, key, label, frm, to):
            f = ttk.Frame(parent)
            f.pack(fill=tk.X, **pad)
            label_widget = ttk.Label(f, width=24)
            label_widget.pack(side=tk.LEFT, anchor=tk.W)
            s = ttk.Scale(
                f,
                from_=frm,
                to=to,
                orient=tk.HORIZONTAL,
                variable=self.vars[key],
            )
            s.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
            ttk.Label(f, textvariable=self.vars[key], width=6).pack(side=tk.LEFT)
            self._scale_meta.append({"widget": label_widget, "text_key": label})

        nb = ttk.Notebook(outer)
        nb.pack(fill=tk.BOTH, expand=True, **pad)
        self.notebook = nb

        tab_move, tab_move_body = self._create_scrollable_tab(nb)
        nb.add(tab_move, text="")
        self.tab_move = tab_move
        self.move_intro_label = ttk.Label(
            tab_move_body,
            wraplength=400,
            style="Hint.TLabel",
        )
        self.move_intro_label.pack(fill=tk.X, **pad)
        rng = ttk.LabelFrame(tab_move_body)
        rng.pack(fill=tk.X, **pad)
        self.range_group = rng
        add_scale(rng, "max_x", "scale_max_x", 0.3, 4.0)
        add_scale(rng, "max_y", "scale_max_y", 0.3, 4.0)

        spd = ttk.LabelFrame(tab_move_body)
        spd.pack(fill=tk.X, **pad)
        self.speed_group = spd
        add_scale(spd, "side_speed", "scale_side_speed", 1.0, 30.0)
        add_scale(spd, "forward_speed", "scale_forward_speed", 1.0, 30.0)

        iv = ttk.LabelFrame(tab_move_body)
        iv.pack(fill=tk.X, **pad)
        self.interval_group = iv
        add_scale(iv, "loop_wait_min", "scale_loop_wait_min", 3.0, 120.0)
        add_scale(iv, "loop_wait_max", "scale_loop_wait_max", 3.0, 180.0)
        add_scale(
            iv,
            "check_step",
            "scale_check_step",
            0.1,
            1.5,
        )
        add_scale(iv, "patrol_pause_min", "scale_patrol_pause_min", 0.02, 0.8)
        add_scale(iv, "patrol_pause_max", "scale_patrol_pause_max", 0.02, 1.2)
        add_scale(iv, "patrol_center_idle_min", "scale_patrol_center_idle_min", 0.05, 2.0)
        add_scale(iv, "patrol_center_idle_max", "scale_patrol_center_idle_max", 0.05, 4.0)
        add_scale(iv, "patrol_no_move_idle_min", "scale_patrol_no_move_idle_min", 0.05, 2.0)
        add_scale(iv, "patrol_no_move_idle_max", "scale_patrol_no_move_idle_max", 0.05, 4.0)

        rt = ttk.LabelFrame(tab_move_body)
        rt.pack(fill=tk.X, **pad)
        self.rethrow_group = rt
        self.rethrow_intro_label = ttk.Label(
            rt,
            wraplength=560,
            style="Hint.TLabel",
        )
        self.rethrow_intro_label.pack(fill=tk.X, padx=10, pady=(8, 4))
        add_scale(rt, "rethrow_interval_hours", "scale_rethrow_interval_hours", 0.0, 12.0)
        add_scale(rt, "rethrow_key_hold", "scale_rethrow_key_hold", 0.02, 0.8)
        add_scale(rt, "rethrow_click_gap", "scale_rethrow_click_gap", 0.0, 1.0)
        add_scale(rt, "rethrow_slot_gap", "scale_rethrow_slot_gap", 0.0, 2.0)
        add_scale(rt, "rethrow_rand_factor", "scale_rethrow_rand_factor", 0.0, 1.0)

        tab_skill, tab_skill_body = self._create_scrollable_tab(nb)
        nb.add(tab_skill, text="")
        self.tab_skill = tab_skill
        self.skill_intro_label = ttk.Label(
            tab_skill_body,
            wraplength=400,
            style="Hint.TLabel",
        )
        self.skill_intro_label.pack(fill=tk.X, **pad)
        sk_iv = ttk.LabelFrame(tab_skill_body)
        sk_iv.pack(fill=tk.X, **pad)
        self.skill_timing_group = sk_iv
        add_scale(sk_iv, "skill_interval", "scale_skill_interval", 3.0, 120.0)

        sk_hold = ttk.LabelFrame(tab_skill_body)
        sk_hold.pack(fill=tk.X, **pad)
        self.skill_hold_group = sk_hold
        add_scale(sk_hold, "skill_key_hold", "scale_skill_key_hold", 0.05, 0.35)

        self._build_skill_sequence_editor(tab_skill_body, pad)

        self.quick_hint_label = ttk.Label(
            outer,
            style="Hint.TLabel",
        )
        self.quick_hint_label.pack(anchor=tk.W, **pad)

    def _make_metric_card(self, parent):
        frame = tk.Frame(parent, bg="#1a3148", padx=12, pady=10)
        title = tk.Label(
            frame,
            bg="#1a3148",
            fg="#9fb7ca",
            font=("Segoe UI", 9),
        )
        title.pack(anchor=tk.W)
        value = tk.Label(
            frame,
            bg="#1a3148",
            fg="#ffffff",
            font=("Segoe UI Semibold", 11),
        )
        value.pack(anchor=tk.W, pady=(3, 0))
        return {"frame": frame, "title": title, "value": value}

    def _create_scrollable_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=0)
        canvas = tk.Canvas(tab, highlightthickness=0, bg="#fffaf2")
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
        body = ttk.Frame(canvas, padding=4, style="Card.TFrame")

        body.bind(
            "<Configure>",
            lambda _e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas_window = canvas.create_window((0, 0), window=body, anchor=tk.NW)
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(canvas_window, width=e.width),
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Enter>", lambda _e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda _e: canvas.unbind_all("<MouseWheel>"))

        return tab, body

    def _style_lang_button(self, button, active: bool):
        if active:
            button.configure(
                bg="#f08a24",
                fg="#ffffff",
                activebackground="#f08a24",
                activeforeground="#ffffff",
            )
        else:
            button.configure(
                bg="#22384e",
                fg="#d7e4ef",
                activebackground="#304961",
                activeforeground="#ffffff",
            )

    def _set_lang(self, lang: str):
        if self.current_lang.get() == lang:
            return
        self.current_lang.set(lang)
        self._refresh_text()

    def _update_header_metrics(self):
        self.metric_vars["window"].set(
            self._t("stat_window_bound") if self.auto.game_hwnd else self._t("stat_window_unbound")
        )
        self.metric_vars["mode"].set(
            self._t("stat_mode_running") if self.auto.running else self._t("stat_mode_idle")
        )
        self.metric_vars["hotkey"].set(self._t("stat_hotkey_value"))

    def _build_skill_sequence_editor(self, parent, pad):
        """可编辑技能步骤：按键、次数、间隔；+ / − 增删行。"""
        box = ttk.LabelFrame(parent)
        box.pack(fill=tk.BOTH, expand=True, **pad)
        self.skill_seq_group = box

        head = ttk.Frame(box)
        head.pack(fill=tk.X, padx=4, pady=(4, 2))
        self.skill_col_drag = ttk.Label(head, width=8)
        self.skill_col_drag.pack(side=tk.LEFT, padx=(0, 4))
        self.skill_col_key = ttk.Label(head, width=12)
        self.skill_col_key.pack(side=tk.LEFT, padx=(0, 4))
        self.skill_col_times = ttk.Label(head, width=6)
        self.skill_col_times.pack(side=tk.LEFT, padx=(0, 4))
        self.skill_col_gap = ttk.Label(head, width=10)
        self.skill_col_gap.pack(side=tk.LEFT, padx=(0, 4))
        ttk.Label(head, text="", width=6).pack(side=tk.LEFT)

        wrap = ttk.Frame(box)
        wrap.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self._skill_canvas = tk.Canvas(
            wrap,
            height=220,
            highlightthickness=0,
            bg="#f8fbff",
        )
        sb = ttk.Scrollbar(wrap, orient=tk.VERTICAL, command=self._skill_canvas.yview)
        self._skill_rows_container = ttk.Frame(self._skill_canvas)
        self._skill_rows_container.bind(
            "<Configure>",
            lambda _e: self._skill_canvas.configure(
                scrollregion=self._skill_canvas.bbox("all")
            ),
        )
        self._skill_canvas_window = self._skill_canvas.create_window(
            (0, 0),
            window=self._skill_rows_container,
            anchor=tk.NW,
        )
        self._skill_canvas.bind(
            "<Configure>",
            lambda e: self._skill_canvas.itemconfig(
                self._skill_canvas_window, width=e.width
            ),
        )
        self._skill_canvas.configure(yscrollcommand=sb.set)
        self._skill_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            self._skill_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self._skill_canvas.bind("<Enter>", lambda _e: self._skill_canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self._skill_canvas.bind("<Leave>", lambda _e: self._skill_canvas.unbind_all("<MouseWheel>"))

        btn_row = ttk.Frame(box)
        btn_row.pack(fill=tk.X, padx=4, pady=(2, 6))
        self.skill_add_button = ttk.Button(btn_row, command=self._skill_add_row_default)
        self.skill_add_button.pack(
            side=tk.LEFT, padx=(0, 6)
        )
        self.skill_remove_button = ttk.Button(btn_row, command=self._skill_remove_last_row)
        self.skill_remove_button.pack(
            side=tk.LEFT, padx=(0, 6)
        )

    def _skill_add_row(self, key: str = "", times: int = 1, gap: float = 0.0):
        if self._skill_rows_container is None:
            return
        f = ttk.Frame(self._skill_rows_container)
        f.pack(fill=tk.X, pady=1)

        k_var = tk.StringVar(value=key)
        t_var = tk.StringVar(value=str(int(times)))
        g_var = tk.StringVar(value=str(gap))

        drag_handle = tk.Label(
            f,
            text="Drag",
            width=7,
            bg="#eadfce",
            fg="#243447",
            cursor="fleur",
            padx=4,
            pady=3,
        )
        drag_handle.pack(side=tk.LEFT, padx=(0, 4))
        ent_k = ttk.Entry(f, textvariable=k_var, width=14)
        ent_k.pack(side=tk.LEFT, padx=(0, 4))
        ent_t = ttk.Entry(f, textvariable=t_var, width=6)
        ent_t.pack(side=tk.LEFT, padx=(0, 4))
        ent_g = ttk.Entry(f, textvariable=g_var, width=10)
        ent_g.pack(side=tk.LEFT, padx=(0, 4))

        row: Dict[str, Any] = {
            "frame": f,
            "drag_handle": drag_handle,
            "key": k_var,
            "times": t_var,
            "gap": g_var,
        }

        def remove_this(r=row):
            if r in self._skill_rows:
                self._skill_rows.remove(r)
            r["frame"].destroy()

        delete_btn = ttk.Button(f, width=4, command=remove_this)
        delete_btn.pack(side=tk.RIGHT)
        self._skill_rows.append(row)
        row["delete_btn"] = delete_btn
        drag_handle.bind("<ButtonPress-1>", lambda event, r=row: self._start_skill_drag(r, event))
        drag_handle.bind("<B1-Motion>", self._on_skill_drag_motion)
        drag_handle.bind("<ButtonRelease-1>", self._end_skill_drag)
        self._refresh_skill_row_labels()

    def _skill_add_row_default(self):
        self._skill_add_row("2", 1, 0.0)

    def _skill_remove_last_row(self):
        if not self._skill_rows:
            return
        row = self._skill_rows.pop()
        row["frame"].destroy()

    def _skill_clear_all_rows(self):
        for row in list(self._skill_rows):
            row["frame"].destroy()
        self._skill_rows.clear()
        self._dragging_skill_row = None

    def _refresh_skill_row_labels(self):
        delete_text = self._t("delete_short")
        for row in self._skill_rows:
            row["delete_btn"].configure(text=delete_text)

    def _repack_skill_rows(self):
        for row in self._skill_rows:
            row["frame"].pack_forget()
        for row in self._skill_rows:
            row["frame"].pack(fill=tk.X, pady=1)
        self._skill_canvas.configure(scrollregion=self._skill_canvas.bbox("all"))

    def _start_skill_drag(self, row: Dict[str, Any], _event):
        self._dragging_skill_row = row
        row["drag_handle"].configure(bg="#d8611f", fg="#ffffff")

    def _on_skill_drag_motion(self, event):
        if self._dragging_skill_row is None or not self._skill_rows:
            return

        pointer_y = event.widget.winfo_pointery()
        remaining_rows = [row for row in self._skill_rows if row is not self._dragging_skill_row]
        target_index = len(remaining_rows)

        for idx, row in enumerate(remaining_rows):
            mid_y = row["frame"].winfo_rooty() + (row["frame"].winfo_height() / 2)
            if pointer_y < mid_y:
                target_index = idx
                break

        new_rows = list(remaining_rows)
        new_rows.insert(target_index, self._dragging_skill_row)
        if new_rows != self._skill_rows:
            self._skill_rows = new_rows
            self._repack_skill_rows()

        canvas_top = self._skill_canvas.winfo_rooty()
        canvas_bottom = canvas_top + self._skill_canvas.winfo_height()
        if pointer_y < canvas_top + 24:
            self._skill_canvas.yview_scroll(-1, "units")
        elif pointer_y > canvas_bottom - 24:
            self._skill_canvas.yview_scroll(1, "units")

    def _end_skill_drag(self, _event):
        if self._dragging_skill_row is None:
            return
        self._dragging_skill_row["drag_handle"].configure(bg="#eadfce", fg="#243447")
        self._dragging_skill_row = None

    def _skill_load_from_automation_defaults(self):
        self._skill_clear_all_rows()
        for st in self.auto.skill_steps:
            self._skill_add_row(
                str(st.get("key", "")),
                int(st.get("times", 1)),
                float(st.get("gap", 0.0)),
            )

    def _skill_steps_from_ui(self) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for row in self._skill_rows:
            raw_k = row["key"].get().strip()
            try:
                ti = int(row["times"].get().strip())
            except (ValueError, AttributeError):
                ti = 1
            gs = row["gap"].get().strip().replace(",", ".")
            try:
                gf = float(gs) if gs else 0.0
            except ValueError:
                gf = 0.0
            out.append(
                {
                    "key": raw_k,
                    "times": max(1, ti),
                    "gap": max(0.0, gf),
                }
            )
        return out

    def _skill_sequence_has_valid_step(self) -> bool:
        for row in self._skill_rows:
            k = row["key"].get().strip().lower()
            gs = row["gap"].get().strip().replace(",", ".")
            try:
                gf = float(gs) if gs else 0.0
            except ValueError:
                gf = 0.0
            if k in ("wait", "sleep", "delay", ""):
                if gf > 0.0:
                    return True
                continue
            if k:
                return True
        return False

    def _tick(self):
        _apply_scale_vars_to_automation(self.auto, self.vars)
        self.auto.skill_steps = self._skill_steps_from_ui()
        self.pos_var.set(
            f"{self.auto.virtual_x:.2f}, {self.auto.virtual_y:.2f}"
        )
        if self.auto.running:
            self.status_var.set(self._t("status_running"))
        elif self.auto.game_hwnd:
            self.status_var.set(self._t("status_bound"))
        self._update_header_metrics()
        self.root.after(120, self._tick)

    def _on_bind(self):
        self.status_var.set(self._t("status_bind_prompt"))

        def task():
            ok = self.auto.select_window_by_mouse()
            self.root.after(
                0,
                lambda: self.status_var.set(
                    self._t("status_bind_ok") if ok else self._t("status_bind_fail")
                ),
            )

        threading.Thread(target=task, daemon=True).start()

    def _on_start(self):
        if not self.auto.game_hwnd:
            messagebox.showwarning(
                self._t("warn_bind_title"),
                self._t("warn_bind_body"),
            )
            return
        if self.auto.running:
            messagebox.showinfo(
                self._t("info_running_title"),
                self._t("info_running_body"),
            )
            return
        if self.worker is not None and self.worker.is_alive():
            messagebox.showinfo(
                self._t("info_running_title"),
                self._t("info_worker_body"),
            )
            return

        _apply_scale_vars_to_automation(self.auto, self.vars)
        self.auto.skill_steps = self._skill_steps_from_ui()
        if not self._skill_sequence_has_valid_step():
            messagebox.showwarning(
                self._t("warn_skill_title"),
                self._t("warn_skill_body"),
            )
            return

        def task():
            try:
                self.auto.run_patrol_loop()
            except Exception as e:
                print(f"Patrol error: {e}")
            finally:
                self.auto.running = False

        self.worker = threading.Thread(target=task, daemon=True)
        self.worker.start()
        self.status_var.set(self._t("status_running"))

    def _on_stop(self):
        self.auto.running = False
        self.status_var.set(self._t("status_stopping"))

    def _on_reset_virtual_pos(self):
        self.auto.virtual_x = 0.0
        self.auto.virtual_y = 0.0
        self.pos_var.set("0.00, 0.00")
        self.status_var.set(self._t("status_reset"))

    def _on_rethrow(self):
        if not self.auto.game_hwnd:
            messagebox.showwarning(
                self._t("warn_rethrow_title"),
                self._t("warn_rethrow_body"),
            )
            return

        _apply_scale_vars_to_automation(self.auto, self.vars)
        self.status_var.set(self._t("status_rethrowing"))

        def task():
            result = self.auto.perform_rethrow_all_pets()
            self.root.after(
                0,
                lambda: self.status_var.set(
                    self._t("status_rethrow_done")
                    if result is True
                    else (
                        self._t("status_rethrow_busy")
                        if result is None
                        else self._t("status_rethrow_failed")
                    )
                ),
            )

        threading.Thread(target=task, daemon=True).start()

    def _refresh_text(self):
        self.root.title(self._t("window_title"))
        self.hero_title_label.configure(text=self._t("hero_title"))
        self.hero_subtitle_label.configure(text=self._t("hero_subtitle"))
        self.lang_label.configure(text=self._t("lang_label"))
        self.lang_zh_button.configure(text=self._t("lang_zh"))
        self.lang_en_button.configure(text=self._t("lang_en"))
        self._style_lang_button(self.lang_zh_button, self.current_lang.get() == "zh")
        self._style_lang_button(self.lang_en_button, self.current_lang.get() == "en")
        self.virtual_hint_label.configure(text=self._t("hint_virtual"))
        self.control_title.configure(text=self._t("card_window"))
        self.bind_button.configure(text=self._t("btn_bind"))
        self.start_button.configure(text=self._t("btn_start"))
        self.stop_button.configure(text=self._t("btn_stop"))
        self.reset_button.configure(text=self._t("btn_reset"))
        self.rethrow_button.configure(text=self._t("btn_rethrow"))
        self.position_title.configure(text=self._t("card_position"))
        self.position_desc.configure(text=self._t("card_position_desc"))
        self.notebook.tab(self.tab_move, text=self._t("tab_move"))
        self.notebook.tab(self.tab_skill, text=self._t("tab_skill"))
        self.move_intro_label.configure(text=self._t("move_intro"))
        self.range_group.configure(text=self._t("range_group"))
        self.speed_group.configure(text=self._t("speed_group"))
        self.interval_group.configure(text=self._t("interval_group"))
        self.rethrow_group.configure(text=self._t("rethrow_group"))
        self.rethrow_intro_label.configure(text=self._t("rethrow_intro"))
        self.skill_intro_label.configure(text=self._t("skill_intro"))
        self.skill_timing_group.configure(text=self._t("skill_timing_group"))
        self.skill_hold_group.configure(text=self._t("skill_hold_group"))
        self.skill_seq_group.configure(text=self._t("skill_seq_group"))
        cols = self._t("skill_seq_cols")
        self.skill_col_drag.configure(text=cols[0])
        self.skill_col_key.configure(text=cols[1])
        self.skill_col_times.configure(text=cols[2])
        self.skill_col_gap.configure(text=cols[3])
        self.skill_add_button.configure(text=self._t("skill_add"))
        self.skill_remove_button.configure(text=self._t("skill_remove"))
        self.quick_hint_label.configure(text=self._t("quick_hint"))
        self.metric_cards["window"]["title"].configure(text=self._t("stat_window"))
        self.metric_cards["mode"]["title"].configure(text=self._t("stat_mode"))
        self.metric_cards["hotkey"]["title"].configure(text=self._t("stat_hotkey"))
        self.metric_cards["window"]["value"].configure(textvariable=self.metric_vars["window"])
        self.metric_cards["mode"]["value"].configure(textvariable=self.metric_vars["mode"])
        self.metric_cards["hotkey"]["value"].configure(textvariable=self.metric_vars["hotkey"])
        for meta in self._scale_meta:
            meta["widget"].configure(text=self._t(meta["text_key"]))
        self._refresh_skill_row_labels()
        self._update_header_metrics()
        if not self.auto.running:
            if self.auto.game_hwnd:
                self.status_var.set(self._t("status_bound"))
            else:
                self.status_var.set(self._t("status_idle"))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] in ("--cli", "-c"):
        GameAutomation().run()
    else:
        AutomationUI().run()
