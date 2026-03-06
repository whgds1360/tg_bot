from Handlers.menu import menu_router
from Handlers.start import start_router
from Handlers.help import help_router


# Здесь хранится список всех роутеров
all_routers = [
    menu_router,
    start_router,
    help_router
]