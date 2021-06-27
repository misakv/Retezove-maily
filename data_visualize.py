"""Module used for fake mails analysis from the database."""
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

COLNAMES = [
    "Date_time",
    "Subject",
    "Abstract",
    "Source",
    "Link",
    "Tag_list",
    "Mentioned_list",
    "Body",
    "Duplicate_date",
]

path = os.getcwd()
df = pd.read_csv(path + "\output.csv", names=COLNAMES, sep=";")

df["Date_time"].head()

df["Date_time"] = pd.to_datetime(df["Date_time"])

df["Date"] = df["Date_time"].dt.date
df["Time"] = df["Date_time"].dt.time


# Count per years, months, days
# add columns for week and year of the date
df["date_week"] = df["Date"].apply(lambda x: x.isocalendar()[1])
df["date_year"] = df["Date"].apply(lambda x: x.isocalendar()[0])


week_groups = df.groupby([df["date_year"], df["date_week"]])["Date_time"].count()

# Plot
week_groups.plot(kind="bar", figsize=(10, 5))


plt.xlabel("Týden v roce")
plt.ylabel("Počet zachycených nových fake news emailů")

red_patch1 = mpatches.Patch(
    color="red", label="(14, 2020) - Odstranění sochy Koněva Praha 6"
)
red_patch2 = mpatches.Patch(
    color="red", label="(18, 2020) - Pomník Vlasovců v Řeporyjích"
)
red_patch3 = mpatches.Patch(
    color="red", label="(23, 2020) - Ricinová kauza a vyhoštění agentů GRU"
)
red_patch4 = mpatches.Patch(
    color="red", label="(40, 2020) - Krajské volby a 1. kolo senátních voleb"
)
red_patch5 = mpatches.Patch(color="red", label="(44, 2020) - Volby USA")
red_patch6 = mpatches.Patch(color="red", label="(15, 2021) - Vrbětice")


plt.legend(
    handles=[red_patch1, red_patch2, red_patch3, red_patch4, red_patch5, red_patch6],
    loc="upper center",
)

plt.show()
