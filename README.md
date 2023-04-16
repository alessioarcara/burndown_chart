# Burn Down Chart Generator

This script generates a burn down chart for a specific GitHub repository and sprint. It visualizes the progress of tasks and their completion over time. The chart is saved as an image file, which can be easily shared or embedded in other documents.

## Requirements

### GitHub issues must be labeled correctly:

In order for the script to generate a burn down chart, the issues in the GitHub repository must be labeled correctly. Each issue must have the following labels:

- A `task` label to indicate that it is a task that needs to be completed
- A label with the sprint number, in the format `s0{number}`, where `{number}` is the sprint iteration number (e.g., `s01` for the first sprint)

Make sure that all issues are labeled correctly before running the script, otherwise the chart may not be generated correctly.

### Dependencies:

- Python 3.6 or higher
- `matplotlib` library
- `numpy` library
- `PyGithub` library

To install the required libraries, run:

```bash
pip install matplotlib numpy PyGithub
```

## Usage

To run the script, execute the following command:

```bash
python burndownchart.py <token> <user> <repository> <sprint> <days> <show>
```

Replace `<token>`, `<user>`, `<repository>`, `<sprint>`, `<days>`, and `<show>` with appropriate values:

* `<token>`: Your GitHub personal access token.
* `<user>`: The GitHub username of the repository owner.
* `<repository>`: The name of the GitHub repository.
* `<sprint>`: The sprint iteration number (e.g., 1, 2, 3, etc.).
* `<days>`: The number of days in the sprint (e.g., 7 for a week-long sprint).
* `<show>`: Set this to "Show" to display the chart for the days after today; otherwise, leave it empty.

## Example

```bash
python burndown_chart.py my_token alessioarcara project_sweng 5 8 Show
```
This command will generate the following burn down chart for the 5th sprint of the specified repository, considering a 7-day sprint.

![esempio](https://user-images.githubusercontent.com/1864054/232249801-629b009b-63fa-4b9d-aedb-3d4c41c9968d.png)

## Customization

The script can be easily modified to generate burn down charts for different metrics and time units, such as story points or sprints.

![esempio2](https://user-images.githubusercontent.com/1864054/232249819-6a1fd1cd-0b12-4bd6-b934-6552a4fd66d2.png)

## Contributing

* If you encounter any bugs or have ideas for new features, feel free to open an issue in the repository's issue tracker.
* To contribute code changes, fork the repository and create a pull request with your changes.
