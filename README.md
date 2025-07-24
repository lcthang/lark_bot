# Lark Bot – AI-powered HR Assistant

Lark Bot is an intelligent assistant designed for HR teams and employees, seamlessly integrated into the Lark platform. It offers automated HR support, employee self-service, and workflow automation, powered by advanced AI.

## Features

- **Employee Self-Service**: Answer common HR questions instantly.
- **Leave & Attendance Management**: Submit leave requests and check balances.
- **Policy Lookup**: Instantly retrieve HR policies and documents.
- **Automated Reminders**: Get notified about important HR deadlines.
- **Custom Workflows**: Automate repetitive HR tasks.

## Getting Started

### Prerequisites

- [Python 3.8+](https://www.python.org/)
- Lark bot credentials (App ID & Secret)
- (Optional) Docker

### Installation

Clone the repository:
```bash
git clone https://github.com/lcthang/lark_bot.git
cd lark_bot
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root with the following:
```env
LARK_APP_ID=your-app-id
LARK_APP_SECRET=your-app-secret
# Add other required settings here
```

### Running the Bot

```bash
python main.py
```

Or with Docker:
```bash
docker build -t lark_bot .
docker run --env-file .env lark_bot
```

## Usage

- Add the bot to your Lark workspace.
- Interact with it via direct messages or group chats.
- Example:  
  > "Apply for leave from Aug 1 to Aug 5"  
  > "What is the company’s remote work policy?"

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contact

Maintained by [lcthang](https://github.com/lcthang).  
For support or questions, open an issue on GitHub.
