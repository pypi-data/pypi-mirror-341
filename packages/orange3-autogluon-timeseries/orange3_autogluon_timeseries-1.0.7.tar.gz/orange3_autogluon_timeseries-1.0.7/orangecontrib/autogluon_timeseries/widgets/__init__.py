import os
import sysconfig

# Путь к справке, если она есть
WIDGET_HELP_PATH = os.path.join(
    sysconfig.get_path("data"),
    "share", "help", "orange3-autogluon-timeseries"
)