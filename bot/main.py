from src import bot
from src.log import *
from src.dependencies import DependenciesBuilder

def main():
    dependencies = DependenciesBuilder.build()
    bot.start_bot(dependencies)

if __name__ == "__main__":
    main()