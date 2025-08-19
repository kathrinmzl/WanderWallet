from datetime import datetime
from colorama import Style, init

# Initialize Colorama (colors reset automatically after each print)
init(autoreset=True)


class Trip:
    """
    Trip class
    """
    def __init__(self, trip_info: dict, expenses: dict):
        self.trip_info = trip_info
        self.expenses = expenses
        # Get trip info input fields (for calculations)
        self.trip_name = trip_info["trip_name"]
        self.start_date = datetime.strptime(
            trip_info["start_date"], "%Y-%m-%d"
            ).date()
        self.end_date = datetime.strptime(
            trip_info["end_date"], "%Y-%m-%d"
            ).date()
        self.total_budget = int(trip_info["total_budget"])

    # Calculate different properties for trip info 
    @property
    def duration(self):
        """
        Calculate duration
        """
        # Add 1 to include the first and last days both
        return (self.end_date-self.start_date).days + 1
    
    @property
    def daily_budget(self):
        """
        Calculate daily budget
        """
        return round(self.total_budget/self.duration)
    
    @property
    def total_spent(self):
        """
        Calculate total expenses
        """
        # If there are no expenses or max. 1 expense tracked, the 
        # "amount" is a single value instead of a list
        if not isinstance(self.expenses["amount"], list):
            if self.expenses["amount"] == "":
                return 0
            else:
                return int(self.expenses["amount"])
        else:
            return sum(int(num) for num in self.expenses["amount"])
    
    @property
    def remaining_budget(self):
        """
        Calculate remaining budget
        """
        return self.total_budget - self.total_spent
    
    @property
    def days_left(self):
        """
        Calculate remaining days
        """
        today = datetime.now().date()
        if today > self.start_date and today < self.end_date:
            days_left_val = (self.end_date - today).days
        elif today > self.end_date:
            # Trip is over
            days_left_val = 0
        else:
            # Trip hasn't started yet
            days_left_val = self.duration
        return days_left_val
    
    @property
    def avg_daily_spent(self):
        """
        Calculate avg daily expenses
        """
        days_spent = self.duration - self.days_left
        # If trip hasn't started yet days_spent is 0
        if days_spent == 0:
            return 0

        return round(self.total_spent/days_spent)
    
    @property
    def budget_status(self):
        """
        Calculate budget status
        """
        if self.avg_daily_spent > self.daily_budget:
            budget_status = "over"
        elif self.avg_daily_spent < self.daily_budget:
            budget_status = "under"
        else:
            budget_status = "on"
        
        return budget_status
    
    def update_trip_info(self):
        """
        Updates the trip_info dict with current calculated values
        """
        self.trip_info["duration"] = self.duration
        self.trip_info["days_left"] = self.days_left
        self.trip_info["total_spent"] = self.total_spent
        self.trip_info["remaining_budget"] = self.remaining_budget
        self.trip_info["daily_budget"] = self.daily_budget
        self.trip_info["avg_daily_spent"] = self.avg_daily_spent
        self.trip_info["budget_status"] = self.budget_status

        return self.trip_info
    
    def summary(self):
        """
        Return a summary of the current trip data
        """
        # Adjust how budget status is display in summary
        if self.budget_status == "over":
            status_msg = "Over budget — try to slow down spending!"
        elif self.budget_status == "under":
            status_msg = "Under budget — great job managing your expenses!"
        else: 
            status_msg = "On track — keep spending balanced."

        print(
            Style.BRIGHT + 
            "Here is a summary of your current trip information:\n"
            )
        return (
            f"{'Trip Name:':20} {self.trip_name}\n"
            f"{'Dates:':20} {self.start_date} - {self.end_date} "
            f"({self.duration} days)\n"
            f"{'Days Left:':20} {self.days_left} days\n"

            f"{'Total Budget:':20} {self.total_budget} €\n"
            f"{'Total Expenses:':20} {self.total_spent} €\n"
            f"{'Remaining Budget:':20} {self.remaining_budget} €\n"

            f"{'Daily Budget:':20} {self.daily_budget} €\n"
            f"{'Avg. Daily Expenses:':20} {self.avg_daily_spent} €\n"
            f"{'Budget Status:':20} {status_msg}\n"
            f"\n(All € values rounded to the nearest possible integer)\n"
            )