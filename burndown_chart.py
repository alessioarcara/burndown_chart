from github import Github
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) < 7:
    print("Errore: devi passare come argomenti da riga di comando:")
    print("- GitHub token -> esempio: validToken")
    print("- GitHub user -> esempio: validUser")
    print("- GitHub repository -> esempio: validRepository")
    print("- Numero della iterazione dello sprint -> esempio: 1,2,3, ...")
    print("- Numero dei giorni -> esempio: 6,7,8, ...")
    print("- Mostra grafico per giorni successivi ad oggi -> esempio: Mostra\n")
    print("Esempio utilizzo:")
    print("> python burndownchart.py validToken validUser valid 3 7 Mostra")
    sys.exit()


def check_positive_int(param):
    try:
        param = int(param)
    except ValueError:
        print("Errore: il parametro deve essere un numero intero.")
        sys.exit()

    if param < 0:
        print("Errore: il parametro deve essere un numero positivo.")
        sys.exit()
    return param


TOKEN = sys.argv[1]
OWNER = sys.argv[2]
REPOSITORY = sys.argv[3]
SPRINT = check_positive_int(sys.argv[4])
DAYS = check_positive_int(sys.argv[5])
MOSTRA = sys.argv[6] == "Mostra"


def get_actual(issues):
    # init
    actual = np.full(DAYS, issues.totalCount, dtype=float)
    bins = np.zeros(DAYS)
    closed_issues = [issue for issue in issues if issue.closed_at is not None]
    closed_issues.sort(key=lambda x: x.closed_at, reverse=False)

    for closed_issue in closed_issues:
        day = closed_issue.closed_at.isoweekday()
        actual[day] -= 1
        actual[day + 1:] = actual[day]
        bins[day] += 1

    if not MOSTRA:
        actual[date.today().isoweekday():] = actual[date.today().isoweekday():] + np.NAN
    return actual, bins


g = Github(TOKEN)
repo = g.get_repo(f"{OWNER}/{REPOSITORY}")
issues = repo.get_issues(state='all', labels=['task', f"s0{SPRINT}"])

fig, ax = plt.subplots()

x = np.arange(DAYS)
actual, bins = get_actual(issues)
ideal = [x - i * (issues.totalCount / (DAYS - 1))
         for i, x in enumerate(np.full(DAYS, issues.totalCount))]
ax.plot(x, ideal, linestyle='dashed', color='green', label="Ideal")
ax.step(x, actual, where='post', label="Actual")
ax.bar(x, bins, width=0.2, color='orange', label="Completed tasks")

ax.set_title(f"Burn down chart for Sprint {SPRINT}")
ax.set_ylabel("Remaining and completed tasks")
ax.legend(loc="upper right")

plt.xticks(x, [f"Day\n{ix}" for ix in x])
plt.savefig("burndownchart.png")
plt.show()
