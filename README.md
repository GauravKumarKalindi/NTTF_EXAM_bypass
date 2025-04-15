# GAURAV HACKS - Exam Retake Tool

![GAURAV HACKS Banner](https://img.shields.io/badge/GAURAV-HACKS-yellow?style=for-the-badge)

A Python-based tool that allows NTTF students to reattempt exams, with the new marks being updated in the server system. This tool provides a convenient way to retake tests and improve your academic performance.

## 📋 Features

- **Secure Authentication**: Safely authenticates users with their NTTF credentials
- **Exam Retake Capability**: Allows students to retake previously attempted exams
- **Colorful Interface**: User-friendly colorful terminal interface for better readability
- **Score Update**: Automatically updates new scores in the server after retaking exams
- **Cross-Platform**: Works on Windows, Linux, macOS, and Android (via Termux)

## ⚠️ Disclaimer

This tool is for educational purposes only. Users are responsible for their actions while using this tool. The author is not responsible for any misuse or consequences resulting from the improper use of this tool.

## 🔧 Requirements

- Python 3.6 or higher
- Internet connection
- NTTF student credentials

## 📥 Installation

### Windows/Mac/Linux PC

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/gaurav-hacks.git
   cd gaurav-hacks
   ```

2. Install required dependencies:
   ```
   pip install colorama requests
   ```

3. Run the script:
   ```
   python exam_retake.py
   ```

### Android (Termux)

1. Install Termux from the [Play Store](https://play.google.com/store/apps/details?id=com.termux) or [F-Droid](https://f-droid.org/packages/com.termux/)

2. Open Termux and run the following commands:
   ```
   pkg update && pkg upgrade
   pkg install python git
   pip install colorama requests
   git clone https://github.com/yourusername/gaurav-hacks.git
   ```

4. Run the script:
   ```
   cd gaurav-hacks
   python exam_nttf.py
   ```

### Running in Thonny IDE

1. Install [Thonny IDE](https://thonny.org/)

2. Open Thonny and install required packages:
   - Go to Tools → Manage packages...
   - Search for and install `colorama` and `requests`

3. Open the script file:
   - File → Open...
   - Navigate to the downloaded/cloned file and select it

4. Run the script by clicking the green play button or pressing F5

## 🚀 Usage Instructions

1. Launch the script using one of the methods described above
2. Enter your NTTF username when prompted
3. Enter your password when prompted
4. Enter the test ID for the exam you want to retake
5. Answer the questions by selecting options (a/b/c/d)
6. The tool will automatically submit your answers and update your score on the server

## 📝 How to Find Test ID

1. Log in to your NTTF learning portal
2. Navigate to the test/exam you want to retake
3. The test ID is usually visible in the URL or test details page
4. If you can't find it, check the network requests in your browser's developer tools when loading the test

## 🛠️ Troubleshooting

- **Authentication Failed**: Double-check your username and password
- **Test Data Not Found**: Verify the test ID is correct and that you have access to the test
- **Connection Issues**: Check your internet connection and try again
- **Submission Failed**: The test may have expired or have submission restrictions

## 💻 Technical Details

This script works by:
1. Authenticating the user with the NTTF server
2. Fetching test details and questions using the test ID
3. Allowing the user to answer questions again
4. Submitting the answers to the server using the same API that the official platform uses
5. Finalizing the test submission, which updates the scores in the system

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

- **GAURAV** - *Initial work* - [GitHub](https://github.com/GauravKumarKalindi)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!
