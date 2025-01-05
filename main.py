import core
import pandas as pd
def make_grid(step, filename, folder):

    grd_df = core.get_grid_df(step=step)

    print(grd_df.head().to_string())

    grd_df.to_csv(f"{folder}/{filename}.csv", sep=";", index=False)

if __name__ == "__main__":

    steps_d = {
        "0p25": 0.25,
        "0p50": 0.5,
        "1p00": 1.0,
        "2p00": 2.0,
        "3p00": 3.0,

    }
    for step_s in steps_d:
        res = str(steps_d[step_s]).replace(".", "p")
        fnm = f"sasg_{step_s}-v0_{res}-d_sa_2025"
        make_grid(step=steps_d[step_s], filename=fnm, folder="C:/data")
