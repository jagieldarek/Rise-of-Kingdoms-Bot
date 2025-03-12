import traceback
import random
import time

from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task

from tasks.constants import TaskName


class Alliance(Task):
    def __init__(self, bot):
        super().__init__(bot)

    territory_gifts_x = random.randint(860,920)
    technology_gifts_y = random.randint(530,588)

    def do(self, next_task=TaskName.MATERIALS):
        try:
            super().set_text(title='Alliance', remove=True)
            alliance_btn_pos = (random.randint(920,950), random.randint(650,690))
            super().set_text(insert='Open alliance')
            super().back_to_home_gui()
            super().menu_should_open(True)
            x, y = alliance_btn_pos
            super().tap(x, y, 3)
            tasks = [
                self.help_alliance,
                self.claim_gifts,
                self.claim_territory,
                self.donate_technology
            ]
            random.shuffle(tasks)
            for task in tasks:
                task()
                time.sleep(random.uniform(1.81, 2.79))
                self.back(1)
        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task

    def help_alliance(self):
        super().set_text(insert='Help Alliance')
        super().tap(random.randint(1000,1050), random.randint(380,430))  # enter the help page
        super().tap(random.randint(570,700), random.randint(635,670))   # tap the help button if present, otherwise it will tap on empty space

    def claim_gifts(self):
        super().set_text(insert='Claim gift')
        gifts_pos = (self.territory_gifts_x, self.technology_gifts_y)
        rare_pos = (random.randint(830,1020), random.randint(195,212))
        normal_pos = (random.randint(570,760), random.randint(195,212))
        claim_all_pos = (random.randint(1100,1120), random.randint(190,225))
        treasure = (random.randint(300,420), random.randint(360,460))
        x, y = gifts_pos
        super().tap(x, y, 2)
        time.sleep(random.uniform(0.7, 3.7))
        # collecting rate gifts
        super().set_text(insert='Claim rate gift')
        x, y = rare_pos
        super().tap(x, y, 1)
        time.sleep(random.uniform(0.7, 3.7))
        for i in range(20):
            _, _, pos = self.gui.check_any(ImagePathAndProps.GIFTS_CLAIM_BUTTON_IMAGE_PATH.value)
            if pos is None:
                break
            x, y = pos
            super().tap(x, y, random.uniform(0.8, 1.6))

        # collecting normal gifts
        super().set_text(insert='Claim normal gift')
        x, y = normal_pos
        super().tap(x, y, 1)
        time.sleep(random.uniform(0.7, 3.7))
        x, y = claim_all_pos
        super().tap(x, y, 1)
        time.sleep(random.uniform(0.7, 3.7))
        # collecting treasure of white crystal
        x, y = treasure
        super().tap(x, y, 1)
        time.sleep(random.uniform(0.7, 3.7))

    def claim_territory(self):
        super().set_text(insert='Claim resource')
        territory_pos = (self.territory_gifts_x, random.randint(380,430))
        claim_pos = (random.randint(970,1060), random.randint(130,147))
        x, y = territory_pos
        super().tap(x, y, 2)
        time.sleep(random.uniform(0.7, 3.7))
        x, y = claim_pos
        super().tap(x, y, 1)
        time.sleep(random.uniform(0.7, 3.7))
    
    def donate_technology(self):
        super().set_text(insert='Donate technology')
        technology_pos = (random.randint(730,780), self.technology_gifts_y)
        x, y = technology_pos
        super().tap(x, y, 5)
        time.sleep(random.uniform(0.7, 3.7))
        _, _, recommend_image_pos = self.gui.check_any(ImagePathAndProps.TECH_RECOMMEND_IMAGE_PATH.value)
        if recommend_image_pos is not None:
            x, y = recommend_image_pos
            super().tap(x, y + 60, 1)
            time.sleep(random.uniform(0.7, 3.7))
            _, _, donate_btn_pos = self.gui.check_any(
                ImagePathAndProps.TECH_DONATE_BUTTON_IMAGE_PATH.value)
            if donate_btn_pos is not None:
                x, y = donate_btn_pos
                for i in range(20):
                    super().tap(x, y, random.uniform(0.7, 1.1))
        else:
            super().set_text(insert="Cannot found Officer's Recommendation")
        self.back(1)