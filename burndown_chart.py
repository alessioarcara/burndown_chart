import sys
import numpy as np
import matplotlib.pyplot as plt
from github import Github, GithubException
from datetime import date


def print_usage_and_exit():
    print("Uso:")
    print("python burndownchart.py <token> <user> <repository> <sprint> <days> <show>\n")
    print("Parametri:")
    print("<token> - Il tuo token di accesso personale GitHub.")
    print("<user> - Il nome utente del proprietario del repository.")
    print("<repository> - Il nome del repository.")
    print("<sprint> - Il numero dello sprint (un numero intero positivo).")
    print("<days> - Il numero di giorni per lo sprint (un numero intero positivo).")
    print("<show> - 'Show' per mostrare i giorni successivi ad oggi nel grafico.")
    print("\nEsempio:")
    print("> python burndownchart.py validToken validUser validRepository 3 7 Show")
    sys.exit()


def check_positive_integer(param):
    try:
        value = int(param)
        if value < 0:
            raise ValueError
    except ValueError:
        print(f"Errore: {param} deve essere un numero intero positivo.")
        sys.exit()
    return value


def calculate_actual_and_bins(issues, days, show):
    actual = np.full(days, issues.totalCount, dtype=float)
    bins = np.zeros(days)
    closed_issues = [issue for issue in issues if issue.closed_at is not None]
    closed_issues.sort(key=lambda x: x.closed_at, reverse=False)

    for closed_issue in closed_issues:
        day = closed_issue.closed_at.isoweekday()
        actual[day:] -= 1
        bins[day] += 1

    if not show:
        actual[date.today().isoweekday():] = np.NAN
    return actual, bins


def parse_arguments():
    if len(sys.argv) < 7:
        print_usage_and_exit()

    args = {
        "token": sys.argv[1],
        "owner": sys.argv[2],
        "repository": sys.argv[3],
        "sprint": check_positive_integer(sys.argv[4]),
        "days": check_positive_integer(sys.argv[5]),
        "show": sys.argv[6] == "Show",
    }

    return args


def create_burndown_chart(days, sprint, actual, ideal, bins):
    fig, ax = plt.subplots()
    x = np.arange(days)

    ax.plot(x, ideal, linestyle="dashed", color="green", label="Ideal")
    ax.step(x, actual, where="post", label="Actual")
    ax.bar(x, bins, width=0.2, color="orange", label="Completed tasks")

    ax.set_title(f"Burn down chart for Sprint {sprint}")
    ax.set_ylabel("Remaining and completed tasks")
    ax.legend(loc="upper right")

    plt.xticks(x, [f"Day\n{ix}" for ix in x])
    plt.savefig("burndownchart.png")
    plt.show()


def main():
    args = parse_arguments()

    try:
        github_api = Github(args["token"])
        repo = github_api.get_repo(f"{args['owner']}/{args['repository']}")
    except GithubException as e:
        print(f"Errore: {e.data.get('message'), 'Token non valido o problema di accesso al repository.'}")
        sys.exit()

    issues = repo.get_issues(state='all', labels=['task', f"s0{args['sprint']}"])
    actual, bins = calculate_actual_and_bins(issues, args['days'], args['show'])
    ideal = np.linspace(issues.totalCount, 0, args['days'])

    create_burndown_chart(args['days'], args['sprint'], actual, ideal, bins)


if __name__ == "__main__":
    main()
