import traceback
import random
import time

from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import TaskName, BuildingNames
from tasks.Task import Task


class Scout(Task):
    def __init__(self, bot):
        super().__init__(bot)

    triball_vilages = [random.randint(1000, 1050), random.randint(600,618)]
    mail_pos = [random.randint(1100,1150), random.randint(650,690)]
    report_pos = [random.randint(200,300), random.randint(23,50)]

    def do(self, next_task=TaskName.BREAK):

        try:
            self.set_text(title="Auto Scout")
            while True:
                self.set_text(insert="init view")
                self.back_to_home_gui()
                self.home_gui_full_view()

                # open scout interface
                self.set_text(insert="tap scout camp")
                scout_camp_pos = self.bot.building_pos[BuildingNames.SCOUT_CAMP.value]
                x, y = scout_camp_pos
                self.tap(x, y, 1)

                # find and tap scout button
                self.set_text(insert="open scout camp")
                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    self.tap(x, y, 1)
                else:
                    return next_task

                # find and tap explore button
                self.set_text(insert="try to tap explore")
                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_EXPLORE2_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    self.tap(x, y, 2)
                else:
                    return next_task
                
                # find and tap explore button
                self.set_text(insert="try to tap explore")
                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_EXPLORE3_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    self.tap(x, y, 2)
                else:
                    return next_task

                self.set_text(insert="try to tap send")

                found, name, pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_IDLE_ICON_IMAGE_PATH.value,
                    ImagePathAndProps.SCOUT_ZZ_ICON_IMAGE_PATH.value,
                )
                if found:
                    x, y = pos
                    self.tap(x - 10, y - 10, 2)
                else:
                    return next_task

                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_SEND_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    self.tap(x, y, 2)
                else:
                    return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task

        return next_task
    
    def mail_read_and_claim(self):
        self.open_mail_and_report()
        read_and_claim_x = random.randint(60,200)
        read_and_claim_y = random.randint(660,670)
        self.tap(read_and_claim_x, read_and_claim_y)
        self.tap(random.randint(1100,1200), random.randint(80,150))
        self.back_to_home_gui()
        time.sleep(random.uniform(5.5, 7.5))


    def open_mail_and_report(self):
        self.back_to_map_gui()
        self.menu_should_open(True)
        self.set_text(insert="Open mail")
        x, y = self.mail_pos
        self.tap(x, y, 2)
        self.set_text(insert="Open report")
        x, y = self.report_pos
        self.tap(x, y, 1)

    def claim_villages(self):
        center_x, center_y = self.center_position()
        self.back_to_home_gui()
        self.home_gui_full_view()
        self.menu_should_open(False)
        self.tap(self.triball_vilages[0], self.triball_vilages[1])
        time.sleep(random.uniform(1.2, 2.1))
        self.tap(center_x, center_y)
        time.sleep(random.uniform(2.2, 3.1))
        self.tap(random.randint(540,740), random.randint(630,670))
        time.sleep(random.uniform(2.1, 3.5))

    def investigation(self):
        idx = 0
        while self.bot.config.enableInvestigation:
            self.mail_read_and_claim()
            self.claim_villages()
            self.open_mail_and_report()

            found, name, pos = self.gui.check_any(
                ImagePathAndProps.MAIL_EXPLORATION_REPORT_IMAGE_PATH.value,
                ImagePathAndProps.MAIL_SCOUT_BUTTON_IMAGE_PATH.value,
            )

            if found:
                if (
                    name
                    == ImagePathAndProps.MAIL_EXPLORATION_REPORT_IMAGE_PATH.value[5]
                ):
                    x, y = pos
                    self.tap(x, y, 2)

                result_list = self.gui.find_all_image_props(
                    ImagePathAndProps.MAIL_SCOUT_BUTTON_IMAGE_PATH.value
                )
                result_list.sort(key=lambda result: result["result"][1])

                if idx < len(result_list):
                    x, y = result_list[idx]["result"]
                    self.tap(x, y, 2)
                else:
                    break

                x, y = pos
                self.tap(x, y, 2)

            else:
                break

            x, y = self.center_position()
            self.tap(x, y, 0.1)
            self.tap(x, y, 0.1)
            self.tap(x, y, 0.1)
            self.tap(x, y, 0.1)
            self.tap(x, y, 0.5)

            found, name, pos = self.gui.check_any(
                ImagePathAndProps.INVESTIGATE_BUTTON_IMAGE_PATH.value,
                ImagePathAndProps.GREAT_BUTTON_IMAGE_PATH.value,
            )

            if found:
                x, y = pos
                self.tap(x, y, 2)
            else:
                continue

            if name == ImagePathAndProps.INVESTIGATE_BUTTON_IMAGE_PATH.value[5]:

                found, name, pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_IDLE_ICON_IMAGE_PATH.value,
                    ImagePathAndProps.SCOUT_ZZ_ICON_IMAGE_PATH.value,
                )

                if found:
                    x, y = pos
                    self.tap(x - 10, y - 10, 2)
                else:
                    break

                found, name, pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_SEND_BUTTON_IMAGE_PATH.value,
                )

                if found:
                    x, y = pos
                    self.tap(x, y, 2)
                else:
                    break
            else:
                continue

            idx = idx + 1
