import tqdm
import onetouchlite as otl


@otl.timer
def circulate_tqdm():
    for i in tqdm.tqdm(range(10_000_000)):
        pass


@otl.timer
def circulate_otl():
    for i in otl.pace(range(10_000_000)):
        pass


circulate_tqdm()
circulate_otl()


