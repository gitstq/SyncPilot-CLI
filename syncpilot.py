#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SyncPilot-CLI - Lightweight Terminal File Synchronization & Backup Engine
轻量级终端智能文件同步与备份引擎

A zero-dependency CLI tool for intelligent file synchronization, backup,
and version control with TUI dashboard support.

Author: SyncPilot Team
License: MIT
Version: 1.0.0
"""

import os
import sys
import json
import hashlib
import shutil
import argparse
import fnmatch
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Callable
from dataclasses import dataclass, asdict
from enum import Enum

__version__ = "1.0.0"
__author__ = "SyncPilot Team"


class SyncAction(Enum):
    """同步操作类型"""
    COPY = "copy"
    UPDATE = "update"
    DELETE = "delete"
    SKIP = "skip"
    CONFLICT = "conflict"


class LogLevel(Enum):
    """日志级别"""
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    SILENT = 4


@dataclass
class FileInfo:
    """文件信息数据类"""
    path: str
    size: int
    mtime: float
    checksum: str
    is_dir: bool = False


@dataclass
class SyncTask:
    """同步任务数据类"""
    source: str
    target: str
    action: SyncAction
    source_info: Optional[FileInfo] = None
    target_info: Optional[FileInfo] = None


@dataclass
class SyncStats:
    """同步统计数据类"""
    total_files: int = 0
    copied: int = 0
    updated: int = 0
    deleted: int = 0
    skipped: int = 0
    conflicts: int = 0
    errors: int = 0
    bytes_transferred: int = 0
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    @property
    def duration(self) -> float:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0

    @property
    def speed(self) -> float:
        if self.duration > 0:
            return self.bytes_transferred / self.duration
        return 0.0


class Logger:
    """日志记录器"""
    
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
    }

    def __init__(self, level: LogLevel = LogLevel.INFO, use_color: bool = True):
        self.level = level
        self.use_color = use_color
        self.lock = threading.Lock()

    def _color(self, code: str, text: str) -> str:
        if self.use_color and sys.stdout.isatty():
            return f"{self.COLORS.get(code, '')}{text}{self.COLORS['reset']}"
        return text

    def _log(self, level: LogLevel, prefix: str, message: str, color: str = ''):
        if level.value < self.level.value:
            return
        with self.lock:
            timestamp = datetime.now().strftime("%H:%M:%S")
            colored_prefix = self._color(color, f"[{prefix}]")
            print(f"{self._color('dim', timestamp)} {colored_prefix} {message}")

    def debug(self, message: str):
        self._log(LogLevel.DEBUG, "DEBUG", message, 'dim')

    def info(self, message: str):
        self._log(LogLevel.INFO, "INFO", message, 'blue')

    def success(self, message: str):
        self._log(LogLevel.INFO, "OK", message, 'green')

    def warn(self, message: str):
        self._log(LogLevel.WARN, "WARN", message, 'yellow')

    def error(self, message: str):
        self._log(LogLevel.ERROR, "ERROR", message, 'red')

    def banner(self):
        """打印启动横幅"""
        banner_text = f"""
╔══════════════════════════════════════════════════════════════╗
║  🔄 SyncPilot-CLI v{__version__} - File Sync & Backup Engine       ║
║  Lightweight • Zero Dependencies • Intelligent • Cross-Platform ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(self._color('cyan', banner_text))


class IgnorePattern:
    """.gitignore风格的忽略模式解析器"""
    
    def __init__(self, patterns: List[str] = None):
        self.patterns: List[Tuple[str, bool]] = []  # (pattern, is_negation)
        if patterns:
            for pattern in patterns:
                self.add_pattern(pattern)

    def add_pattern(self, pattern: str):
        """添加忽略模式"""
        pattern = pattern.strip()
        if not pattern or pattern.startswith('#'):
            return
        
        is_negation = pattern.startswith('!')
        if is_negation:
            pattern = pattern[1:]
        
        self.patterns.append((pattern, is_negation))

    def load_from_file(self, filepath: str) -> bool:
        """从文件加载忽略模式"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    self.add_pattern(line)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            return False

    def matches(self, path: str, is_dir: bool = False) -> bool:
        """检查路径是否匹配忽略模式"""
        path = path.replace('\\', '/')
        basename = os.path.basename(path)
        
        ignored = False
        for pattern, is_negation in self.patterns:
            if self._match_pattern(pattern, path, basename, is_dir):
                ignored = not is_negation
        
        return ignored

    def _match_pattern(self, pattern: str, path: str, basename: str, is_dir: bool) -> bool:
        """匹配单个模式"""
        # 目录模式
        if pattern.endswith('/'):
            if not is_dir:
                return False
            pattern = pattern[:-1]
        
        # 处理 /**/ 模式
        if '/**/' in pattern:
            parts = pattern.split('/**/')
            if path.startswith(parts[0]):
                rest = path[len(parts[0]):]
                return fnmatch.fnmatch(rest, '*/' + parts[1]) or fnmatch.fnmatch(rest, parts[1])
        
        # 绝对路径匹配
        if pattern.startswith('/'):
            return fnmatch.fnmatch(path, pattern[1:])
        
        # 匹配任意层级
        if pattern.startswith('**/') or '/' not in pattern:
            simple_pattern = pattern.lstrip('**/')
            if fnmatch.fnmatch(basename, simple_pattern):
                return True
            # 检查路径中的任何部分
            for part in path.split('/'):
                if fnmatch.fnmatch(part, simple_pattern):
                    return True
        
        # 相对路径匹配
        return fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path, '*/' + pattern)


class FileHasher:
    """文件哈希计算器"""
    
    CHUNK_SIZE = 8192

    @staticmethod
    def calculate(filepath: str, algorithm: str = 'md5') -> str:
        """计算文件哈希值"""
        if algorithm == 'md5':
            hasher = hashlib.md5()
        elif algorithm == 'sha256':
            hasher = hashlib.sha256()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(FileHasher.CHUNK_SIZE):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""

    @staticmethod
    def quick_hash(filepath: str) -> str:
        """快速哈希（仅使用文件元数据）"""
        try:
            stat = os.stat(filepath)
            data = f"{stat.st_size}:{stat.st_mtime}"
            return hashlib.md5(data.encode()).hexdigest()
        except Exception:
            return ""


class FileScanner:
    """文件扫描器"""
    
    def __init__(self, ignore_patterns: IgnorePattern = None, use_hash: bool = True):
        self.ignore_patterns = ignore_patterns or IgnorePattern()
        self.use_hash = use_hash
        self.logger = Logger()

    def scan(self, root_path: str, progress_callback: Callable = None) -> Dict[str, FileInfo]:
        """扫描目录并返回文件信息字典"""
        files: Dict[str, FileInfo] = {}
        root_path = os.path.abspath(root_path)
        
        if not os.path.exists(root_path):
            return files
        
        total = 0
        for _, _, filenames in os.walk(root_path):
            total += len(filenames)
        
        processed = 0
        for dirpath, dirnames, filenames in os.walk(root_path):
            # 过滤目录
            dirnames[:] = [
                d for d in dirnames 
                if not self.ignore_patterns.matches(
                    os.path.relpath(os.path.join(dirpath, d), root_path),
                    is_dir=True
                )
            ]
            
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                relpath = os.path.relpath(filepath, root_path)
                
                if self.ignore_patterns.matches(relpath):
                    continue
                
                try:
                    stat = os.stat(filepath)
                    checksum = ""
                    if self.use_hash and stat.st_size < 100 * 1024 * 1024:  # 小于100MB才计算哈希
                        checksum = FileHasher.quick_hash(filepath)
                    
                    files[relpath] = FileInfo(
                        path=relpath,
                        size=stat.st_size,
                        mtime=stat.st_mtime,
                        checksum=checksum,
                        is_dir=False
                    )
                except Exception as e:
                    self.logger.warn(f"Cannot read file: {filepath}")
                
                processed += 1
                if progress_callback:
                    progress_callback(processed, total)
        
        return files


class SyncEngine:
    """同步引擎"""
    
    def __init__(self, logger: Logger = None, dry_run: bool = False):
        self.logger = logger or Logger()
        self.dry_run = dry_run
        self.stats = SyncStats()
        self._stop_requested = False

    def stop(self):
        """请求停止同步"""
        self._stop_requested = True

    def compare(self, source_files: Dict[str, FileInfo], 
                target_files: Dict[str, FileInfo]) -> List[SyncTask]:
        """比较源目录和目标目录，生成同步任务列表"""
        tasks: List[SyncTask] = []
        
        # 检查需要复制或更新的文件
        for relpath, source_info in source_files.items():
            if self._stop_requested:
                break
            
            if relpath not in target_files:
                tasks.append(SyncTask(
                    source=relpath,
                    target=relpath,
                    action=SyncAction.COPY,
                    source_info=source_info
                ))
            else:
                target_info = target_files[relpath]
                if self._is_different(source_info, target_info):
                    tasks.append(SyncTask(
                        source=relpath,
                        target=relpath,
                        action=SyncAction.UPDATE,
                        source_info=source_info,
                        target_info=target_info
                    ))
                else:
                    tasks.append(SyncTask(
                        source=relpath,
                        target=relpath,
                        action=SyncAction.SKIP,
                        source_info=source_info
                    ))
        
        # 检查需要删除的文件（仅在双向同步时）
        for relpath in target_files:
            if self._stop_requested:
                break
            if relpath not in source_files:
                tasks.append(SyncTask(
                    source="",
                    target=relpath,
                    action=SyncAction.DELETE,
                    target_info=target_files[relpath]
                ))
        
        return tasks

    def _is_different(self, source: FileInfo, target: FileInfo) -> bool:
        """判断两个文件是否不同"""
        if source.size != target.size:
            return True
        if abs(source.mtime - target.mtime) > 1:  # 1秒容差
            return True
        if source.checksum and target.checksum and source.checksum != target.checksum:
            return True
        return False

    def execute(self, tasks: List[SyncTask], source_root: str, target_root: str,
                progress_callback: Callable = None) -> SyncStats:
        """执行同步任务"""
        self.stats = SyncStats()
        self.stats.start_time = time.time()
        self.stats.total_files = len(tasks)
        
        for i, task in enumerate(tasks):
            if self._stop_requested:
                self.logger.warn("Sync stopped by user")
                break
            
            try:
                self._execute_task(task, source_root, target_root)
            except Exception as e:
                self.logger.error(f"Failed to sync {task.target}: {e}")
                self.stats.errors += 1
            
            if progress_callback:
                progress_callback(i + 1, len(tasks), task)
        
        self.stats.end_time = time.time()
        return self.stats

    def _execute_task(self, task: SyncTask, source_root: str, target_root: str):
        """执行单个同步任务"""
        if task.action == SyncAction.SKIP:
            self.stats.skipped += 1
            self.logger.debug(f"Skip: {task.target}")
            return
        
        if task.action == SyncAction.COPY:
            self._copy_file(task.source, source_root, target_root)
            self.stats.copied += 1
            self.logger.success(f"Copy: {task.target}")
        
        elif task.action == SyncAction.UPDATE:
            self._copy_file(task.source, source_root, target_root)
            self.stats.updated += 1
            self.logger.success(f"Update: {task.target}")
        
        elif task.action == SyncAction.DELETE:
            self._delete_file(task.target, target_root)
            self.stats.deleted += 1
            self.logger.warn(f"Delete: {task.target}")

    def _copy_file(self, relpath: str, source_root: str, target_root: str):
        """复制文件"""
        source_path = os.path.join(source_root, relpath)
        target_path = os.path.join(target_root, relpath)
        
        if self.dry_run:
            return
        
        # 确保目标目录存在
        target_dir = os.path.dirname(target_path)
        os.makedirs(target_dir, exist_ok=True)
        
        # 复制文件并保留元数据
        shutil.copy2(source_path, target_path)
        
        # 更新统计
        self.stats.bytes_transferred += os.path.getsize(source_path)

    def _delete_file(self, relpath: str, target_root: str):
        """删除文件"""
        target_path = os.path.join(target_root, relpath)
        
        if self.dry_run:
            return
        
        if os.path.isdir(target_path):
            shutil.rmtree(target_path)
        else:
            os.remove(target_path)


class SnapshotManager:
    """快照管理器"""
    
    SNAPSHOT_DIR = ".syncpilot/snapshots"
    
    def __init__(self, root_path: str):
        self.root_path = os.path.abspath(root_path)
        self.snapshot_path = os.path.join(self.root_path, self.SNAPSHOT_DIR)

    def create(self, files: Dict[str, FileInfo], name: str = None) -> str:
        """创建快照"""
        os.makedirs(self.snapshot_path, exist_ok=True)
        
        if name is None:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        snapshot_file = os.path.join(self.snapshot_path, f"{name}.json")
        
        snapshot_data = {
            "created_at": datetime.now().isoformat(),
            "file_count": len(files),
            "files": {k: asdict(v) for k, v in files.items()}
        }
        
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(snapshot_data, f, indent=2)
        
        return snapshot_file

    def list_snapshots(self) -> List[Tuple[str, str, int]]:
        """列出所有快照"""
        snapshots = []
        if not os.path.exists(self.snapshot_path):
            return snapshots
        
        for filename in os.listdir(self.snapshot_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.snapshot_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    snapshots.append((
                        filename[:-5],
                        data.get('created_at', 'Unknown'),
                        data.get('file_count', 0)
                    ))
                except Exception:
                    pass
        
        return sorted(snapshots, key=lambda x: x[0], reverse=True)

    def load(self, name: str) -> Optional[Dict[str, FileInfo]]:
        """加载快照"""
        snapshot_file = os.path.join(self.snapshot_path, f"{name}.json")
        
        if not os.path.exists(snapshot_file):
            return None
        
        with open(snapshot_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {
            k: FileInfo(**v) 
            for k, v in data.get('files', {}).items()
        }


class TUI:
    """终端用户界面"""
    
    def __init__(self, logger: Logger = None):
        self.logger = logger or Logger()
        self.bar_width = 40

    def print_progress_bar(self, current: int, total: int, prefix: str = "Progress"):
        """打印进度条"""
        if total == 0:
            return
        
        percent = current / total
        filled = int(self.bar_width * percent)
        bar = '█' * filled + '░' * (self.bar_width - filled)
        
        sys.stdout.write(f'\r{prefix}: [{bar}] {current}/{total} ({percent*100:.1f}%)')
        sys.stdout.flush()
        
        if current >= total:
            print()  # 完成时换行

    def print_stats(self, stats: SyncStats):
        """打印同步统计"""
        print()
        self.logger.info("═" * 50)
        self.logger.info("📊 Sync Statistics")
        self.logger.info("═" * 50)
        print(f"  📁 Total files:    {stats.total_files}")
        print(f"  ✅ Copied:         {stats.copied}")
        print(f"  🔄 Updated:        {stats.updated}")
        print(f"  🗑️  Deleted:        {stats.deleted}")
        print(f"  ⏭️  Skipped:        {stats.skipped}")
        print(f"  ⚠️  Conflicts:      {stats.conflicts}")
        print(f"  ❌ Errors:         {stats.errors}")
        print(f"  📦 Data transferred: {self._format_bytes(stats.bytes_transferred)}")
        print(f"  ⏱️  Duration:       {stats.duration:.2f}s")
        print(f"  🚀 Speed:          {self._format_bytes(stats.speed)}/s")
        self.logger.info("═" * 50)

    def _format_bytes(self, size: int) -> str:
        """格式化字节大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    def print_comparison(self, tasks: List[SyncTask], max_items: int = 20):
        """打印文件比较结果"""
        print()
        self.logger.info("📋 Sync Preview")
        self.logger.info("─" * 50)
        
        actions = {
            SyncAction.COPY: ("📥 COPY", 'green'),
            SyncAction.UPDATE: ("🔄 UPDATE", 'yellow'),
            SyncAction.DELETE: ("🗑️  DELETE", 'red'),
            SyncAction.SKIP: ("⏭️  SKIP", 'dim'),
            SyncAction.CONFLICT: ("⚠️  CONFLICT", 'magenta'),
        }
        
        shown = 0
        for task in tasks:
            if task.action == SyncAction.SKIP:
                continue
            
            label, color = actions.get(task.action, ("?", 'reset'))
            print(f"  {self.logger._color(color, label)} {task.target}")
            
            shown += 1
            if shown >= max_items:
                remaining = len([t for t in tasks if t.action != SyncAction.SKIP]) - max_items
                if remaining > 0:
                    print(f"  ... and {remaining} more items")
                break
        
        self.logger.info("─" * 50)


def create_default_config(path: str):
    """创建默认配置文件"""
    config = {
        "version": "1.0.0",
        "default_ignore": [
            ".syncpilot/",
            ".git/",
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".DS_Store",
            "Thumbs.db",
            "*.swp",
            "*.swo",
            "*~",
            ".idea/",
            ".vscode/",
            "node_modules/",
            ".env",
            ".venv/",
            "venv/",
        ],
        "profiles": {}
    }
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="SyncPilot-CLI - Intelligent File Synchronization & Backup Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sync ./source ./backup              # 基本同步
  %(prog)s sync ./source ./backup --dry-run    # 预览模式
  %(prog)s sync ./source ./backup --delete     # 同步并删除目标多余文件
  %(prog)s snapshot ./source                   # 创建快照
  %(prog)s snapshot ./source --list            # 列出快照
  %(prog)s compare ./source ./backup           # 比较目录差异
        """
    )
    
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('-q', '--quiet', action='store_true', help='静默模式')
    parser.add_argument('--no-color', action='store_true', help='禁用彩色输出')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # sync 命令
    sync_parser = subparsers.add_parser('sync', help='同步两个目录')
    sync_parser.add_argument('source', help='源目录')
    sync_parser.add_argument('target', help='目标目录')
    sync_parser.add_argument('--dry-run', action='store_true', help='预览模式（不实际执行）')
    sync_parser.add_argument('--delete', action='store_true', help='删除目标目录中多余的文件')
    sync_parser.add_argument('--ignore-file', default='.syncignore', help='忽略模式文件')
    sync_parser.add_argument('--no-hash', action='store_true', help='禁用文件哈希比较')
    
    # snapshot 命令
    snapshot_parser = subparsers.add_parser('snapshot', help='管理目录快照')
    snapshot_parser.add_argument('path', help='目标目录')
    snapshot_parser.add_argument('--list', action='store_true', help='列出所有快照')
    snapshot_parser.add_argument('--load', metavar='NAME', help='加载指定快照')
    snapshot_parser.add_argument('--name', help='快照名称')
    
    # compare 命令
    compare_parser = subparsers.add_parser('compare', help='比较两个目录差异')
    compare_parser.add_argument('source', help='源目录')
    compare_parser.add_argument('target', help='目标目录')
    compare_parser.add_argument('--ignore-file', default='.syncignore', help='忽略模式文件')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.quiet:
        log_level = LogLevel.SILENT
    elif args.verbose:
        log_level = LogLevel.DEBUG
    else:
        log_level = LogLevel.INFO
    
    logger = Logger(level=log_level, use_color=not args.no_color)
    tui = TUI(logger)
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    logger.banner()
    
    if args.command == 'sync':
        # 检查目录
        if not os.path.isdir(args.source):
            logger.error(f"Source directory does not exist: {args.source}")
            sys.exit(1)
        
        if not os.path.exists(args.target):
            logger.info(f"Creating target directory: {args.target}")
            os.makedirs(args.target, exist_ok=True)
        
        # 加载忽略模式
        ignore_patterns = IgnorePattern()
        if os.path.exists(args.ignore_file):
            ignore_patterns.load_from_file(args.ignore_file)
            logger.info(f"Loaded ignore patterns from {args.ignore_file}")
        
        # 添加默认忽略
        default_ignores = [
            ".syncpilot/", ".git/", "__pycache__/", ".DS_Store",
            "*.pyc", "*.pyo", "*.swp", "*~"
        ]
        for pattern in default_ignores:
            ignore_patterns.add_pattern(pattern)
        
        logger.info(f"🔍 Scanning source: {args.source}")
        scanner = FileScanner(ignore_patterns, use_hash=not args.no_hash)
        source_files = scanner.scan(args.source, lambda c, t: tui.print_progress_bar(c, t, "Source"))
        print()
        logger.info(f"   Found {len(source_files)} files")
        
        logger.info(f"🔍 Scanning target: {args.target}")
        target_files = scanner.scan(args.target, lambda c, t: tui.print_progress_bar(c, t, "Target"))
        print()
        logger.info(f"   Found {len(target_files)} files")
        
        # 比较并生成任务
        engine = SyncEngine(logger, dry_run=args.dry_run)
        tasks = engine.compare(source_files, target_files if args.delete else {})
        
        # 显示预览
        tui.print_comparison(tasks)
        
        if args.dry_run:
            logger.info("🔍 Dry run mode - no changes made")
            sys.exit(0)
        
        # 确认执行
        changes = len([t for t in tasks if t.action != SyncAction.SKIP])
        if changes > 0:
            if not args.quiet:
                response = input(f"\nProceed with {changes} changes? [Y/n]: ").strip().lower()
                if response and response not in ('y', 'yes'):
                    logger.info("Cancelled")
                    sys.exit(0)
            
            # 执行同步
            logger.info("🚀 Starting synchronization...")
            stats = engine.execute(
                tasks, args.source, args.target,
                lambda c, t, task: tui.print_progress_bar(c, t, "Syncing")
            )
            print()
            tui.print_stats(stats)
            
            if stats.errors == 0:
                logger.success("✨ Sync completed successfully!")
            else:
                logger.warn(f"⚠️  Sync completed with {stats.errors} errors")
        else:
            logger.success("✨ Everything is up to date!")
    
    elif args.command == 'snapshot':
        if not os.path.isdir(args.path):
            logger.error(f"Directory does not exist: {args.path}")
            sys.exit(1)
        
        snapshot_mgr = SnapshotManager(args.path)
        
        if args.list:
            snapshots = snapshot_mgr.list_snapshots()
            if not snapshots:
                logger.info("No snapshots found")
            else:
                print()
                logger.info("📸 Available Snapshots")
                logger.info("─" * 60)
                for name, created_at, file_count in snapshots:
                    print(f"  📷 {name}")
                    print(f"     Created: {created_at}")
                    print(f"     Files: {file_count}")
                    print()
        elif args.load:
            files = snapshot_mgr.load(args.load)
            if files is None:
                logger.error(f"Snapshot not found: {args.load}")
                sys.exit(1)
            logger.info(f"Loaded snapshot '{args.load}' with {len(files)} files")
        else:
            # 创建快照
            logger.info(f"🔍 Scanning directory: {args.path}")
            scanner = FileScanner()
            files = scanner.scan(args.path, lambda c, t: tui.print_progress_bar(c, t, "Scanning"))
            print()
            
            snapshot_file = snapshot_mgr.create(files, args.name)
            logger.success(f"✨ Snapshot created: {snapshot_file}")
    
    elif args.command == 'compare':
        if not os.path.isdir(args.source):
            logger.error(f"Source directory does not exist: {args.source}")
            sys.exit(1)
        
        if not os.path.isdir(args.target):
            logger.error(f"Target directory does not exist: {args.target}")
            sys.exit(1)
        
        # 加载忽略模式
        ignore_patterns = IgnorePattern()
        if os.path.exists(args.ignore_file):
            ignore_patterns.load_from_file(args.ignore_file)
        
        logger.info(f"🔍 Scanning source: {args.source}")
        scanner = FileScanner(ignore_patterns)
        source_files = scanner.scan(args.source)
        logger.info(f"   Found {len(source_files)} files")
        
        logger.info(f"🔍 Scanning target: {args.target}")
        target_files = scanner.scan(args.target)
        logger.info(f"   Found {len(target_files)} files")
        
        # 比较
        engine = SyncEngine(logger, dry_run=True)
        tasks = engine.compare(source_files, target_files)
        
        tui.print_comparison(tasks, max_items=100)
        
        # 统计
        only_in_source = len([t for t in tasks if t.action == SyncAction.COPY])
        only_in_target = len([t for t in tasks if t.action == SyncAction.DELETE])
        different = len([t for t in tasks if t.action == SyncAction.UPDATE])
        same = len([t for t in tasks if t.action == SyncAction.SKIP])
        
        print()
        logger.info("📊 Comparison Summary")
        logger.info("─" * 40)
        print(f"  📥 Only in source:  {only_in_source}")
        print(f"  📤 Only in target:  {only_in_target}")
        print(f"  🔄 Different:       {different}")
        print(f"  ✅ Identical:       {same}")


if __name__ == '__main__':
    main()
