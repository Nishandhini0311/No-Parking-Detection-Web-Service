# 🚫 AI-Based No Parking Detection Web Service

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask)
![YOLO](https://img.shields.io/badge/YOLO-Object%20Detection-red?style=for-the-badge)
![ESP32-CAM](https://img.shields.io/badge/ESP32--CAM-IoT-green?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?style=for-the-badge&logo=mysql)

---

## 📖 Overview

The **AI-Based No Parking Detection Web Service** is an intelligent traffic monitoring system designed to detect vehicles parked in restricted no-parking zones. The system captures vehicle images using an **ESP32-CAM**, detects vehicles using **YOLO**, extracts the vehicle registration number through **OCR (Tesseract)**, automatically generates a traffic fine, stores the violation details in a **MySQL** database, and sends an **SMS notification** to the vehicle owner using **Twilio**.

This project demonstrates the integration of **Artificial Intelligence**, **Computer Vision**, **Embedded Systems**, and **Web Technologies** to automate traffic violation management.

---

## 🎯 Objectives

- Detect vehicles parked in no-parking zones.
- Automatically recognize vehicle registration numbers.
- Generate traffic fines without manual intervention.
- Notify vehicle owners through SMS.
- Maintain violation records through a web dashboard.

---

## ✨ Features

- 🚗 Vehicle Detection using YOLO
- 🔍 Automatic Number Plate Recognition (OCR)
- 📄 Automatic Fine Generation
- 📱 SMS Notification using Twilio
- 🌐 Flask-based Web Application
- 🗄️ MySQL Database Integration
- 📊 Dashboard for Violation Monitoring

---

## 🛠️ Technologies Used

### Programming
- Python
- HTML
- CSS
- JavaScript

### Framework
- Flask

### AI & Computer Vision
- YOLO
- OpenCV
- OCR (Tesseract)

### Hardware
- ESP32-CAM

### Database
- MySQL

### Messaging Service
- Twilio SMS API

---

## ⚙️ System Workflow

1. ESP32-CAM captures the vehicle image.
2. YOLO detects the parked vehicle.
3. OCR (Tesseract) extracts the vehicle registration number.
4. Vehicle details are verified.
5. A traffic fine is automatically generated.
6. Violation details are stored in MySQL.
7. Twilio sends an SMS notification to the vehicle owner.
8. The dashboard displays all violation records.

---

## 📂 Repository Structure

```
No-Parking-Detection-Web-Service
│
├── app.py
├── index.html
├── dashboard.html
├── status.html
├── violations.html
└── .gitignore
```

---

## 🚀 Future Improvements

- Real-time CCTV integration
- Mobile application
- Online fine payment gateway
- GPS location tagging
- Cloud deployment
- AI analytics dashboard

---

## 👩‍💻 Author

**Nishandhini S**

Electronics and Communication Engineering (ECE)

Interested in Embedded Systems, IoT, Artificial Intelligence, and Computer Vision.
