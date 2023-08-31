import sys
sys.dont_write_bytecode = True

from modules.gui.windows import main_loop
from modules.tkb_agent.tkb_agent import TKB_Agent
import modules.globals.globals as globals


def main():
    globals.init_globals()
    tkb_agent = TKB_Agent()
    main_loop(tkb_agent)
    # tkb_agent.driver.quit()


if __name__ == '__main__':
    main()