# PY26057 
PROJECT TITLE 

          FARMIO – Enhancing Trust and Quality in Farmer-to-Consumer  Applications

WORKFLOW OF THE PROJECT :

 ┌──────────────────────┐
 │      User Opens      │
 │      FARMIO App      │
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │  Language Selection  │
 │ (14 Regional Langs)  │
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │   User Role Select   │
 │  Farmer / Consumer  │
 └───────┬────────┬────┘
         │        │
         │        │
         ▼        ▼
 ┌────────────┐ ┌─────────────────┐
 │   Farmer   │ │    Consumer     │
 │   Login    │ │  Registration   │
 │  (OTP)     │ │   (Demo)        │
 └─────┬──────┘ └────────┬────────┘
       │                  │
       ▼                  ▼
┌────────────────┐   ┌───────────────────────┐
│ Farmer Uploads │   │ Consumer Uploads Image │
│ Product Image  │   │ (Shop Product)         │
│ / Live Video   │   └──────────┬────────────┘
└───────┬────────┘              │
        │                       │
        ▼                       ▼
 ┌──────────────────────────────────────────┐
 │      AI PROCESSING LAYER (Core)           │
 │                                          │
 │  Custom Vision Model (From Scratch)       │
 │  - Identifies product                     │
 │  - Detects damage / rot / scratches       │
 │  - Generates quality score                │
 └───────────────┬──────────────────────────┘
                 │
                 ▼
 ┌──────────────────────────────────────────┐
 │   LLM SUPPORT LAYER (Explanation Only)    │
 │  - Converts AI result into simple text    │
 │  - Translates output into local language  │
 │  - Builds trust via clear explanation     │
 └───────────────┬──────────────────────────┘
                 │
                 ▼
 ┌──────────────────────────────────────────┐
 │   Market Price Comparison Module          │
 │  - Fetches current market price           │
 │  - Compares with farmer-listed price      │
 └───────────────┬──────────────────────────┘
                 │
                 ▼
 ┌──────────────────────────────────────────┐
 │     Final Output to Consumer              │
 │  - Product image/video                   │
 │  - Quality report                        │
 │  - Price comparison                      │
 │  - Language-specific explanation          │
 └──────────────────────────────────────────┘

WORK DONE TILL NOW :

START
  ↓
Load Streamlit App
  ↓
Set Page Config (Title, Layout)
  ↓
Load Logo & Apply UI Styling
  ↓
Language Selection (14 Languages)
  ↓
Store Language in Session State
  ↓
Apply Selected Language to ALL Pages (for now 1 page)
   ↓
   ↓
User Type
   ├── Farmer
   │     ↓
   │  OTP Login
   │     ↓
   │  Live Video Verification (DEMO)
   │     ↓
   │  Upload Product (photo/video proof)
   │     ↓
   │  Farmer Dashboard
   │
   └── Consumer
         ↓
      OTP Login
         ↓
      UPLOADED VIDEO IS VIEWED
         ↓
      LLM model is used to identify the fruits uploaded by the user (till now)
         ↓
      RECOGNISES AND GIVE THE NAME 

PROJECT OBJECTIVE:

 * The primary objective of FARMIO is to enhance trust, quality
  transparency, and accessibility in Farmer‑to‑Consumer (F2C) marketplaces. The project aims to:

 * Build consumer trust in farmer‑sold products using visual proof and AI analysis
 
 * Enable quality verification of agricultural goods through image‑based intelligence

 * Reduce price exploitation by enabling market price comparison

 * Overcome language and literacy barriers using multi‑lingual and assisted access.

 Problem Statement:

 Existing Farmer‑to‑Consumer applications face several limitations
  
 ->Consumers cannot reliably verify the quality of products online
this makes the farmer difficult to sell their products.

 ->No easy way to compare shop prices with farmer prices.

 ->Limited regional language support excludes many farmers.

 Proposed Solution:

FARMIO addresses these gaps through three core solutions:

1️. AI‑Based Trust & Quality Verification (Farmer Side):

  ~Farmers upload live‑harvested product images or videos
 
  ~A custom‑trained vision‑based deep learning model analyzes the product

  ~The model identifies the product and detects quality issues such as:

    * Scratches
    * Rotten parts
    * Physical damage

  ~The system generates a quality assessment and review

  ~The uploaded media and AI review are shown to consumers
2.Consumer‑Side Image Recognition & Price Comparison:
 Consumers upload product images taken from shops

 The same custom‑trained model:

~Identifies the product
~Evaluates its quality under any condition
~The system fetches the current market price and compares it with:
~Farmer‑listed prices in the app
~Consumers receive a transparent recommendation.

3.Multi‑Lingual & Inclusive Access:
#The app supports 14+ Indian regional languages
#language selection is persistent across all pages
#Designed for simple navigation and assisted usage

TECHNOLOGIES USED TILL NOW:
 Frontend & Application Framework:
Streamlit – Python‑based web application framework for UI, navigation, and interaction.It makes the page to load to the next and give connectivity.

 Programming Language:
Python – Core language for frontend logic, backend processing, and AI integration.

 Authentication:
2Factor.in SMS OTP API – Secure OTP‑based farmer authentication and customer.
  Sends OTP via SMS
  Verifies OTP
  Confirms farmer identity.
 
 Multi‑Language Support:
Dictionary‑based internationalization
Supports English, Tamil, Telugu, Malayalam, Hindi, Urdu, Kannada, Bengali, Marathi, Gujarati, Punjabi, Assamese, Bhojpuri, Odia.
  (kept for 1 page as a demo)

 File Handling & Storage:
Local file system for storing uploaded images and videos      

AI & Machine Learning (Model Development):
Primary AI (Implemented): LLM Model

Vision‑based deep learning model trained from scratch
Current dataset: 13,680 fruit images (fresh, scratched, damaged, rotten)
Planned dataset: 1,75,000+ images across fruits, vegetables, and grains
Responsible for product identification and quality assessment under varied real‑world conditions.

FUTURE INHANCEMENT:
   LLM TRAINED MODEL FOR IMAGE UPLOADDED BY CONSUMER FOR THE NAME AND THE QUALITY.
   LLM TRAINED MODEL FOR IMAGE QUALITY VERIFICATION UPLOADED BY FARMER.
   THE IMPLEMENTATION OF REGIONAL LANGUAGE.

PROJECT OUTCOME:
Improved trust between farmers and consumers

Transparent quality verification using AI

Empowered consumers with price awareness

Increased farmer participation through regional language support

A scalable foundation for AI‑driven agricultural marketplaces.
