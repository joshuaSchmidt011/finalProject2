from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from processing import *
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    """
    This is the main application window for my workout planner application.
    Sets the UI and managed connections between pages from button signals
    """
    def __init__(self):
        """
        Runs the initialization for the app, establishes som variables and widget throughout the different pages
        """

        super().__init__()
        self.goal_graph_layout = QVBoxLayout()
        self.setWindowTitle("Workout planner")
        self.setFixedSize(1400, 1000)

        self.active_user = 'test'
        self.goal_selected = 'test'

        # Top Bar
        self._createMenuBar()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Build the widgets for different pages
        self.login_page = QWidget()
        self.home_page = QWidget()
        self.new_user_page = QWidget()
        self.goal_page = QWidget()

        # Place widget into stacked widget to function allowing movement between pages
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.new_user_page)
        self.stacked_widget.addWidget(self.goal_page)

        # loads the pages
        self._login_screen()
        self._home_screen()
        self._new_user_screen()
        self._goal_screen()

    def _createMenuBar(self):
        """
        Creates a menu bar with file, edit, and help #Note No use for those functions yet
        """
        menuBar = self.menuBar()
        #
        fileMenu = QMenu('&File', self)
        menuBar.addMenu(fileMenu)
        #
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu(("&Help"))

    def _login_screen(self):
        """
        Sets up the login screen, this screen has fields for username, passwords, and provides link to create account
        """

        # Build login layout and set alignment
        layout = QVBoxLayout(self.login_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_login = QLabel('Login')
        label_login.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # build username and password entries and labels
        label_username = QLabel('Username')
        self.entry_username = QLineEdit()
        self.entry_username.setFixedWidth(200)

        label_password = QLabel('Password')
        self.entry_password = QLineEdit()
        self.entry_password.setFixedWidth(200)

        # Build login button that runs the login function
        login_button = QPushButton("Login")
        login_button.setFixedWidth(100)
        login_button.clicked.connect(self.login)

        # Builds the new user button that sends user to make an account
        new_user_button = QPushButton("Create an account")
        new_user_button.setFixedWidth(150)
        new_user_button.setStyleSheet("QPushButton { border: none; color: blue;}")
        new_user_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        # Add label to display if errors occurred while creating an account.
        self.label_error = QLabel('')

        # Adjusting fonts and colors
        font = label_login.font()
        font.setBold(True)
        font.setPointSize(20)
        label_login.setFont(font)
        label_login.setStyleSheet("background-color: tan;")

        # Adding all items to the layout for display
        layout.addStretch()
        layout.addWidget(label_login)
        layout.addWidget(label_username)
        layout.addWidget(self.entry_username)
        layout.addWidget(label_password)
        layout.addWidget(self.entry_password)
        layout.addWidget(login_button)
        layout.addWidget(new_user_button)
        layout.addWidget(self.label_error)
        layout.addStretch()

    def _home_screen(self):
        """
        Sets up the home screen layout, containing a navigation bar, workout recommendations and weight tracker
        :return:
        """
        # Establish an overarching layout
        outerLayout = QVBoxLayout(self.home_page)
        # Nav Bar ----------------------------------------------------------------------
        navLayout = QHBoxLayout()

        # Home button
        home_button = QPushButton("Home")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        home_button.setFixedWidth(75)
        home_button.setStyleSheet('border: none; background-color: gray;')

        spacer1 = QLabel('|')
        # Goals button
        goal_button = QPushButton("Goals")
        goal_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        goal_button.setFixedWidth(75)
        goal_button.setStyleSheet('border: none; background-color: gray;')

        print(self.active_user, 'in homescreen')
        # Welcome Label for user
        self.label_welcome = QLabel()

        # Log out button
        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        logout_button.setFixedWidth(75)

        # Placing all navigation functions into the layout
        navLayout.addWidget(home_button)
        navLayout.addWidget(spacer1)
        navLayout.addWidget(goal_button)
        navLayout.addStretch()
        navLayout.addWidget(self.label_welcome)
        navLayout.addStretch()
        navLayout.addWidget(logout_button)

        # Workout Recommendations ----------------------------------------------------------
        gen_workout_button = QPushButton('Generate Workout')
        gen_workout_button.clicked.connect(self.gen_workout)

        self.workout_layout = QVBoxLayout()
        self.workout_rows = QFormLayout()

        # Weight in tracker --------------------------------------------------------------------
        self.weigh_in_full_layout = QVBoxLayout()
        weigh_in_layout = QHBoxLayout()
        self.weigh_entry = QLineEdit()
        gen_weight_button = QPushButton('Submit')
        gen_weight_button.clicked.connect(self.gen_weigh_in)

        weigh_in_layout.addWidget(self.weigh_entry)
        weigh_in_layout.addWidget(gen_weight_button)
        self.weigh_in_full_layout.addLayout(weigh_in_layout)

        # Main screen setting all layouts in place and in order
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(gen_workout_button)
        mainLayout.addLayout(self.workout_layout)
        mainLayout.addLayout(self.weigh_in_full_layout)

        mainLayout.addStretch()

        # Setup
        outerLayout.addLayout(navLayout)
        outerLayout.addLayout(mainLayout)
        self.setLayout(outerLayout)

    def _new_user_screen(self):
        """
        Screen used to build a new account for new users. Input username, password and adds them to file
        :return:
        """
        # sets outer layout
        layout = QVBoxLayout(self.new_user_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Builds elements to be populated in the layout
        label_head = QLabel('Create an account')
        label_head.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_username = QLabel('New Username')
        self.entry_new_username = QLineEdit()
        self.entry_new_username.setFixedWidth(200)

        label_password = QLabel('New Password')
        self.entry_new_password = QLineEdit()
        self.entry_new_password.setFixedWidth(200)

        # Links to create account function
        account_button = QPushButton("Create Account")
        account_button.setFixedWidth(100)
        account_button.clicked.connect(self.create_account)

        self.label_error_new = QLabel('')

        # Adjusting font and sizing
        font = label_head.font()
        font.setBold(True)
        font.setPointSize(16)
        label_head.setFont(font)
        label_head.setStyleSheet("background-color: lightgreen;")

        # Placing all items in the layout
        layout.addStretch()
        layout.addWidget(label_head)
        layout.addWidget(label_username)
        layout.addWidget(self.entry_new_username)
        layout.addWidget(label_password)
        layout.addWidget(self.entry_new_password)
        layout.addWidget(account_button)
        layout.addWidget(self.label_error_new)
        layout.addStretch()

    def _goal_screen(self):
        """
        Sets up a goal selector screen where users pick their workout and see a generated graph of their progress
        overtime.
        :return:
        """
        # Sets up outer layout
        outerLayout = QVBoxLayout(self.goal_page)

        # Nav Bar - Build the box that holds the whole top nav bar
        navLayout = QHBoxLayout()

        # Home button
        home_button = QPushButton("Home")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        home_button.setFixedWidth(75)
        home_button.setStyleSheet('border: none; background-color: gray;')

        spacer1 = QLabel('|')
        # Goals button
        goal_button = QPushButton("Goals")
        goal_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        goal_button.setFixedWidth(75)
        goal_button.setStyleSheet('border: none; background-color: gray;')

        # Log out button
        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        logout_button.setFixedWidth(75)

        # Puts all the elements in the nav layout
        navLayout.addWidget(home_button)
        navLayout.addWidget(spacer1)
        navLayout.addWidget(goal_button)
        navLayout.addStretch()
        navLayout.addWidget(logout_button)

        # Goals working stuff, Build box for the goal button and graphs to go in
        self.goals_layout = QVBoxLayout()
        goals_label = QLabel('Pick the workout you want to look at!')
        # Builds combo box
        self.goals_combo = QComboBox(self)
        # Pulls all workouts from file
        workout_list = pull_workouts()
        print(workout_list)
        # Adds all workouts to the combobox and connects them to the on selection changed function
        self.goals_combo.addItems(workout_list)
        self.goals_combo.currentTextChanged.connect(self.on_selection_changed)

        self.goal_graph_label = QLabel('')

        self.goals_layout.addWidget(goals_label)
        self.goals_layout.addWidget(self.goals_combo)
        self.goals_layout.addWidget(self.goal_graph_label)


        # Main screen
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(navLayout)
        mainLayout.addLayout(self.goals_layout)
        mainLayout.addStretch()

        # Setup
        outerLayout.addLayout(navLayout)
        outerLayout.addLayout(mainLayout)
        self.setLayout(outerLayout)

    def login(self):
        """
        Handles the user login by validating them, then sends user to the home-screen.
        If it fails user will be prompted with what when wrong
        :return:
        """
        username = self.entry_username.text()
        password = self.entry_password.text()
        # lambda: self.stacked_widget.setCurrentIndex(1)
        login_check = run_login(username, password)

        if login_check[0]:
            self.stacked_widget.setCurrentIndex(1)
            self.active_user = username
            print(self.active_user)
            self.label_welcome.setText(f'Welcome {self.active_user}')
            self.entry_username.setText('')
            self.entry_password.setText('')
            self.label_error.setText('')
        else:
            if login_check[1] == 0:
                self.label_error.setText('Please put in your username.')
            elif login_check[1] == 1:
                self.label_error.setText('Please put in your password')
            elif login_check[1] == 2:
                self.label_error.setText('There is no user by that Username, Please make an account, or try another '
                                         'username.')
            elif login_check[1] == 3:
                self.label_error.setText('Your username and password do not match')

    def create_account(self):
        """
        Handles the creation of the new users account, will check to see if that user already exists

        Will prompt user with what went wrong if something falls
        :return:
        """
        username = self.entry_new_username.text()
        print(username)
        password = self.entry_new_password.text()
        print(password)

        account_check = run_account_create(username, password)
        if account_check[0]:
            self.stacked_widget.setCurrentIndex(0)
        else:
            if account_check[1] == 0:
                self.label_error_new.setText('Please put in your username.')
            elif account_check[1] == 1:
                self.label_error_new.setText('Please put in your password')
            else:
                self.label_error_new.setText('That username is taken, please pick another.')

    def gen_workout(self):
        '''
        Generates a workout plan based on the day of the weak

        also auto clears old information every click
        :return:
        '''
        try:
            # Clear previous layout items before generating news layout, important else app crashes
            self.workout_layout.removeItem(self.workout_rows)
            self.workout_rows.deleteLater()
            self.workout_layout.removeItem(self.add_workout_label)
            self.workout_layout.removeItem(self.add_workout_entry)
            self.workout_layout.removeItem(self.add_workout_button)

        except:
            print('Error clearing previous widgets')
            pass

        for i in reversed(range(self.workout_rows.count())):
            self.workout_rows.itemAt(i).widget().deleteLater()

        for i in reversed(range(self.workout_layout.count())):
            self.workout_layout.itemAt(i).widget().deleteLater()

        # Get today's weekday to find what workouts you are doing.
        today = datetime.date.today()
        str_weekday = today.strftime("%A")

        # Generating new widgets
        self.workout_rows = QFormLayout()

        workout_list = pick_workout(str_weekday, self.active_user)

        # the dictionary made below allows us to take the inputs from the generated line edits.
        self.line_edits = {}
        for workout in workout_list:
            line_edit = QLineEdit()
            self.workout_rows.addRow(f'{workout}', line_edit)
            self.line_edits[workout] = line_edit

            attributes = get_attributes(workout)
            self.workout_rows.addRow(
                QLabel(f"Please add the follow information separating each by a comma in order: {attributes}"))

        # Sets up for the add workout function
        self.add_workout_label = QLabel('Please type in Workout you want to add')
        self.add_workout_entry = QLineEdit()
        self.add_workout_button = QPushButton('Add Workout')
        self.add_workout_button.clicked.connect(self.add_workout)
        self.a_w_r = QLabel('')
        self.workout_submit_button = QPushButton('Submit')
        self.workout_submit_button.clicked.connect(self.workout_submit)
        self.submit_info = QLabel('')

        # adds elements to the layouts
        self.workout_layout.addLayout(self.workout_rows)

        self.workout_layout.addWidget(self.add_workout_label)
        self.workout_layout.addWidget(self.add_workout_entry)
        self.workout_layout.addWidget(self.add_workout_button)
        self.workout_layout.addWidget(self.a_w_r)
        self.workout_layout.addWidget(self.workout_submit_button)
        self.workout_layout.addWidget(self.submit_info)

    def add_workout(self):
        """
        Adds a new workout to the workout lists and validates input
        :return:
        """
        workout = self.add_workout_entry.text()
        check = check_workout(workout)
        if check:
            line_edit = QLineEdit()
            self.workout_rows.addRow(f'{workout}', line_edit)
            self.line_edits[workout] = line_edit
            attributes = get_attributes(workout)
            self.workout_rows.addRow(
                QLabel(f"Please add the follow information separating each by a comma in order: {attributes}"))
            self.a_w_r.setText('')
        else:
            self.a_w_r.setText('Please input one of the available exercises')

    def workout_submit(self):
        """
        Submits the workout data and runs data validation

        if the data passes the data validation it is saved to file else the user is prompted.
        :return:
        """
        print('submit')
        for workout, value in self.line_edits.items():
            temp_dict = {}
            temp_dict[workout] = value.text()
            print('temp_dict', temp_dict)
            check = check_edits(temp_dict, self.active_user)
            print(check)
            if check[0] == True:
                print('check good')
                self.submit_info.setText('Data has saved')
            else:
                print('check bad')
                if check[1] == 1:
                    self.submit_info.setText('You have added to many or to few variables, please match template exactly')
                elif check[1] == 2:
                    self.submit_info.setText('One of your dates is not in a valid format, please match something like '
                                             '12/12/2024')
                elif check[1] == 3:
                    self.submit_info.setText('You inputted a non-number for weight')
                elif check[1] == 4:
                    self.submit_info.setText('You inputted a non-number for reps')
                elif check[1] == 5:
                    self.submit_info.setText('You inputted a non-number for sets')

    def gen_weigh_in(self):
        """
        Logs the user's weight and generates a graph of user's weight progression

        Uses matPlotLib
        :return:
        """
        try:
            # Try top remove old graph if any.
            self.weigh_in_full_layout.removeItem(self.graph_layout)
            self.graph_layout.deleteLater()
        except:
            print('Could not remove graph')

        # Input weight value into file
        new_weight = self.weigh_entry.text()
        self.weigh_entry.setText('')
        now = datetime.datetime.now()
        date = now.strftime("%m/%d/%Y")
        log_weight(new_weight, date, self.active_user)

        # Generates graph
        self.graph_layout = QVBoxLayout()

        # Building matPlotLib stuff
        figure = plt.Figure(figsize=(8, 6), dpi=100)
        axes = figure.add_subplot(111)

        # Get points from file
        points = get_points('weight', 'weight',self.active_user)
        dates = points[0]
        weights = points[1]
        weights = [int(x) for x in weights]

        # Convert dates
        date_objects = [datetime.datetime.strptime(date, "%m/%d/%Y") for date in dates]

        # Plot points
        axes.plot(date_objects, weights)
        axes.set_title('Weight Overtime')
        axes.set_xlabel('Date')
        axes.set_ylabel('Weight')

        # Formats dates
        axes.xaxis.set_major_formatter(DateFormatter("%m/%d/%Y"))

        # Rotate labels
        for tick in axes.get_xticklabels():
            tick.set_rotation(45)

        figure.subplots_adjust(bottom=0.2)

        # Adjusting limits of graph
        axes.set_ylim(min(weights) - 5, max(weights) + 5)

        canvas = FigureCanvas(figure)
        self.graph_layout.addWidget(canvas)

        self.weigh_in_full_layout.addLayout(self.graph_layout)

    def on_selection_changed(self, selected_item):
        """
        Handles the event when a users selects a goal from the combo box. Then generates a graph to show user's
        progression.

        Clears old graph
        """
        self.goal_selected = selected_item
        print(self.goal_selected)
        try:
            # Try top remove old graph if any.
            self.goals_layout.removeItem(self.goal_graph_layout)
            self.goal_graph_layout.deleteLater()
        except:
            print('Could not remove graph')

        try:
            for i in reversed(range(self.goal_graph_layout.count())):
                self.goal_graph_layout.itemAt(i).widget().deleteLater()
        except:
            print('Failed to clear graph')

        self.goal_graph_layout = QVBoxLayout()

        # Building matPlotLib stuff
        figure = plt.Figure(figsize=(8, 6), dpi=100)
        axes = figure.add_subplot(111)

        # Get Workout id
        workout_id = get_workout_id(self.goal_selected)

        # Get points from file
        points = get_points(workout_id, 'weight',self.active_user)
        x = points[0]
        y = points[1]
        y = [int(x) for x in y]
        print(y)

        if len(x) > 0 and len(y) > 0:
            # Convert dates
            date_objects = [datetime.datetime.strptime(date, "%m/%d/%Y") for date in x]

            # Plot points
            axes.plot(date_objects, y)
            axes.set_title(f'{self.goal_selected} Progress')
            axes.set_xlabel('Date')
            axes.set_ylabel('Weight')

            # Formats dates
            axes.xaxis.set_major_formatter(DateFormatter("%m/%d/%Y"))

            # Rotate labels
            for tick in axes.get_xticklabels():
                tick.set_rotation(45)

            figure.subplots_adjust(bottom=0.2)
            # Adjusting limits of graph

            axes.set_ylim(min(y) - 5, max(y) + 5)

            canvas = FigureCanvas(figure)
            self.goal_graph_layout.addWidget(canvas)

            self.goals_layout.addLayout(self.goal_graph_layout)
        else:
            self.goal_graph_label.setText("This exercise doesn't have any data yet")
            print('made it to here')
            self.goals_layout.addLayout(self.goal_graph_layout)
