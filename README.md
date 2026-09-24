# 💙 Financial Help Hub

A beautiful, colorful web application for connecting people in need with generous donors.

## 🌟 Features

- **Beautiful UI** - 6 vibrant gradient color schemes inspired by tafcares.org
- **Inspirational Quotes** - 15 rotating charity/finance quotes from database
- **Authentication** - Secure login/signup with session management
- **Help Requests** - Browse and view people who need financial assistance
- **Donation Flow** - Easy donate modal with multiple payment methods
- **Admin Dashboard** - (Coming soon) Approve/reject requests
- **Mobile Responsive** - Works beautifully on all devices

## 🎨 Design Highlights

- Hero section with glass morphism effect
- Vibrant gradient card backgrounds (purple, pink, blue, green, yellow, dark blue)
- Smooth animations and hover effects
- Clean, modern interface

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** Supabase (PostgreSQL)
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Deployment:** Vercel (recommended) / Databricks Apps

## 📦 Project Structure

```
financial-help-hub/
├── app.py                 # Flask backend (auth, donations, admin)
├── database.py            # Supabase integration
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── .vercelignore         # Vercel ignore file
├── .gitignore            # Git ignore file
└── templates/
    └── index.html        # Beautiful colorful UI (570 lines)
```

## 🚀 Deployment Options

### Option 1: Vercel (Recommended for Public Access)

1. Fork/clone this repository
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import this repository
4. Add environment variables (see below)
5. Deploy!

### Option 2: Databricks Apps

1. Use Databricks Apps for internal/authenticated deployments
2. Follow Databricks Apps deployment guide

## 🔑 Environment Variables

Set these in your deployment platform:

```
SUPABASE_URL=https://tzrcjamabhduxezmeyze.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
SECRET_KEY=your_secret_key_here
```

## 📊 Database Schema

### Tables:
- `help_requests` - Financial assistance requests (extended with approval fields)
- `users` - User authentication and profiles
- `bank_details` - Payment information
- `payments` - Transaction tracking
- `documents` - File uploads
- `quotes` - Inspirational messages (15 quotes)
- `districts` - Geographic districts
- `categories` - Request categories

## 🎯 Usage

1. **Browse Requests** - View all approved help requests (public)
2. **Sign Up** - Create an account to donate or request help
3. **Donate** - Select a request and make a donation
4. **Request Help** - (Coming soon) Submit your own request for approval
5. **Admin** - (Coming soon) Approve/reject pending requests

## 🔧 Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd financial-help-hub

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SUPABASE_URL="your_url"
export SUPABASE_KEY="your_key"
export SECRET_KEY="your_secret"

# Run the app
python app.py

# Visit http://localhost:5000
```

## 📝 TODO

- [ ] Add request submission modal for authenticated users
- [ ] Build admin approval dashboard
- [ ] Add file upload for request photos/documents
- [ ] Implement payment gateway integration
- [ ] Add email notifications
- [ ] Add request progress tracking

## 🎨 Color Palette

The app uses 6 vibrant gradient schemes:
1. Purple-Violet: `#667eea → #764ba2`
2. Pink-Red: `#f093fb → #f5576c`
3. Blue-Cyan: `#4facfe → #00f2fe`
4. Green-Teal: `#43e97b → #38f9d7`
5. Pink-Yellow: `#fa709a → #fee140`
6. Cyan-Purple: `#30cfd0 → #330867`

## 📄 License

MIT License - feel free to use this project!

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 👨‍💻 Author

Built with ❤️ for those in need
