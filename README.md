# Playwright X Scraper

⚠️ **EDUCATION PURPOSE ONLY** ⚠️

This project is created **solely for educational and learning purposes**. It demonstrates browser automation techniques using Playwright with Python. Users are responsible for ensuring their use complies with applicable laws, terms of service, and ethical guidelines.

## 🎓 Learning Objectives

This project showcases:
- **Async/Await Patterns**: Modern Python async programming with Playwright
- **Browser Automation**: Controlling headless browsers with persistent contexts
- **Session Management**: Handling cookies and authentication state
- **Anti-Detection Techniques**: Basic stealth methods for browser automation
- **Web Scraping**: Extracting data from dynamic JavaScript-heavy websites

## 🛠️ Tech Stack

- **Python 3.8+** with asyncio
- **Playwright** - Browser automation library
- **Chromium** - Headless browser
- **CSS Selectors & XPath** - Element selection strategies

## 📋 Features

### Supported Platforms
- X/Twitter (`x.py`)

### Capabilities
- Persistent browser sessions (cookies saved between runs)
- Automated login with credentials via environment variables
- Profile data extraction (bio, description)
- Tweet/post scraping with configurable limits
- Multi-language support (English/Thai)
- Error handling and retry mechanisms
- Stealth mode to bypass basic bot detection

## 🚀 Setup

### Prerequisites
```bash
# Install Python 3.8+
python --version

# Install Playwright
pip install playwright
playwright install chromium
```

### Configuration
Create a `.env` file with your credentials:

```bash
# For X.com
X_EMAIL=your_email@example.com
X_PASSWORD=your_password
X_PROFILE_DIR=x_profile
```

**⚠️ SECURITY NOTE**: Never commit `.env` to version control! It's already in `.gitignore`.

### Running

```bash
# X.com automation
python x.py
```

## 📖 Usage Examples

### X.com Tweet Scraping
```python
# Extracts profile bio/description
# Scrapes first 3 tweets from timeline
# Returns: author, text, URL
```

## ⚖️ Legal & Ethical Disclaimer

**IMPORTANT**: This tool is provided for **educational purposes only**.

- ✅ **DO**: Use to learn browser automation and web scraping
- ✅ **DO**: Run on your own accounts with permission
- ❌ **DON'T**: Spam, harass, or abuse any platform
- ❌ **DON'T**: Violate Terms of Service of any platform
- ❌ **DON'T**: Scrape data without proper authorization
- ❌ **DON'T**: Use for commercial purposes without permission

**You are solely responsible** for how you use this code. The authors are not responsible for any misuse or damages.

## 🛡️ Best Practices

1. **Respect Rate Limits**: Add delays between requests
2. **Use Official APIs**: When available, prefer official APIs over scraping
3. **Obey robots.txt**: Check website scraping policies
4. **Get Permission**: Always get permission before scraping
5. **Protect Credentials**: Never share or commit credentials

## 📚 Project Structure

```
automate/
├── .gitignore          # Files to exclude from git
├── .env                # Credentials (NOT in git)
├── README.md           # This file
├── x.py               # X.com automation script
└── *_profile/         # Browser session data (NOT in git)
```

## 🔧 Configuration Options

### Browser Settings
- Headless mode toggle
- Custom user agents
- Locale and timezone settings
- Viewport dimensions
- Stealth arguments

### Scraping Limits
- Configurable tweet/post limits
- Retry attempts with exponential backoff
- Timeout settings

## 🐛 Troubleshooting

### Common Issues

**Issue**: Timeout errors
- **Solution**: Increase timeout or change `wait_until` condition

**Issue**: Login fails
- **Solution**: Manually login once to save session, check credentials

**Issue**: Elements not found
- **Solution**: Update selectors (platform UI changes frequently)

**Issue**: Bot detection
- **Solution**: Use stealth settings, rotate user agents, add delays

## 📝 Notes

- Sessions persist in profile directories
- Cookies auto-save between runs
- Anti-bot detection is basic (advanced detection may still trigger)
- Platform UI changes may break selectors periodically

## 🤝 Contributing

This is an educational project. Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests
- Share knowledge

## 📄 License

This project is provided as-is for educational purposes. Use at your own risk.

## ⚠️ Warnings

- Web scraping may violate website Terms of Service
- Automated account actions may lead to account suspension
- Public data scraping may have legal implications
- Always consult legal counsel before production use
