# CRM Pro - User Manual

## Table of Contents

1. [Getting Started](#getting-started)
2. [Account Registration](#account-registration)
3. [Logging In](#logging-in)
4. [Dashboard](#dashboard)
5. [Customer Management](#customer-management)
6. [Lead Management](#lead-management)
7. [Opportunity Management](#opportunity-management)
8. [Activity Tracking](#activity-tracking)
9. [Task Management](#task-management)
10. [Editing & Deleting Records (CRUD)](#editing--deleting-records-crud)
11. [Sending Email](#sending-email)
12. [Bulk Email Marketing](#bulk-email-marketing)
13. [Email Log](#email-log)
14. [Navigation](#navigation)
15. [Password Security](#password-security)
16. [Logging Out](#logging-out)

---

## Getting Started

CRM Pro is a Customer Relationship Management system that helps you manage customers, leads, sales opportunities, activities, and tasks from a single platform.

### System Requirements

- A modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection (for Tailwind CSS CDN)

### Starting the Application

```bash
cd CRM
venv\Scripts\activate
python manage.py runserver
```

Open your browser and navigate to: `http://127.0.0.1:8000/crm/`

You will be redirected to the login page.

### Email Configuration (Development)

By default, emails are sent using Django's **console backend**, which prints the email content to the terminal instead of actually sending it. This is great for testing.

To send real emails, update the SMTP settings in `crm/settings.py`:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-app-password"
```

---

### Re-applying Migrations

The new email features require a database migration. If you cloned the project fresh:

```bash
python manage.py makemigrations user
python manage.py migrate
```

---

## Account Registration

1. On the login page, click **"Create account"** at the bottom.
2. Fill in the registration form:
   - **Username**: Choose a unique username
   - **Email**: Enter a valid email address
   - **Password**: Minimum 6 characters
   - **Confirm Password**: Re-enter the same password
3. Click **"Create Account"**.
4. You will be redirected to the login page with a success message.

> **Note**: Passwords are encrypted using PBKDF2-SHA256 with a random salt before being stored in the database.

---

## Logging In

1. Enter your **Username** and **Password**.
2. Click **"Sign In"**.
3. On successful login, you will be taken to the **Dashboard**.
4. If credentials are incorrect, an error message will be displayed.

---

## Dashboard

The dashboard provides an overview of your CRM data:

### Stats Cards (Top Row)
- **Total Customers**: Number of customers in the system
- **Total Leads**: Number of leads tracked
- **Open Opportunities**: Active sales opportunities
- **Pending Tasks**: Tasks awaiting completion

### Revenue Section
- **Revenue**: Total amount from won opportunities
- **Pipeline Value**: Total value of active (non-closed) opportunities

### Charts
- **Lead Status Distribution**: Visual breakdown of leads by status (New, Contacted, Qualified, Converted, Lost)
- **Opportunity Pipeline**: Visual breakdown of opportunities by stage

### Quick Stats
- Won Deals
- Lost Deals
- Tasks Completed

### Recent Data (Bottom Section)
- **Recent Leads**: Latest 5 leads added
- **Upcoming Tasks**: Next 5 pending tasks sorted by due date
- **Recent Customers**: Latest 5 customers added
- **Recent Activities**: Latest 5 logged activities

Click **"View all"** links to navigate to the full list pages.

---

## Customer Management

Navigate to **Customers** from the sidebar.

### Adding a Customer

1. Click **"Add New Customer"** to expand the form.
2. Fill in the fields:
   - **Customer Name** (required)
   - **Company** (required)
   - **Email Address** (required, must be unique)
   - **Phone Number** (required, must be unique)
   - **City** (required)
   - **Status**: Active or Inactive
   - **Address** (optional)
   - **Notes** (optional)
3. Click **"Add Customer"**.

### Viewing Customers

All customers are displayed in a table with columns:
- Name, Company, Email, Phone, City, Status, Created Date

### Customer Status
- **Active**: Customer is currently engaged
- **Inactive**: Customer is no longer active

---

## Lead Management

Navigate to **Leads** from the sidebar.

### Adding a Lead

1. Click **"Add New Lead"** to expand the form.
2. Fill in the fields:
   - **Lead Name** (required)
   - **Company** (required)
   - **Email Address** (required, must be unique)
   - **Phone Number** (required, must be unique)
   - **Lead Source**: Website, Referral, Social Media, or Other
   - **Status**: New, Contacted, Qualified, Converted, or Lost
   - **Assign To**: Select a user to assign the lead to
   - **Notes** (optional)
3. Click **"Add Lead"**.

### Lead Status Lifecycle

```
New -> Contacted -> Qualified -> Converted (becomes Customer)
                                    |
                                  Lost
```

### Viewing Leads

Leads are displayed with status badges color-coded:
- **Blue**: New
- **Amber**: Contacted
- **Purple**: Qualified
- **Green**: Converted
- **Red**: Lost

---

## Opportunity Management

Navigate to **Opportunities** from the sidebar.

### Adding an Opportunity

1. Click **"Add New Opportunity"** to expand the form.
2. Fill in the fields:
   - **Opportunity Title** (required)
   - **Customer** (required, select an existing customer)
   - **Amount** (required, in dollars)
   - **Stage**: Prospecting, Qualified, Proposal, Negotiation, Won, or Lost
   - **Probability** (0-100%)
   - **Expected Close Date** (required)
   - **Notes** (optional)
3. Click **"Add Opportunity"**.

### Opportunity Stages

| Stage | Description |
|-------|-------------|
| Prospecting | Initial identification of potential deal |
| Qualified | Lead has been qualified as a real opportunity |
| Proposal | A proposal has been sent to the customer |
| Negotiation | Actively negotiating terms |
| Won | Deal closed successfully |
| Lost | Deal was not won |

### Viewing Opportunities

Opportunities are displayed with stage badges color-coded:
- **Sky**: Prospecting
- **Indigo**: Qualified
- **Purple**: Proposal
- **Amber**: Negotiation
- **Green**: Won
- **Red**: Lost

---

## Activity Tracking

Navigate to **Activities** from the sidebar.

### Adding an Activity

1. Click **"Add New Activity"** to expand the form.
2. Fill in the fields:
   - **Customer** (required)
   - **Lead** (required)
   - **Activity Type**: Call, Email, Meeting, Note, or Other
   - **Subject** (required)
   - **Description** (optional)
   - **Activity Date & Time** (required)
   - **Created By** (select user)
3. Click **"Add Activity"**.

### Activity Types

- **Call**: Phone call with customer/lead
- **Email**: Email correspondence
- **Meeting**: In-person or virtual meeting
- **Note**: General notes about interaction
- **Other**: Any other type of interaction

---

## Task Management

Navigate to **Tasks** from the sidebar.

### Adding a Task

1. Click **"Add New Task"** to expand the form.
2. Fill in the fields:
   - **Task Title** (required)
   - **Customer** (required)
   - **Lead** (required)
   - **Due Date** (required)
   - **Priority**: Low, Medium, or High
   - **Status**: Pending or Completed
   - **Description** (optional)
   - **Created By** (select user)
3. Click **"Add Task"**.

### Priority Levels

- **High** (Red): Urgent tasks that need immediate attention
- **Medium** (Amber): Normal priority tasks
- **Low** (Sky): Tasks that can wait

### Task Status

- **Pending**: Task is not yet completed
- **Completed**: Task has been finished

---

## Editing & Deleting Records (CRUD)

Every management page (Customers, Leads, Opportunities, Activities, Tasks) supports full CRUD (Create, Read, Update, Delete) operations.

### Editing a Record

1. Navigate to the list page of the record you want to edit.
2. Find the row in the table.
3. Click the **pencil icon** (Edit) in the **Actions** column.
4. Update the fields in the form.
5. Click **"Save Changes"**.
6. You will be redirected back to the list with a success message.

### Deleting a Record

1. Navigate to the list page of the record you want to delete.
2. Find the row in the table.
3. Click the **trash icon** (Delete) in the **Actions** column.
4. A confirmation dialog will appear — click **OK** to confirm.
5. The record is permanently deleted and you are returned to the list.

> **Note**: Deleting is permanent and cannot be undone. Use with caution.

### Full CRUD Operations by Section

| Section | Create | View | Update | Delete |
|---------|--------|------|--------|--------|
| Customers | ✅ | ✅ | ✅ | ✅ |
| Leads | ✅ | ✅ | ✅ | ✅ |
| Opportunities | ✅ | ✅ | ✅ | ✅ |
| Activities | ✅ | ✅ | ✅ | ✅ |
| Tasks | ✅ | ✅ | ✅ | ✅ |

---

## Sending Email

Send a single email to a customer directly from the CRM.

### Steps

1. From the sidebar, click **"Send Email"** under **Email Marketing**.
2. Select a **customer** from the dropdown (their email address is used automatically).
3. Enter the **subject** of the email.
4. Write your **message** in the message box.
5. Click **"Send Email"**.

A record of the sent email is saved in the Email Log.

---

## Bulk Email Marketing

Send the same email to multiple customers (and optionally all leads) at once.

### Steps

1. From the sidebar, click **"Bulk Marketing"** under **Email Marketing**.
2. **Select Recipients**: Hold `Ctrl`/`Cmd` and click to choose multiple customers.
3. Optionally check **"Also include all Leads?"** to add every lead's email to the recipient list.
4. Enter the **subject** and **message**.
5. Click **"Send Bulk Email"**.

Duplicate email addresses are automatically merged (a customer and a lead with the same email receive it once).

### Recipient Count

The system tells you exactly how many recipients the email was sent to. Your message is delivered to all of them in a single campaign.

---

## Email Log

The Email Log records the history of every email sent through the CRM.

### Viewing the Email Log

- From the sidebar, click **"Email Log"** under **Email Marketing**.
- Each entry shows:
  - **Subject** of the email
  - **Recipients** (count and email addresses)
  - **Type**: Single or Bulk
  - **Status**: Sent or Failed
  - **Sent By**: The user who sent it
  - **Sent At**: Date and time

### Quick Actions

From the Email Log page you can quickly jump to:
- **Compose Email** — send a new single email
- **Bulk Marketing** — launch a new bulk campaign

---

## Navigation

### Sidebar Navigation

The sidebar provides quick access to all sections:

| Icon | Section | Description |
|------|---------|-------------|
| Home | Dashboard | Overview of CRM data |
| People | Customers | Customer records |
| Trending Up | Leads | Lead tracking |
| Dollar Sign | Opportunities | Sales opportunities |
| Clipboard | Activities | Interaction log |
| Check Circle | Tasks | Follow-up tasks |
| Plus | Send Email | Compose and send a single customer email |
| People | Bulk Marketing | Send email to multiple recipients |
| Envelope | Email Log | History of all sent emails |

### Collapsing the Sidebar

- **Desktop**: The sidebar remains visible on larger screens
- **Mobile**: Click the hamburger menu icon to toggle the sidebar

---

## Password Security

CRM Pro uses industry-standard password hashing:

- **Algorithm**: PBKDF2-SHA256
- **Iterations**: 100,000
- **Salt**: Random 16-byte salt per password
- **Storage**: Only the salt and hash are stored (never plaintext)

This ensures that even if the database is compromised, user passwords remain secure.

---

## Logout

1. Click the **logout icon** (door icon) in the sidebar bottom or top bar.
2. You will be redirected to the login page.

---

## Tips

1. **Dashboard first**: Check the dashboard daily for an overview of your CRM health
2. **Keep leads updated**: Update lead status regularly to maintain accurate pipeline data
3. **Log activities**: Record every interaction to maintain a complete communication history
4. **Set task priorities**: Use High priority for urgent follow-ups to avoid missed opportunities
5. **Create customers from leads**: Convert qualified leads into customers for better tracking

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cannot log in | Verify username and password are correct |
| Form not submitting | Ensure all required fields are filled |
| Page looks unstyled | Check internet connection (Tailwind CDN required) |
| Data not appearing | Refresh the page or check if you are logged in |

---

*CRM Pro v1.0 - Built with Django & Tailwind CSS*
