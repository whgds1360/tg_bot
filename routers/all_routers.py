from routers.menu import menu_router
from routers.start import start_router
from routers.help import help_router


# Здесь хранится список всех роутеров
all_routers = [
    menu_router,
    start_router,
    help_router
]