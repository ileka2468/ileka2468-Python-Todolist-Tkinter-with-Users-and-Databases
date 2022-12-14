from tkinter import *
from tkinter import ttk
from database import preRegister, preLogin, retrieve_content, insertPost
import placeholder as pl
from scrollFrame import VerticalScrolledFrame
from datetime import datetime

class Login:
    def __init__(self, master):
        self.master = master
        self.master.title("ToDoShit Login")
        self.master.geometry("500x300")
        self.master.resizable(False, False)

        self.mainFrame = Frame(master)
        self.mainFrame.pack(expand=True, fill="both")

        self.TitleFrame = Frame(self.mainFrame)
        self.TitleFrame.pack(pady=5)

        self.Title = Label(self.TitleFrame, text="ToDoShit Login", font=("Arial", 15))
        self.Title.pack()

        self.statusFrame = Frame(self.mainFrame)
        self.statusFrame.pack()

        self.statusLabel = Label(self.statusFrame, text="", font=("Arial", 10))
        self.statusLabel.pack()

        self.formFrame = LabelFrame(self.mainFrame, text="Login or Register", padx=10)
        self.formFrame.pack(pady=5)

        self.usernameLabel = Label(self.formFrame, text="Username:", font=("Arial", 10))
        self.usernameLabel.grid(row=0, column=0, pady=2.5)

        self.usernameEntry = Entry(self.formFrame, font=("Arial", 15))
        self.usernameEntry.grid(row=0, column=1, pady=10)

        self.PasswordLabel = Label(self.formFrame, text="Password:", font=("Arial", 10))
        self.PasswordLabel.grid(row=1, column=0, pady=2.5)

        self.passwordEntry = Entry(self.formFrame, font=("Arial", 15))
        self.passwordEntry.grid(row=1, column=1, pady=10)

        self.buttonFrame = Frame(self.mainFrame)
        self.buttonFrame.pack(pady=25)

        self.registerButton = Button(self.buttonFrame, text="Register", width=20, command=self.Register)
        self.registerButton.grid(row=0, column=0, padx=5)

        self.loginButton = Button(self.buttonFrame, text="Login", width=20, command=self.Login)
        self.loginButton.grid(row=0, column=1, padx=5)

        self.master.bind('<Return>', self.LoginBind)


    def getInfo(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        return (username, password)

    def Register(self):
        provided_creds = self.getInfo()
        status = preRegister(provided_creds[0], provided_creds[1])
        self.clearFields(len(provided_creds[0]), len(provided_creds[1]))
        self.updateLabel(status, False)

    def Login(self):
        self.provided_creds = self.getInfo()
        status = preLogin(self.provided_creds[0], self.provided_creds[1])
        self.clearFields(len(self.provided_creds[0]), len(self.provided_creds[1]))
        appStart = self.updateLabel(status, True)
        if appStart is not None:
            if appStart[0] == 1:
                self.openToDoList(appStart)

    def LoginBind(self, bind):
        self.provided_creds = self.getInfo()
        status = preLogin(self.provided_creds[0], self.provided_creds[1])
        self.clearFields(len(self.provided_creds[0]), len(self.provided_creds[1]))
        appStart = self.updateLabel(status, True)
        if appStart is not None:
            if appStart[0] == 1:
                self.openToDoList(appStart)


    def updateLabel(self, status, isLogin):
        if not isLogin:
            if status == "STATUS OK":
                self.statusLabel.config(text="User Registered", fg="green")
            elif status == "FORMAT ERROR":
                self.statusLabel.config(text="Username and passwords cannot contain spaces.", fg="red")
            elif status == "FORMAT EMPTY":
                self.statusLabel.config(text="Fields cannot be empty!.", fg="red")
            else:
                self.statusLabel.config(text="User already exists, choose a different username.", fg="red")
        else:
            if type(status) == tuple and status[0] == "STATUS OK":
                self.statusLabel.config(text="Logged in", fg="green")
                return 1, status
            else:
                self.statusLabel.config(text="Username or password did not match.", fg="red")

    def openToDoList(self, logged_in_user_info):
        self.master.destroy()
        self.new_master = Tk()
        self.newApp = mainApp(self.new_master, logged_in_user_info[1][1], logged_in_user_info[1][-1])
        self.new_master.mainloop()

    def clearFields(self, userCharLen, passCharLen):
        self.usernameEntry.delete(0, userCharLen)
        self.passwordEntry.delete(0, passCharLen)


class mainApp:
    def __init__(self, master, user, uid):
        self.uid = uid
        self.user = user
        self.master = master
        self.master.title("ToDoShit")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        self.mainFrame = Frame(master)
        self.mainFrame.pack(expand=True, fill="both")

        self.addReminderFrame = Frame(self.mainFrame, padx=100)
        self.addReminderFrame.pack()

        self.welcomeLabel = Label(self.addReminderFrame, text=f"Welcome, {user}", font=("Arial", 15))
        self.welcomeLabel.grid(row=0, column=0, pady=20)

        self.reminderEntry = pl.EntryWithPlaceholder(self.addReminderFrame, "Add new reminder")
        self.reminderEntry.grid(row=1, column=0, ipady=8, pady=30)

        self.photo = PhotoImage(file="plusresize.png")
        self.addReminderButton = Button(self.addReminderFrame, image=self.photo, borderwidth=0, command=self.addPost)
        self.addReminderButton.grid(row=1, column=1, padx=20)

        self.postsLabel = Label(self.addReminderFrame, text="", font=("Arial", 12))
        self.postsLabel.grid(row=2, column=0)

        self.contentFrame = VerticalScrolledFrame(self.mainFrame, padding=10)
        self.contentFrame.pack(pady=20)
        self.retreive_posts()


    def checkPost(self, reminder):
        if reminder != "Add new reminder":
            if reminder not in [""]:
                if not reminder.isspace():
                    now = datetime.now()
                    date = now.strftime("%m/%d/%Y")
                    time = now.strftime("%H:%M:%S")
                    lastrowid = insertPost(self.uid, reminder, date, time)
                    self.updatePosts(reminder)

    def updatePosts(self, content):
        self.counter += 1
        frame = LabelFrame(self.contentFrame.interior, text=f"Reminder {self.counter}", pady=5)
        text = Label(frame, text=f"{content}", font=("Arial", 10), width=70)
        frame.pack(pady=10, padx=10)
        text.pack()
        self.postsLabel.config(text=f"Amount of shit to do: {self.counter}")



    def addPost(self):
        reminder = self.reminderEntry.get()
        self.reminderEntry.delete(0, len(reminder))
        self.checkPost(reminder)

    def retreive_posts(self):
        userPosts = retrieve_content(self.uid)
        post_quantity = len(userPosts)
        self.postsLabel.config(text=f"Amount of shit to do: {post_quantity}")
        self.loadPosts(userPosts, post_quantity)

    def delete(self):
        print("delted")


    def sel(self):
        pass

    def loadPosts(self, posts, post_quantity):
        self.counter = 0
        self.posts = {}
        if post_quantity == 0:
            frame = LabelFrame(self.contentFrame.interior, pady=5, borderwidth=0)
            text = Label(frame, text=f" ", font=("Arial", 10), width=70)
            frame.pack(pady=10, padx=10)
            text.pack(side=LEFT)
        else:
            for post in posts:
                self.counter += 1
                var = IntVar()
                primary_id = post[0]
                content = post[2]
                frame = LabelFrame(self.contentFrame.interior, text=f"Reminder ID {primary_id}", pady=5)
                text = Label(frame, text=f"{content}", font=("Arial", 10), width=70)
                button = Radiobutton(frame, text=f"Delete post {self.counter}", variable=var, value=primary_id, command=self.sel)
                button.pack(anchor=W)
                frame.pack(pady=10, padx=10)
                text.pack()
                self.posts[primary_id] = text

                #add label to list or tuple with the content so it can be looked up and edited


window = Tk()
Login(window)

window.mainloop()

# devwindow = Tk()
# mainApp(devwindow, "Dev")
# devwindow.mainloop()
