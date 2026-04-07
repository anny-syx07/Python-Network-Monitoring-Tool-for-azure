# Network Monitoring & Security System (Azure Cloud)

This project is a comprehensive network monitoring solution featuring a real-time Python desktop application (Tkinter) and a localized Azure Flask API for persistent logging and monitoring.

## 🚀 Key Features
- **Real-time Monitoring**: Ping targets with live status updates (Online/Offline).
- **Interactive Visualizations**: Dynamic Matplotlib graphs showing connection stability over time.
- **LAN Scanning**: Quickly scan local IP ranges (e.g., .1 to .10) to discover active devices.
- **Cloud Integration**: Data is automatically sent to an Azure-hosted Flask API for centralized logging.
- **Security Hardening**: Secure API communication using Bearer Token authentication (`Anna-Secret-Token-2026`).
- **Fail-safe Logging**: Local CSV backup (`log.csv`) ensures data integrity if the cloud is unreachable.

## 📁 Project Structure
- `monitor.py`: Main desktop application GUI and logic.
- `azure_app/app.py`: Flask-based API for handling cloud logs.
- `log.csv`: Local backup dataset.
- `requirements.txt`: Python dependencies needed for local and cloud environments.

## 🛠 Setup & Installation
1. **Local App**:
   ```bash
   pip install -r requirements.txt
   python monitor.py
   ```
2. **Azure Deployment**:
   - The Flask app is pre-configured for Azure App Service.
   - Authentication is managed via `Authorization` headers.

## 🎓 Defense Documentation
This project was built for the Final Academic Defense (2026), focusing on:
1. **Cloud Architecture**: Integrating Desktop Apps with Azure App Services.
2. **Persistent Storage**: Handling real-time data flow.
3. **Security**: Implementing authentication tokens for API security.

---
*Developed as a high-performance network diagnostic tool.*
