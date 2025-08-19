# Wander Wallet

“Wander Wallet” is a Python-based command-line application designed to help travelers track expenses and stay within budget while being on a trip. It is designed to give travelers a clear overview of their budget, tracked expenses and remaining funds while travelling. The application connects to Google Sheets to store and update trip information and expenses. As a user, I want to easily add new expenses, view my current financial status and stay on track with my travel budget.

The website was created for educational purposes only.

[Live page on Heroku](https://wander-wallet-c4d586c6e78d.herokuapp.com/)

![Wander Wallet Website Start Screen](docs/start-screen.png) TODO

![GitHub last commit](https://img.shields.io/github/last-commit/kathrinmzl/organizedLife?color=red)
![GitHub contributors](https://img.shields.io/github/contributors/kathrinmzl/organizedLife?color=orange)
![GitHub language count](https://img.shields.io/github/languages/count/kathrinmzl/organizedLife?color=yellow)
![GitHub top language](https://img.shields.io/github/languages/top/kathrinmzl/organizedLife?color=green)


- - -

## User Experience (UX)

### Site Goals

- Business Goals: Provide a simple and reliable tool for managing travel budgets directly from the command line

- Users’ needs: Easily track trip expenses, stay on top of budgets and quickly understand whether they are spending within their limits

- Primary user: Travelers who want a simple way to manage their trip finances

### User Stories

#### Must-have

1. As a user, I want to easily understand the main purpose of the app

2. As a user, I want to be able to create a new trip with a budget and dates

3. As a user, I want to see a clear summary of my trip, including budget, expenses and whether I am over, under or on budget

4. As a user, I want to add new expenses with a date and amount

5. As a user, I want to update an expense if I entered something incorrectly

6. As a user, I want my data to be saved so that I can continue tracking expenses until the end of my trip

#### Should-have

7. As a user, I want feedback after adding or updating an expense so I know it worked

8. As a user, I want the app to handle errors gracefully so it doesn’t crash unexpectedly

#### Could-have

9. As a user, I want to track multiple trips at once

10. As a user, I want to categorize expenses (e.g., food, transport, accommodation)

11. As a user, I want to see charts of my spending for better insights

### Features to achieve the goals

- The application will have a simple, clear command-line interface so users immediately understand its purpose

- Users will be able to create a new trip by entering a trip name, budget and start/end dates

- Users will be able to add new expenses for specified dates

- Users will be able to update/correct an existing expense for a specific date

- Users will be able to view a clear summary of their trip, showing total budget, spent amount, remaining funds and whether they are over, under, or on budget

- Users will be able to see a list of expenses

- The application will provide immediate feedback after adding or updating an expense to confirm the action succeeded

- Trip and expense data will be stored in Google Sheets to ensure persistence and accessibility across devices

- The app will handle errors gracefully to prevent crashes (e.g., invalid input)

- Users will be able to track multiple trips independently (could-have)

- Expenses can be categorized for better tracking and reporting (could-have)

- Users will be able to view charts or visual summaries of spending by category or over time (could-have)

- - -

## Design

### Flowchart

The following flowchart was created using [Lucidchart](https://lucid.app/) before starting to code, to visualize the intended general workflow of the application. During the development process, the workflow was adapted in certain areas to better fit technical requirements and improve user experience. While the flowchart represents the initial plan, some steps were modified or added in the final implementation.

![Wander Wallet Initial Flowchart](docs/wander_wallet_flowchart.png)

### Color Scheme/Imagery/Typography
Although the application has a simple terminal-based interface with limited UI design, the following style choices were made to make user inputs, feedback, and overall interaction clear and easy to follow.

Bold text is used to highlight anything directly concerning the user, such as their inputs or headings in summaries. Green text is used to signal valid user inputs, while red text indicates errors, invalid inputs or warnings.

Emojis are used to indicate status messages and user inputs, helping to make the interface more engaging and easier to follow.

