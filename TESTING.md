# Testing

> NOTE: Return back to the [README.md](README.md) file.

## Code Validation

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

Initially I had lines of code exceeding the recommended 79 characters, which I then restructured. Also there where some unnecessary whitespaces that I removed.

The final results are as follows:

| File | URL | Screenshot | Notes |
| --- | --- | --- | --- |
| [run.py](https://github.com/kathrinmzl/WanderWallet/blob/main/run.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/kathrinmzl/WanderWallet/main/run.py) | ![screenshot](docs/testing/code-validation/validation-run-py.png) | No errors found |
| [sheet_manager.py](https://github.com/kathrinmzl/WanderWallet/blob/main/sheet_manager.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/kathrinmzl/WanderWallet/main/sheet_manager.py) | ![screenshot](docs/testing/code-validation/validation-sheet-manager-py.png) | No errors found |
| [trip.py](https://github.com/kathrinmzl/WanderWallet/blob/main/trip.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/kathrinmzl/WanderWallet/main/trip.py) | ![screenshot](docs/testing/code-validation/validation-trip-py.png) | No errors found |
| [validation.py](https://github.com/kathrinmzl/WanderWallet/blob/main/validation.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/kathrinmzl/WanderWallet/main/validation.py) | ![screenshot](docs/testing/code-validation/validation-validation-py.png) | No errors found |

## Defensive Programming

Defensive programming was manually tested with the below user acceptance testing:

| Feature | Expectation | Test | Result | Screenshot |
| --- | --- | --- | --- | --- |
| Check if trip already exists |  Upon launching the application, inform the user whether they have already set up a trip. | Open application with an empty database | User is informed that no trip has been found | ![screenshot](docs/features/start-screen-no-trip.png) |
| |  | Open application with an exisiting database | User is informed that a trip has been found and is shown a summary of their current trip| ![screenshot](docs/features/start-screen-existing-trip.png) |
| Set up a new trip |  The user can only provide a valid trip name | Input an empty trip name | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-name-empty.png) |
| | | Input a trip name that is not only letters (A–Z), numbers (0–9) and spaces | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-name-symbol.png) |
| | | Input a trip name that is not 1-30 characters | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-name-long.png) |
| | | Input a valid trip name | Valid data message is shown | ![screenshot](docs/features/new-trip-name-input.png) |
| |  The user can only provide valid trip dates | Input empty trip dates | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-dates-empty.png) |
| | | Input trip dates that does not have the format YYYY-MM-DD| Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-dates-format.png) |
| | | Input a trip end date that is not in the future | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-dates-not-future.png) |
| | | Input a trip end date that before the start date | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-dates-order.png) |
| | | Input trip dates not seperated by a comma | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-dates-comma.png) |
| | | Input valid trip dates | Valid data message is shown | ![screenshot](docs/features/new-trip-date-input.png) |
| |  The user can only provide a valid trip budget | Input empty trip budget | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-budget-empty.png) |
| | | Input negative trip budget | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-budget-negative.png) |
| | | Input symbols that aren't whole numbers | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/new-trip-budget-no-int.png) |
| | | Input a valid trip budget | Valid data message is shown | ![screenshot](docs/features/new-trip-budget-input.png) |
| Yes/No question inputs |  The user can only provide a valid input | Input an empty string | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/yes-no-empty.png) |
| | | Input anything but "yes" or "no" | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/yes-no-not-yes-no.png) |
| | | Input "yes" or "no" in capital or small letters |  Valid data message is shown | ![screenshot](docs/testing/manual-testing/yes-no-valid.png) |
| Show a trip summary |  All values are correctly calculated from the trip info and expenses user input | Verify the trip summary values after setting up a new trip | All values are calculated correctly| ![screenshot](docs/features/new-trip-summary.png) |
| | | Verify the trip summary values after adding expenses | All values are calculated correctly| ![screenshot](docs/testing/manual-testing/summary-after-expenses.png) |
| | | Verify the trip summary values when opening the app with an existing trip | All values are calculated correctly| ![screenshot](docs/testing/manual-testing/summary-beginning.png) |
| Show expenses list |  All values are correctly displayed and chronologically ordered | Verify the expense list when opening the app with an existing trip| All values are shown correctly| ![screenshot](docs/features/existing-trip-expenses-summary.png) |
| | | Verify the expense list after adding expenses | All values are shown correctly| ![screenshot](docs/testing/manual-testing/expense-list-after-expenses.png) |
| Continue trip |  Delete trip data if user does not want to continue working with the current trip | Input "no"| The user can set up a new trip| ![screenshot](docs/features/existing-trip-continue-input-no.png) |
| | Continue to add expenses if user wants to continue working with the trip | Input "yes"| The user is able to add expenses| ![screenshot](docs/features/existing-trip-continue-input-yes.png) |
| Add expense |  The user can only provide a valid expense date | Input an empty trip date| Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/add-expense-empty.png) |
| | | Input a date that does not have the format YYYY-MM-DD| Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/add-expense-period.png) |
| | | Input a date that is not within the travel period | Error message is shown and user can make a new input| ![screenshot](docs/features/add-expense-date-error.png) |
| | | Input a date that is a future date | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/add-expense-future.png) |
| | | Input a valid date | Valid data message is shown | ![screenshot](docs/features/add-expense-date.png) |
| |  The user can only provide a valid expense amount| Input an empty amount| Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/add-expense-amount-empty.png) |
| | | Input a negative amount | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/add-expense-amount-negative.png) |
| | | Input symbols that aren't whole numbers | Error message is shown and user can make a new input| ![screenshot](docs/testing/manual-testing/add-expense-amount-not-int.png) |
| | | Input a valid amount | Valid data message is shown | ![screenshot](docs/features/add-expense-amount.png) |
| Add another expense |  If the user chooses "yes", the process of entering a new expense begins again | Input "yes"| The user can add another expense | ![screenshot](docs/features/add-expense-another-one-yes.png) |
| | If the user chooses "no", the app proceeds| Input "no"| The app proceeds to the next step| ![screenshot](docs/features/add-expense-another-one-no.png) |
| Update an expense |  If the user enters an already exisiting expense date, they are prompted to decide whether to update it or not | Input "yes"| The expense gets updated | ![screenshot](docs/features/add-expense-update-yes.png) |
| | | Input "no"| The expense does not get updated | ![screenshot](docs/features/add-expense-update-no.png) |
| End of program |  When the user decides not to add any more expenses, they are given the opportunity to show a list of expenses and the trip summary | Don't add another expense| The program gives the option to show the expense list and then ends the program with the final trip summary | ![screenshot](docs/features/end-of-programm-expense-list.png) ![screenshot](docs/features/end-of-programm.png) |

## User Story Testing

| Target | Expectation | Outcome | Screenshot |
| --- | --- | --- | --- |
| As a user | I want to easily understand the main purpose of the app | so I know right away how it helps me. | ![screenshot](docs/testing/user-stories/user-story-1.png) |
| As a user | I want to be able to create a new trip with a budget and dates | so I can set the financial framework for my travels. | ![screenshot](docs/testing/user-stories/user-story-2.png) |
| As a user | I want to see a clear summary of my trip, including budget, expenses and whether I am over, under or on budget | so I always know my financial status. | ![screenshot](docs/testing/user-stories/user-story-3.png) |
| As a user | I want to add new expenses with a date and amount | so I can keep an accurate record of my spending. | ![screenshot](docs/testing/user-stories/user-story-4.png) |
| As a user | I want to update an expense if I entered something incorrectly | so my data stays accurate. | ![screenshot](docs/testing/user-stories/user-story-5.png) |
| As a user | I want my data to be saved so that I can continue tracking expenses until the end of my trip | so I don’t lose progress during the journey.| ![screenshot](docs/testing/user-stories/user-story-6.png) |
| As a user | I want feedback after adding or updating an expense| so I know my action was successful. | ![screenshot](docs/testing/user-stories/user-story-7.png) |
| As a user |  I want the app to handle errors gracefully so it doesn’t crash unexpectedly | so I can keep using it without interruptions. | ![screenshot](docs/testing/user-stories/user-story-8.png) |

## Bugs

All bug fixing activities were documented in the Git commit history using the keyword `fix: ...` for clarity and traceability. 

To this date, no known unfixed errors remain in the application, though, even after thorough testing, I cannot rule out the possibility.

### Known Issues

| Issue | Screenshot |
| --- | --- |
| If a user types `CTRL`+`C` in the terminal on the live site, they can manually stop the application and receive an error. | ![screenshot](docs/testing/known-issues/ctrl-c-issue.png) |


