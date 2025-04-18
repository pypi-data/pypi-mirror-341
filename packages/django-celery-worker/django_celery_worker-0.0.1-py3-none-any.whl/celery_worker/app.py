# _*_coding:utf-8 _*_

import os
from pathlib import Path
from celery import Celery, platforms
from celery.utils.log import get_task_logger

platforms.C_FORCE_ROOT = True
logger = get_task_logger(__name__)


def locate_celery_config():
    """

    """
    # 1. 检查环境变量
    env_path = os.getenv('CELERY_WORKER_PATH')
    if env_path:
        return Path(env_path).resolve().name + ".config"

    # 2. 项目根目录下的文件
    project_root = os.getenv('PYTHONPATH', '.').split(';')[-1]
    project_root = Path(project_root).resolve()
    project_config_path = project_root / 'config.py'
    if project_config_path.exists():
        return "config"

    # 3. 返回包内默认路径
    return Path(__file__).parent.name + ".config"


celery_config = locate_celery_config()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', celery_config)

app = Celery('task')
app.config_from_object(celery_config)

# 自动发现任务
app.autodiscover_tasks()
