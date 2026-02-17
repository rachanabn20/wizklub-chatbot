# WizKlub Conversion Chatbot

**Live Demo:** [https://wizklub-chatbot-ga7qwrfvp83wvr89keirpl.streamlit.app/](https://wizklub-chatbot-ga7qwrfvp83wvr89keirpl.streamlit.app/)

---

## About

WizKlub Conversion Chatbot is an AI-powered lead qualification and conversion engine built for [WizKlub.com](https://wizklub.com). It engages website visitors, identifies whether they are a Parent or School representative, qualifies them through structured questions, captures contact details, applies intelligent lead scoring, and drives them toward booking a demo.

This is not just a chatbot. It is a full conversion funnel designed to reduce visitor drop-off and increase demo bookings.

---

## Problem Statement

WizKlub serves two primary audiences:

- **Parents** exploring STEM programs for their children
- **Schools** interested in partnership programs

Most website visitors drop off without taking action. This chatbot solves that by:

1. Engaging visitors the moment they land
2. Identifying their user type (Parent or School)
3. Collecting relevant qualification details
4. Scoring lead quality in real time
5. Nudging them toward booking a demo or speaking to the sales team

---

## Features

### Core Features (Mandatory)

| Feature | Description |
|---------|-------------|
| Live Hosted Chatbot | Deployed on Streamlit Cloud with shareable link |
| Parent Flow | 8-step qualification: Grade, Goals, Challenges, City, Budget, Name, Email, Phone |
| School Flow | 8-step qualification: School Name, Students, Board, Timeline, City, Name, Email, Phone |
| Lead Capture | Captures Name, Email, Phone, User Type with validation |
| Structured Questions | 5 qualification questions before lead capture in each flow |
| Rule-Based Logic | FAQ handling, flow routing, scoring algorithm |
| AI-Powered Responses | Optional OpenAI GPT integration for context-aware replies |

### Bonus Features

| Feature | Description |
|---------|-------------|
| Lead Scoring | 0-100 score based on grade, goals, challenges, city, budget, student count, timeline, school type |
| Intent Classification | Automatic High / Medium / Low intent tagging |
| Smart AI Responses | OpenAI GPT integration for dynamic, context-aware conversations |
| CRM Simulation | In-memory leads database with full qualification data |
| Admin Dashboard | Password-protected sidebar with live metrics, lead details, CSV export |

### Extra Features

| Feature | Description |
|---------|-------------|
| Email Validation | Regex-based email format validation |
| Phone Validation | 10-digit Indian phone number validation |
| Back Navigation | Go back to any previous step without losing data |
| Start Over | Reset entire conversation at any point |
| CSV Export | Download all captured leads as a CSV file |
| Urgency Triggers | Dynamic urgency messages for high-intent leads |
| Social Proof | Rotating statistics shown during conversion |
| Testimonials | Parent testimonial displayed at conversion stage |
| Visual Step Tracker | Animated dot indicator showing current progress |
| Score-Based CTAs | Different action buttons based on lead score |
| Conversation History | Full chat bubble history maintained throughout |
| Demo Booking Simulation | Simulated booking confirmation with details |
| Persistent Metrics | Metrics survive across multiple conversations |

---

## User Journey

### Parent Flow


Welcome Screen
|
v
Role Selection --> "I am a Parent"
|
v
Step 1: Child's Grade (Dropdown)
|
v
Step 2: Learning Goals (Multi-select)
|
v
Step 3: Current Challenges (Multi-select)
|
v
Step 4: City (Text Input)
|
v
Step 5: Budget Preference (Radio)
|
v
Step 6: Name (Text Input + Validation)
|
v
Step 7: Email (Text Input + Validation)
|
v
Step 8: Phone (Text Input + Validation)
|
v
Lead Score Calculated --> Intent Classified
|
v
Conversion Offer (Demo / Callback / Brochure)



### School Flow



Welcome Screen
|
v
Role Selection --> "I represent a School"
|
v
Step 1: School Name (Text Input)
|
v
Step 2: Student Count (Dropdown)
|
v
Step 3: Board Type (Dropdown)
|
v
Step 4: Decision Timeline (Radio)
|
v
Step 5: City (Text Input)
|
v
Step 6: Name (Text Input + Validation)
|
v
Step 7: Email (Text Input + Validation)
|
v
Step 8: Phone (Text Input + Validation)
|
v
Lead Score Calculated --> Intent Classified
|
v
Conversion Offer (Demo / Partnership Call / Brochure)



---

## Lead Scoring Algorithm

### Parent Scoring

| Factor | Condition | Points |
|--------|-----------|--------|
| Grade | Grade 3-8 (prime target) | +25 |
| Grade | Grade 1-2 | +15 |
| Grade | Grade 9-10 | +18 |
| Grade | Other grades | +8 |
| Learning Goals | High-value (Coding, Critical Thinking, AI, Competition) | +8 each |
| Learning Goals | Other goals | +4 each |
| Learning Goals | 3 or more selected | +5 bonus |
| Challenges | High-urgency (lacks interest, not performing, gifted) | +7 each |
| Challenges | Other challenges | +3 each |
| City | Tier 1 city | +10 |
| City | Other city | +5 |
| Budget | Not a concern | +10 |
| Budget | Moderate | +6 |
| Budget | Tight | +2 |
| Contact | Name provided | +3 |
| Contact | Email provided | +5 |
| Contact | Phone provided | +5 |

### School Scoring

| Factor | Condition | Points |
|--------|-----------|--------|
| Students | 2000+ | +30 |
| Students | 1000-2000 | +25 |
| Students | 500-1000 | +20 |
| Students | 300-500 | +15 |
| Students | 100-300 | +10 |
| School Type | International/Private/ICSE | +15 |
| School Type | Other boards | +8 |
| Timeline | Immediately (within 1 month) | +30 |
| Timeline | This quarter (1-3 months) | +20 |
| Timeline | Next session | +10 |
| Timeline | Just exploring | +5 |
| School Name | Provided | +5 |
| City | Tier 1 | +8 |
| City | Other | +4 |
| Contact | Name + Email + Phone | +13 |

### Intent Classification

| Score Range | Classification | Action |
|-------------|---------------|--------|
| 70-100 | High Intent | Book FREE Demo button + Urgency banner |
| 40-69 | Medium Intent | Demo + Callback + Brochure options |
| 0-39 | Low Intent | Brochure + Ask Question options |

---

## Conversion Strategy

### Psychological Triggers Used

| Trigger | Implementation |
|---------|---------------|
| Social Proof | "50,000+ students", "500+ schools", "98% approval" |
| Urgency | "Limited slots", "Only 5 left", "First month FREE" |
| Commitment | Progressive questioning creates micro-commitments |
| Personalization | Grade-specific messaging, city-specific community mentions |
| Authority | Specific outcome statistics build credibility |
| Reciprocity | Free assessment, free brochure offered before asking |

### Why Qualification Before Pitch

1. Builds trust -- user feels heard, not sold to
2. Creates investment -- after 5+ answers, abandonment drops
3. Enables personalization -- demo pitch matches their exact needs
4. Powers scoring -- sales team gets prioritized, qualified leads
5. Natural transition -- demo feels like logical next step

---

## Admin Dashboard

Access the admin dashboard by:

1. Click the sidebar arrow (top left)
2. Enter password: `wizklub2024`

### Dashboard Features

| Feature | Description |
|---------|-------------|
| Total Conversations | Count of all chat sessions started |
| Leads Captured | Count of completed lead submissions |
| Conversion Rate | Leads / Conversations percentage |
| High Intent Count | Number of high-scoring leads |
| Medium Intent Count | Number of medium-scoring leads |
| Low Intent Count | Number of low-scoring leads |
| Demo Requests | Count of demo bookings |
| Lead Details | Expandable cards with full lead information |
| CSV Download | Export all leads as CSV file |
| AI Configuration | Enter OpenAI API key to enable smart responses |
| Reset All | Clear all data and start fresh |

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend logic |
| Streamlit | Web framework and UI |
| OpenAI API | Optional AI-powered responses |
| CSV | Lead data export |
| In-Memory Storage | Lead database simulation |

---


---

## Lead Scoring Algorithm

### Parent Scoring

| Factor | Condition | Points |
|--------|-----------|--------|
| Grade | Grade 3-8 (prime target) | +25 |
| Grade | Grade 1-2 | +15 |
| Grade | Grade 9-10 | +18 |
| Grade | Other grades | +8 |
| Learning Goals | High-value (Coding, Critical Thinking, AI, Competition) | +8 each |
| Learning Goals | Other goals | +4 each |
| Learning Goals | 3 or more selected | +5 bonus |
| Challenges | High-urgency (lacks interest, not performing, gifted) | +7 each |
| Challenges | Other challenges | +3 each |
| City | Tier 1 city | +10 |
| City | Other city | +5 |
| Budget | Not a concern | +10 |
| Budget | Moderate | +6 |
| Budget | Tight | +2 |
| Contact | Name provided | +3 |
| Contact | Email provided | +5 |
| Contact | Phone provided | +5 |

### School Scoring

| Factor | Condition | Points |
|--------|-----------|--------|
| Students | 2000+ | +30 |
| Students | 1000-2000 | +25 |
| Students | 500-1000 | +20 |
| Students | 300-500 | +15 |
| Students | 100-300 | +10 |
| School Type | International/Private/ICSE | +15 |
| School Type | Other boards | +8 |
| Timeline | Immediately (within 1 month) | +30 |
| Timeline | This quarter (1-3 months) | +20 |
| Timeline | Next session | +10 |
| Timeline | Just exploring | +5 |
| School Name | Provided | +5 |
| City | Tier 1 | +8 |
| City | Other | +4 |
| Contact | Name + Email + Phone | +13 |

### Intent Classification

| Score Range | Classification | Action |
|-------------|---------------|--------|
| 70-100 | High Intent | Book FREE Demo button + Urgency banner |
| 40-69 | Medium Intent | Demo + Callback + Brochure options |
| 0-39 | Low Intent | Brochure + Ask Question options |

---

## Conversion Strategy

### Psychological Triggers Used

| Trigger | Implementation |
|---------|---------------|
| Social Proof | "50,000+ students", "500+ schools", "98% approval" |
| Urgency | "Limited slots", "Only 5 left", "First month FREE" |
| Commitment | Progressive questioning creates micro-commitments |
| Personalization | Grade-specific messaging, city-specific community mentions |
| Authority | Specific outcome statistics build credibility |
| Reciprocity | Free assessment, free brochure offered before asking |

### Why Qualification Before Pitch

1. Builds trust -- user feels heard, not sold to
2. Creates investment -- after 5+ answers, abandonment drops
3. Enables personalization -- demo pitch matches their exact needs
4. Powers scoring -- sales team gets prioritized, qualified leads
5. Natural transition -- demo feels like logical next step

---

## Admin Dashboard

Access the admin dashboard by:

1. Click the sidebar arrow (top left)
2. Enter password: `wizklub2024`

### Dashboard Features

| Feature | Description |
|---------|-------------|
| Total Conversations | Count of all chat sessions started |
| Leads Captured | Count of completed lead submissions |
| Conversion Rate | Leads / Conversations percentage |
| High Intent Count | Number of high-scoring leads |
| Medium Intent Count | Number of medium-scoring leads |
| Low Intent Count | Number of low-scoring leads |
| Demo Requests | Count of demo bookings |
| Lead Details | Expandable cards with full lead information |
| CSV Download | Export all leads as CSV file |
| AI Configuration | Enter OpenAI API key to enable smart responses |
| Reset All | Clear all data and start fresh |

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend logic |
| Streamlit | Web framework and UI |
| OpenAI API | Optional AI-powered responses |
| CSV | Lead data export |
| In-Memory Storage | Lead database simulation |

---


---

## How to Run Locally

### Prerequisites

- Python 3.10 or higher installed
- pip package manager

### Steps

1. Clone the repository


git clone https://github.com/rachanabn20/wizklub-chatbot.git
cd wizklub-chatbot

2. Install dependencies

pip install streamlit openai

3. Run the application

streamlit run app.py

4. Open in browser

http://localhost:8501
