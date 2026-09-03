# Sales CRM & Lead Management System

A simple web-based Customer Relationship Management (CRM) system built with **Django** to help small businesses manage customers, leads, sales opportunities, follow-ups, and customer interactions from a centralized platform.

---

## 📌 Project Overview

The **Sales CRM & Lead Management System** is designed to provide businesses with a centralized and easy-to-use platform for managing their customer relationships and sales activities.

The system allows users to track leads from their initial entry through qualification and conversion into customers. It also provides tools for managing sales opportunities, recording customer interactions, and scheduling follow-up tasks.

The primary goal of the system is to replace scattered customer information and manual tracking methods with a structured digital CRM solution.

---

# 🎯 Business Problem

Small businesses and sales teams often manage customer and sales information using multiple disconnected tools such as:

* Excel or Google Sheets
* Notebooks
* Emails
* Messaging applications
* Separate documents

This creates several operational problems.

### 1. Scattered Customer Information

Customer information such as names, phone numbers, email addresses, companies, and notes may be stored in different locations.

This makes it difficult to find and maintain accurate customer information.

### 2. Missed Follow-Ups

Sales representatives may forget to follow up with leads or existing customers because follow-up activities are tracked manually.

This can result in lost sales opportunities.

### 3. Difficult Lead Tracking

Without a centralized system, it is difficult to determine the current status of a lead.

For example:

```text
New → Contacted → Qualified → Converted
                         ↓
                       Lost
```

### 4. Lack of Sales Visibility

Managers may not have a simple way to understand:

* How many leads are currently active
* How many leads have been converted
* How many sales opportunities are open
* Which deals have been won or lost
* Which follow-ups are pending

### 5. Lack of Interaction History

Customer conversations, calls, meetings, and notes can become difficult to track when they are stored across different applications.

---

# 💡 Proposed Solution

The CRM provides a centralized system for managing the complete basic sales lifecycle.

Users can:

* Store customer information
* Create and manage leads
* Track lead status
* Convert qualified leads into customers
* Manage sales opportunities
* Record customer interactions
* Create follow-up tasks
* Search and filter records
* Monitor sales activity through a dashboard

The system provides a single source of truth for customer and sales information.

---

# 🏢 Business Requirements Specification

## 1. User Authentication

The system shall provide secure user authentication.

### Requirements

* User login
* User logout
* Password-based authentication
* Session management
* Authentication-protected CRM pages

Django's built-in authentication framework will be used for user management.

---

## 2. Dashboard

The system shall provide a dashboard that gives users an overview of CRM activities.

### Dashboard Information

* Total customers
* Total leads
* Open opportunities
* Won opportunities
* Recent leads
* Upcoming follow-ups
* Recent activities
* Sales pipeline summary

Example:

```text
+-------------+-------------+-------------+-------------+
| Customers   | Leads       | Open Deals  | Won Deals   |
+-------------+-------------+-------------+-------------+
|     120     |     35      |     18      |     42      |
+-------------+-------------+-------------+-------------+
```

---

## 3. Customer Management

The system shall allow users to manage customer records.

### Customer Information

* Customer name
* Company
* Email
* Phone
* Address
* City
* Status
* Notes
* Created date
* Updated date

### Operations

Users shall be able to:

* Add customers
* View customers
* Edit customers
* Delete customers
* Search customers
* Filter customers

---

## 4. Lead Management

The system shall allow users to manage potential customers.

### Lead Information

* Lead name
* Company
* Email
* Phone
* Lead source
* Lead status
* Assigned user
* Notes
* Created date
* Updated date

### Lead Sources

The system may support sources such as:

* Website
* Referral
* Social Media
* Email
* Advertisement
* Other

### Lead Status

```text
New
Contacted
Qualified
Converted
Lost
```

---

## 5. Lead Conversion

The system shall allow users to convert a qualified lead into a customer.

### Conversion Flow

```text
New
 ↓
Contacted
 ↓
Qualified
 ↓
Converted
 ↓
Customer
```

When a lead is converted, the system should create or associate the corresponding customer record.

---

## 6. Sales Opportunity Management

The system shall allow users to manage potential sales deals.

### Opportunity Information

* Opportunity title
* Customer
* Deal amount
* Sales stage
* Probability
* Expected closing date
* Notes
* Created date
* Updated date

### Opportunity Stages

```text
Prospecting
Qualified
Proposal
Negotiation
Won
Lost
```

Example:

```text
Opportunity: Website Development
Customer: ABC Technologies
Amount: ₹80,000
Stage: Proposal
Probability: 60%
Expected Close Date: 15 September 2026
```

---

## 7. Follow-Up and Task Management

The system shall allow users to create and manage customer follow-up tasks.

### Task Information

* Task title
* Customer
* Lead
* Due date
* Priority
* Status
* Description
* Created by

### Priority

```text
Low
Medium
High
```

### Status

```text
Pending
Completed
```

Example:

```text
Task: Follow up with ABC Technologies
Due Date: 5 September 2026
Priority: High
Status: Pending
```

---

## 8. Customer Activity Management

The system shall allow users to record interactions with leads and customers.

### Activity Types

* Call
* Email
* Meeting
* Note
* Other

### Activity Information

* Customer
* Lead
* Activity type
* Subject
* Description
* Activity date
* Created by

Example:

```text
05 September 2026

Type: Call
Subject: Project Requirements

Discussed website development requirements
with the customer.
```

This provides a historical record of customer interactions.

---

## 9. Search and Filtering

The system shall provide basic search and filtering functionality.

### Customer Search

Users can search customers by:

* Name
* Company
* Email
* Phone

### Lead Filtering

Users can filter leads based on:

* Status
* Source
* Assigned user

### Opportunity Filtering

Users can filter opportunities based on:

* Sales stage
* Customer
* Status

---

# 🔄 Basic Business Workflow

The CRM should support the following basic business workflow:

```text
                    ┌───────────────┐
                    │     Lead      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Contacted   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Qualified   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Convert    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Customer    │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌────────────┐  ┌──────────┐
        │   Deal   │  │ Activities │  │  Tasks   │
        └──────────┘  └────────────┘  └──────────┘
```

---

# ✨ Core Features

| Feature                | Description                                         |
| ---------------------- | --------------------------------------------------- |
| Authentication         | Secure user login and logout                        |
| Dashboard              | Overview of CRM and sales activities                |
| Customer Management    | Create, view, update, and delete customers          |
| Lead Management        | Manage potential customers                          |
| Lead Tracking          | Track leads through different stages                |
| Lead Conversion        | Convert qualified leads into customers              |
| Opportunity Management | Track potential sales deals                         |
| Follow-Up Tasks        | Manage customer and lead follow-ups                 |
| Activity History       | Record calls, emails, meetings, and notes           |
| Search                 | Search customers and leads                          |
| Filtering              | Filter records based on status and other attributes |
| Django Admin           | Administrative management of CRM data               |

---

# 🛠️ Technology Stack

## Backend

* **Python**
* **Django**
* **Django ORM**
* **Django Authentication**

## Frontend

* **HTML5**
* **CSS3**
* **Bootstrap**
* **JavaScript**

## Database

* **SQLite** for development
* **PostgreSQL** can be used for production

## Deployment

The application can be deployed using:

* Gunicorn
* Nginx
* AWS EC2

---

# 🗄️ Core Data Entities

The application consists of the following primary entities:

```text
User
 │
 ├── Lead
 │
 ├── Task
 │
 └── Activity

Lead
 │
 └── Customer

Customer
 │
 ├── Opportunity
 ├── Activity
 └── Task
```

### Main Entities

* User
* Customer
* Lead
* Opportunity
* Task
* Activity

---

# 🔐 Security Requirements

The application should follow Django's standard security practices.

These include:

* Authentication-protected pages
* CSRF protection
* Password hashing
* Form validation
* Server-side validation
* Authentication-based access control
* Secure session management

---

# 🚀 Future Enhancements

The following features can be added in future versions:

* Role-based access control
* REST API using Django REST Framework
* Email integration
* Automated email notifications
* WhatsApp integration
* Advanced sales analytics
* CSV import/export
* Calendar integration
* Sales forecasting
* Customer segmentation
* AI-powered lead analysis
* Automated follow-up reminders

---

# 📄 Project Scope

This project focuses on providing a **basic but functional CRM solution** for small businesses and sales teams.

The MVP focuses on the core CRM lifecycle:

```text
Lead
 ↓
Qualification
 ↓
Conversion
 ↓
Customer
 ↓
Opportunity
 ↓
Follow-Up
 ↓
Interaction History
```

The system is designed to be simple, maintainable, and extendable while demonstrating the core capabilities of the Django framework.
